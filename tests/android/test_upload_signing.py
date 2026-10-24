"""Real cryptographic regressions use only an isolated, disposable test key.

No operator/release key is created, requested or used by this suite. Tool output,
test passwords and certificates are never printed or retained as artifacts.
"""
import base64
import importlib.util
import json
import os
import secrets
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('upload_test', ROOT / 'scripts/android/upload_signing.py')
signing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signing)
spec = importlib.util.spec_from_file_location('identity_release_test', ROOT / 'scripts/android/identity.py')
identity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(identity)


class ReleaseGuardTests(unittest.TestCase):
    def test_final_package_is_required_and_provisional_ids_are_rejected(self):
        for value in [None, '', identity.TOKEN, 'org.example.kinderwelt', 'de.kindertest.app', 'de.app.debug', 'de..app', 'de.public.app']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                identity.validate_release_package(value)
        self.assertEqual(identity.validate_release_package('de.publisher.kinderwelt'), 'de.publisher.kinderwelt')

    def test_cli_failures_precede_tool_access_and_artifact_creation(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith('KINDERWELT_')}
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'absent'
            cases = [([], 'Release requires --package-id'),
                     (['--package-id', 'org.example.kinderwelt'], 'must be final'),
                     (['--package-id', 'de.publisher.kinderwelt'], 'KINDERWELT_UPLOAD_KEYSTORE'),
                     (['--variant', 'family'], 'neutral/public'),
                     (['--preview'], 'without --preview')]
            for args, message in cases:
                result = subprocess.run(['python3', str(ROOT / 'scripts/android/build.py'), '--release', '--tools', '/nonexistent', '--output', str(out), *args], env=env, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertFalse(out.exists())

    def test_operator_placeholders_block_release(self):
        with self.assertRaisesRegex(ValueError, 'KINDERWELT_PUBLISHER'):
            signing.metadata({})
        env = dict(KINDERWELT_PUBLISHER='Synthetic operator fixture', KINDERWELT_SUPPORT_EMAIL='fixture@example.invalid', KINDERWELT_ASSET_LICENSE='Fixture only, no legal approval')
        self.assertEqual(signing.metadata(env)['publisher'], env['KINDERWELT_PUBLISHER'])
        env['KINDERWELT_SUPPORT_EMAIL'] = 'invalid'
        with self.assertRaisesRegex(ValueError, 'SUPPORT_EMAIL'):
            signing.metadata(env)

    def test_missing_credentials_and_invalid_alias_fail_without_values_in_errors(self):
        for omitted in signing.REQUIRED:
            values = {n: 'DO-NOT-PRINT' for n in signing.REQUIRED if n != omitted}
            with self.assertRaises(ValueError) as error:
                signing.credentials(values)
            self.assertIn(omitted, str(error.exception))
            self.assertNotIn('DO-NOT-PRINT', str(error.exception))

    def test_unsigned_export_children_receive_no_upload_secrets(self):
        env = {n: 'secret' for n in signing.REQUIRED}
        env.update({n: 'operator-info' for n in signing.METADATA_ENV.values()})
        env['PATH'] = '/tools'
        self.assertEqual(signing.export_environment(env), {'PATH': '/tools'})

    def test_verification_tool_diagnostics_do_not_corrupt_manifest_stdout(self):
        spec = importlib.util.spec_from_file_location('verify_release_io_test', ROOT / 'scripts/android/verify.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        result = verifier.command([sys.executable, '-c', 'import sys; print("Picked up JAVA_TOOL_OPTIONS: fixture", file=sys.stderr); print("<manifest />")'])
        self.assertEqual(result, '<manifest />\n')

    def test_base64_material_is_private_and_always_removed(self):
        values = {'KINDERWELT_UPLOAD_KEYSTORE': 'base64:' + base64.b64encode(b'synthetic-not-a-key').decode()}
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, 'fixture'):
                with signing.materialize(values, directory) as path:
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                    self.assertEqual(path.read_bytes(), b'synthetic-not-a-key')
                    raise RuntimeError('fixture')
            self.assertFalse(path.exists())
        for value in ['base64:!!!', 'base64:', str(ROOT / 'project.godot')]:
            with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
                with signing.materialize({'KINDERWELT_UPLOAD_KEYSTORE': value}, directory):
                    self.fail('Invalid keystore accepted')

    def test_tool_errors_do_not_expose_credentials(self):
        fake = subprocess.CompletedProcess([], 1, b'secret output', b'secret password')
        with patch.object(signing.subprocess, 'run', return_value=fake), self.assertRaisesRegex(ValueError, '^Safe failure$'):
            signing._tool(['tool'], {}, 'Safe failure')

    def test_both_presets_receive_one_version_source(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory)
            for name in ['project.godot', 'export_presets.cfg']:
                shutil.copy2(ROOT / name, app / name)
            identity.configure(app)
            text = (app / 'export_presets.cfg').read_text()
            self.assertEqual(text.count('version/code=' + str(identity.CONFIG['version_code'])), 2)
            self.assertEqual(text.count('version/name=' + json.dumps(identity.CONFIG['version_name'])), 2)
            self.assertNotIn('@KINDERWELT_VERSION_', text)
        raw = json.loads((ROOT / 'scripts/android/app-config.json').read_text())
        self.assertNotIn('version_name', raw)
        self.assertNotIn('version_code', raw)

    def test_manual_release_workflow_has_no_family_access_or_write_permission(self):
        text = (ROOT / '.github/workflows/android-release.yml').read_text()
        self.assertIn('workflow_dispatch:', text)
        self.assertNotIn('pull_request:', text)
        self.assertNotIn('  push:', text)
        self.assertNotIn('contents: write', text)
        self.assertNotIn('FAMILY_ASSETS', text)
        self.assertNotIn('.private', text)
        self.assertIn('Release signing SKIPPED', text)
        self.assertIn('--release --variant public', text)
        self.assertIn("if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'", text)
        self.assertIn('    environment: release\n', text)
        self.assertIn('TMPDIR: ${{ runner.temp }}/kinderwelt-release', text)

    def test_actual_ci_cleanup_removes_only_its_private_temporary_directory(self):
        text = (ROOT / '.github/workflows/android-release.yml').read_text()
        block = text.split('name: Remove private temporary signing files', 1)[1].split('        run: |\n', 1)[1]
        shell = '\n'.join(line[10:] for line in block.splitlines())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            private = root / 'kinderwelt-release'
            private.mkdir()
            (private / 'synthetic-marker').write_text('Not a real key')
            keep = root / 'unrelated-file'
            keep.write_text('Keep this')
            env = signing.export_environment()
            env['RUNNER_TEMP'] = str(root)
            result = subprocess.run(['bash', '-e', '-c', shell], env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(private.exists())
            self.assertEqual(keep.read_text(), 'Keep this')

    def test_actual_ci_preflight_skips_without_secrets(self):
        # Run the exact workflow shell block, not a mirrored implementation.
        text = (ROOT / '.github/workflows/android-release.yml').read_text()
        block = text.split('        run: |\n', 1)[1].split('      - ', 1)[0]
        shell = '\n'.join(line[10:] for line in block.splitlines())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'outputs'
            env = signing.export_environment()
            env['GITHUB_OUTPUT'] = str(output)
            result = subprocess.run(['bash', '-e', '-c', shell], env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(), 'ready=false\n')
            self.assertIn('Release signing SKIPPED', result.stdout)


class RealUploadSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        candidates = [ROOT.parent / 'tools/android-jdk', Path(os.environ.get('JAVA_HOME', '/nonexistent'))]
        cls.java = next((p for p in candidates if (p / 'bin/keytool').is_file()), None)
        if cls.java is None:
            keytool = shutil.which('keytool')
            if keytool:
                cls.java = Path(keytool).resolve().parents[1]
        if cls.java is None:
            raise unittest.SkipTest('JDK needed for actual signed/tampered archive regression')
        cls.temp = tempfile.TemporaryDirectory(prefix='kinderwelt-upload-test.')
        cls.directory = Path(cls.temp.name)
        cls.key = cls.directory / 'disposable-test.keystore'
        password = secrets.token_urlsafe(32)
        cls.values = dict(KINDERWELT_UPLOAD_KEYSTORE=str(cls.key), KINDERWELT_UPLOAD_ALIAS='fixture', KINDERWELT_UPLOAD_STORE_PASSWORD=password, KINDERWELT_UPLOAD_KEY_PASSWORD=password)
        env = signing.export_environment()
        env.update(cls.values)
        # Exception expressly allowed by package 1 acceptance: a test-only
        # throwaway key, outside source, destroyed by tearDownClass.
        signing._tool([cls.java / 'bin/keytool', '-genkeypair', '-keystore', cls.key, '-storepass:env', 'KINDERWELT_UPLOAD_STORE_PASSWORD', '-keypass:env', 'KINDERWELT_UPLOAD_KEY_PASSWORD', '-alias', 'fixture', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '2', '-dname', 'CN=Disposable Regression Fixture', '-storetype', 'JKS', '-noprompt'], env, 'Cannot create disposable regression key')
        cls.key.chmod(0o600)
        cls.fingerprint = signing.certificate(cls.key, cls.java, cls.values)
        cls.unsigned = cls.directory / 'unsigned.aab'
        with zipfile.ZipFile(cls.unsigned, 'w') as archive:
            archive.writestr('base/manifest/AndroidManifest.xml', b'synthetic signed-entry fixture')
            archive.writestr('assetPackInstallTime/assets/example.txt', b'fixture payload')
        cls.signed = cls.directory / 'signed.aab'
        signing.sign(cls.unsigned, cls.signed, cls.key, cls.java, cls.values)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'temp'):
            cls.temp.cleanup()

    def test_real_signature_and_expected_certificate(self):
        proof = signing.verify(self.signed, self.java, self.fingerprint)
        self.assertEqual(proof['signed_entries'], 2)
        self.assertEqual(proof['certificate_sha256'], self.fingerprint)

    def test_unsigned_bundle_and_wrong_certificate_are_rejected(self):
        for bundle, fingerprint in [(self.unsigned, self.fingerprint), (self.signed, '0' * 64)]:
            with self.assertRaisesRegex(ValueError, 'signature verification failed'):
                signing.verify(bundle, self.java, fingerprint)

    def test_modified_or_extra_unsigned_entry_is_rejected(self):
        for change in ['modified', 'added']:
            target = self.directory / (change + '.aab')
            with zipfile.ZipFile(self.signed) as source, zipfile.ZipFile(target, 'w') as dest:
                for item in source.infolist():
                    data = source.read(item.filename)
                    if change == 'modified' and item.filename.endswith('example.txt'):
                        data = b'tampered'
                    dest.writestr(item, data)
                if change == 'added':
                    dest.writestr('base/assets/unsigned.txt', b'unsigned injected file')
            with self.assertRaisesRegex(ValueError, 'signature verification failed'):
                signing.verify(target, self.java, self.fingerprint)

    def test_wrong_password_has_no_secret_diagnostics(self):
        values = dict(self.values, KINDERWELT_UPLOAD_KEY_PASSWORD=secrets.token_urlsafe(32))
        with self.assertRaises(ValueError) as error:
            signing.sign(self.unsigned, self.directory / 'wrong-password.aab', self.key, self.java, values)
        self.assertNotIn(values['KINDERWELT_UPLOAD_KEY_PASSWORD'], str(error.exception))
