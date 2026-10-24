"""Source scope, same-version recordings and actual packaged notice bytes."""
import configparser
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


music = load('asset_music_notices_test', 'scripts/music/notices.py')
notices = load('android_asset_notices_test', 'scripts/android/asset_notices.py')
signing = load('asset_license_guard_test', 'scripts/android/upload_signing.py')


class AssetNoticeTests(unittest.TestCase):
    def test_each_share_alike_recording_keeps_the_original_version_and_url(self):
        tracks = json.loads((ROOT / 'scripts/music/catalog.json').read_text())['tracks']
        manifest = json.loads((ROOT / 'assets/music/manifest.json').read_text())['tracks']
        fixtures = json.loads((ROOT / 'scripts/music/notice-license-fixtures.json').read_text())
        text = (ROOT / 'assets/music/NOTICES.txt').read_text()
        count = 0
        for original, actual, fixture in zip(tracks, manifest, fixtures):
            with self.subTest(track=original['id']):
                license, url = fixture.removeprefix('Lizenz: ').split(' · ')
                self.assertEqual(actual['license'], license)
                self.assertEqual(actual['license_url'], url)
                if license.startswith('CC-BY-SA-'):
                    count += 1
                    recording = actual['recording_license']
                    self.assertEqual((recording['license'], recording['url']), (license, url))
                    self.assertEqual(set(recording['notices']), {'de', 'en', 'ru'})
                    for locale, prefix in [('de', 'Die Aufnahme in dieser App'), ('en', 'The recording in this app'), ('ru', 'Запись в этом приложении')]:
                        notice = recording['notices'][locale]
                        self.assertIn(prefix, notice)
                        self.assertIn(license, notice)
                        self.assertIn(url, notice)
                    self.assertIn(recording['notices']['de'], text)
                else:
                    self.assertNotIn('recording_license', actual)
        self.assertEqual(count, 5)
        self.assertEqual(text, music.render_notices())
        self.assertEqual((ROOT / 'assets/music/manifest.json').read_text(), music.manifest_notices())

    def test_recording_metadata_preserves_cached_audio_and_rejects_wrong_versions(self):
        track = {'license': 'CC-BY-SA-4.0', 'file': 'cached.ogg', 'sha256': 'unchanged audio hash', 'bytes': 123, 'seconds': 12.5}
        result = music.with_recording_terms(track, 'https://creativecommons.org/licenses/by-sa/4.0/')
        for key, value in track.items():
            self.assertEqual(result[key], value)
        self.assertNotIn('recording_license', track)
        with self.assertRaisesRegex(ValueError, 'differs'):
            music.with_recording_terms(track, 'https://creativecommons.org/licenses/by-sa/3.0/')
        with self.assertRaisesRegex(ValueError, 'Unsupported ShareAlike'):
            music.recording_terms({'license': 'CC-BY-SA-unspecified'})

    def test_both_real_export_filters_include_all_fifteen_required_notices(self):
        self.assertEqual(notices.check_filters(), 15)
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (ROOT / 'assets/licenses/Kinderwelt-MIT.txt').read_bytes())
        required = set(notices.required())
        self.assertIn('assets/music/NOTICES.txt', required)
        self.assertIn('assets/quest/OFL.txt', required)
        for locale in ['de', 'en', 'ru']:
            self.assertIn(f'assets/voice/quest/{locale}/MODEL_CARD.txt', required)
            self.assertIn(f'assets/voice/quest/{locale}/LICENSE.txt', required)

    def source_fixture(self, root):
        shutil.copy2(ROOT / 'export_presets.cfg', root / 'export_presets.cfg')
        for name in notices.required():
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)

    def test_filter_removal_or_explicit_exclusion_fails_in_either_preset(self):
        for preset in ['preset.0', 'preset.1']:
            for action in ['remove_include', 'exclude_voice']:
                with self.subTest(preset=preset, action=action), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    self.source_fixture(root)
                    config = configparser.ConfigParser(interpolation=None)
                    config.read(root / 'export_presets.cfg')
                    if action == 'remove_include':
                        config[preset]['include_filter'] = '"games/quest/*.json"'
                    else:
                        config[preset]['exclude_filter'] = '"assets/voice/quest/en/LICENSE.txt"'
                    with (root / 'export_presets.cfg').open('w') as stream:
                        config.write(stream)
                    with self.assertRaisesRegex(ValueError, 'excluded'):
                        notices.check_filters(root)

    def test_missing_source_notice_blocks_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.source_fixture(root)
            (root / 'assets/voice/quest/en/LICENSE.txt').unlink()
            with self.assertRaisesRegex(ValueError, 'source notice is missing'):
                notices.check_filters(root)

    def archive(self, prefix, mutation=None, target=None):
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as archive:
            for name in notices.required():
                if mutation == 'missing' and name == target:
                    continue
                data = (ROOT / name).read_bytes()
                if mutation == 'changed' and name == target:
                    data = b'Stale or replaced notice'
                archive.writestr(prefix + name, data)
                if mutation == 'duplicate' and name == target:
                    archive.writestr('unexpected/assets/' + name, data)
        output.seek(0)
        return zipfile.ZipFile(output)

    def test_actual_notice_bytes_work_in_apk_base_and_install_time_pack(self):
        for prefix in ['assets/', 'base/assets/', 'assetPackInstallTime/assets/']:
            with self.subTest(prefix=prefix), self.archive(prefix) as archive:
                self.assertEqual(notices.check_archive(archive), {'status': 'PASS', 'files_checked': 15})

    def test_every_missing_modified_or_duplicate_packaged_notice_is_rejected(self):
        for prefix in ['assets/', 'base/assets/', 'assetPackInstallTime/assets/']:
            for action in ['missing', 'changed', 'duplicate']:
                for name in notices.required():
                    with self.subTest(prefix=prefix, action=action, name=name), self.archive(prefix, action, name) as archive:
                        with self.assertRaises(AssertionError):
                            notices.check_archive(archive)

    def test_operator_asset_licence_stays_unselected_and_release_blocked(self):
        text = (ROOT / 'ASSETS_LICENSE.md').read_text()
        self.assertIn('{{ASSET_LIZENZ_DES_BETREIBERS}}', text)
        self.assertIn('not a blanket licence', text)
        self.assertIn('dataset', text)
        with self.assertRaisesRegex(ValueError, 'KINDERWELT_ASSET_LICENSE'):
            signing.metadata({'KINDERWELT_PUBLISHER': 'Synthetic fixture only', 'KINDERWELT_SUPPORT_EMAIL': 'fixture@example.invalid'})

    def test_english_notice_does_not_invent_a_model_or_output_grant(self):
        manifest = json.loads((ROOT / 'assets/voice/quest/en/manifest.json').read_text())
        text = (ROOT / 'assets/voice/quest/en/LICENSE.txt').read_text()
        self.assertIn(manifest['model'], text)
        self.assertIn(manifest['model_source'], text)
        self.assertIn('License: public domain', text)
        self.assertIn('does not contain a separate', ' '.join(text.split()))
        self.assertIsNone(manifest.get('model_license'))

    def test_legacy_dates_match_the_existing_evidence_without_claiming_authentication(self):
        registry = json.loads((ROOT / 'art/character-origins.json').read_text())['historical_excluded']
        ledger = json.loads((ROOT / 'scripts/qa/visual-ip-owner-review.json').read_text())
        chronology = {r['source_sha256']: r for r in ledger['legacy_chronology']['files']}
        text = (ROOT / 'docs/character-origins.md').read_text()
        for entry in registry:
            self.assertEqual(entry['c2pa_creation_claim_utc'], chronology[entry['sha256']]['creation_claim_utc'])
            self.assertIn(entry['c2pa_creation_claim_utc'], text)
            display = datetime.fromisoformat(entry['c2pa_creation_claim_utc'].replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Berlin'))
            self.assertIn(display.strftime('%H:%M:%S CEST'), text)
        self.assertIn('have not\nbeen cryptographically verified', text)
        self.assertNotIn('Herkunft in den untersuchten historischen Dateien nicht hinreichend belegt', text)
