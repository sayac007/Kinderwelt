"""Size claims use bundletool byte counts, not AAB/asset directory sizes."""
import importlib.util
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('download_size_test', ROOT / 'scripts/android/size_report.py')
size = importlib.util.module_from_spec(spec)
spec.loader.exec_module(size)


class SizeReportTests(unittest.TestCase):
    def test_numeric_bundletool_csv_is_authoritative(self):
        self.assertEqual(size.parse_size('MIN,MAX\r\n27,31\r\n'), {'min_bytes': 27, 'max_bytes': 31})
        for text in ['', 'MIN,MAX\n1MB,2MB', 'MIN,MAX\n-1,2', 'MIN,MAX\n3,2',
                     'MIN,MAX\n1,2\n3,4', 'SIZE\n123', 'notice\nMIN,MAX\n1,2', 'MIN,MAX\nNaN,2']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                size.parse_size(text)

    def test_category_classification_matches_shipped_paths(self):
        fixtures = {
            'assets/.godot/imported/voice_de_123.ogg-hash.oggvorbisstr': 'speech',
            'assets/assets/voice/quest/de/MODEL_CARD.txt': 'speech',
            'assets/.godot/imported/babbino.ogg-hash.oggvorbisstr': 'music',
            'assets/assets/music/manifest.json': 'music',
            'assets/.godot/imported/landscape.png-hash.ctex': 'graphics',
            'res/mipmap/icon.webp': 'graphics',
            'lib/arm64-v8a/libgodot_android.so': 'engine', 'classes2.dex': 'engine',
            'assets/.godot/imported/Nunito.ttf-hash.fontdata': 'other',
            'assets/games/quest/tasks.json': 'other', 'AndroidManifest.xml': 'other'}
        for name, expected in fixtures.items():
            self.assertEqual(size.category(name), expected, name)

    def test_interval_difference_is_conservative(self):
        result = size.difference({'min_bytes': 100, 'max_bytes': 120}, {'min_bytes': 20, 'max_bytes': 25})
        self.assertEqual(result, {'min_bytes': 75, 'max_bytes': 100})

    def test_base_budget_warns_without_rejecting_the_bundle(self):
        self.assertEqual(size.base_budget({'min_bytes': 0, 'max_bytes': 190_000_000})['status'], 'PASS')
        self.assertEqual(size.base_budget({'min_bytes': 0, 'max_bytes': 190_000_001})['status'], 'WARN')

    def test_report_orchestration_still_succeeds_over_budget_and_strips_secrets(self):
        # Only this orchestration test substitutes the external tool. Actual
        # download measurements are separately executed with pinned bundletool.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools = root / 'tools'
            (tools / 'android-tools').mkdir(parents=True)
            jar = tools / 'android-tools/bundletool-fixture.jar'
            jar.write_bytes(b'Synthetic tool fixture, never executed')
            (root / 'scripts/android').mkdir(parents=True)
            (root / 'scripts/android/toolchain.json').write_text(json.dumps({
                'bundletool_version': 'fixture', 'java': 'fixture',
                'bundletool_sha256': hashlib.sha256(jar.read_bytes()).hexdigest()}))
            bundle = root / 'neutral.aab'
            with zipfile.ZipFile(bundle, 'w') as archive:
                archive.writestr('assetPackInstallTime/assets/assets/quest/cast.json', json.dumps({'variant': 'public'}))
            original = bundle.read_bytes()
            calls = []
            def tool(command, env, log):
                calls.append([str(c) for c in command])
                self.assertFalse(any(k.startswith('KINDERWELT_UPLOAD_') for k in env))
                if 'build-apks' in command:
                    self.assertFalse(any(str(c).startswith('--ks') for c in command))
                    output = Path(next(c.split('=', 1)[1] for c in command if str(c).startswith('--output=')))
                    apk = output.parent / 'fixture.apk'
                    self.fixture(apk)
                    with zipfile.ZipFile(output, 'w') as archive:
                        archive.writestr('toc.pb', b'synthetic targeting metadata')
                        archive.write(apk, 'splits/base-master.apk')
                    return ''
                return 'MIN,MAX\n190000001,190000001\n' if '--modules=base' in command else 'MIN,MAX\n200000000,200000000\n'
            output = root / 'report'
            summary = root / 'summary.md'
            with patch.object(size, 'ROOT', root), patch.object(size, 'run', side_effect=tool), \
                 patch.dict(os.environ, {'KINDERWELT_UPLOAD_KEYSTORE': 'invalid-fixture-marker', 'GITHUB_STEP_SUMMARY': str(summary)}), \
                 contextlib.redirect_stdout(io.StringIO()) as console:
                report = size.measure(bundle, tools, output)
            self.assertEqual(report['base_budget']['status'], 'WARN')
            self.assertIn('::warning::', console.getvalue())
            self.assertEqual(bundle.read_bytes(), original)
            self.assertEqual(summary.read_text().strip(), (output / 'SIZE_REPORT.md').read_text().strip())
            self.assertEqual(sum('build-apks' in c for c in calls), 1)
            self.assertEqual(sum('get-size' in c for c in calls), 7)

    def test_zip_end_record_parser_handles_false_signatures_in_comments(self):
        comment = b'false signature in comment PK\x05\x06'
        end = struct.pack('<4s4H2IH', b'PK\x05\x06', 0, 0, 0, 0, 0, 123, len(comment))
        self.assertEqual(size._central_directory_offset(io.BytesIO(b'x' * 123 + end + comment)), 123)

    def fixture(self, path, descriptor=False):
        class NonSeekable(io.BytesIO):
            def seek(self, *args):
                raise io.UnsupportedOperation('streaming fixture')
        target = NonSeekable() if descriptor else io.BytesIO()
        files = {'assets/.godot/imported/voice_de_fixture.ogg-h.oggvorbisstr': b'voice fixture' * 100,
                 'assets/games/quest/tasks.json': b'{"tasks":[]}' * 20,
                 'lib/arm64-v8a/libgodot_android.so': b'engine fixture' * 80,
                 'assets/quest/icon.png': b'graphic fixture' * 30}
        with zipfile.ZipFile(target, 'w') as archive:
            archive.comment = b'ZIP comment retained verbatim'
            for index, (name, data) in enumerate(files.items()):
                entry = zipfile.ZipInfo(name, (2026, 1, 2, 3, 4, 6))
                entry.compress_type = zipfile.ZIP_DEFLATED if index % 2 else zipfile.ZIP_STORED
                entry.comment = b'entry comment'
                archive.writestr(entry, data)
        path.write_bytes(target.getvalue())
        return files

    def compressed_payload(self, path, name):
        with zipfile.ZipFile(path) as archive:
            info = archive.getinfo(name)
        with path.open('rb') as stream:
            stream.seek(info.header_offset)
            local = struct.unpack('<4s5H3I2H', stream.read(30))
            stream.seek(local[-2] + local[-1], 1)
            return stream.read(info.compress_size)

    def test_diagnostic_filter_preserves_surviving_compressed_bytes_and_crc(self):
        for descriptor in [False, True]:
            with self.subTest(descriptor=descriptor), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                original, target = root / 'source.apk', root / 'probe.apk'
                files = self.fixture(original, descriptor)
                before = original.read_bytes()
                removed = size.filter_apk(original, target, 'speech')
                self.assertEqual(removed, 1)
                self.assertEqual(before, original.read_bytes())
                with zipfile.ZipFile(target) as archive:
                    self.assertIsNone(archive.testzip())
                    self.assertEqual(archive.comment, b'ZIP comment retained verbatim')
                    for name, data in files.items():
                        if size.category(name) == 'speech':
                            self.assertNotIn(name, archive.namelist())
                        else:
                            self.assertEqual(archive.read(name), data)
                            self.assertEqual(self.compressed_payload(original, name), self.compressed_payload(target, name))

    def test_unaffected_apk_is_copied_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original, target = root / 'source.apk', root / 'probe.apk'
            self.fixture(original)
            self.assertEqual(size.filter_apk(original, target, 'music'), 0)
            self.assertEqual(original.read_bytes(), target.read_bytes())

    def test_probe_keeps_apk_set_targeting_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            apk = root / 'fixture.apk'
            self.fixture(apk)
            original, target = root / 'source.apks', root / 'probe.apks'
            with zipfile.ZipFile(original, 'w') as archive:
                archive.writestr('toc.pb', b'synthetic targeting metadata')
                archive.write(apk, 'asset-slices/fixture-master.apk')
            self.assertEqual(size.diagnostic_set(original, target, 'speech', root), 1)
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(archive.read('toc.pb'), b'synthetic targeting metadata')
                with zipfile.ZipFile(io.BytesIO(archive.read('asset-slices/fixture-master.apk'))) as inner:
                    self.assertIsNone(inner.testzip())
                    self.assertFalse(any(size.category(n) == 'speech' for n in inner.namelist()))

    def test_family_bundle_is_rejected_before_tools_or_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / 'not-public.aab'
            with zipfile.ZipFile(bundle, 'w') as archive:
                archive.writestr('assetPackInstallTime/assets/assets/quest/cast.json', json.dumps({'variant': 'family'}))
            with self.assertRaisesRegex(ValueError, 'neutral/public'):
                size.measure(bundle, root / 'no-tools', root / 'output')
            self.assertFalse((root / 'output').exists())

    def test_ci_runs_measurement_and_retains_reports_without_apk_sets(self):
        for name in ['android.yml', 'android-release.yml']:
            text = (ROOT / '.github/workflows' / name).read_text()
            self.assertIn('python3 scripts/android/size_report.py', text)
            self.assertIn('*.csv', text)
            self.assertIn('*.md', text)
            self.assertNotIn('*.apks', text)
