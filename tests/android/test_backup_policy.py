"""Check real compiled backup exclusions and their manifest references."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/android'))
import backup_policy as policy


class BackupPolicyTests(unittest.TestCase):
    def test_both_variants_exclude_cloud_and_device_transfer_without_permissions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            policy.install(root)
            for variant in ['debug', 'release']:
                manifest = ET.parse(root / 'src' / variant / 'AndroidManifest.xml').getroot()
                self.assertFalse(manifest.findall('uses-permission'))
                self.assertEqual(manifest.find('application').get('{http://schemas.android.com/apk/res/android}allowBackup'), 'false')
            for attribute, name in policy.FILES.items():
                policy.validate_rules(ET.parse(root / 'res/xml' / (name + '.xml')).getroot(), attribute == 'dataExtractionRules')
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                policy.install(root)

    def test_incomplete_or_inclusive_rules_fail(self):
        for text in ['<full-backup-content/>', '<full-backup-content><include domain="file" path="avatars/"/></full-backup-content>',
                     '<data-extraction-rules><cloud-backup/></data-extraction-rules>']:
            with self.subTest(text=text), self.assertRaises(AssertionError):
                policy.validate_rules(ET.fromstring(text), 'data-extraction' in text)

    def test_actual_aapt_compiled_exclusions_are_referenced_and_checked(self):
        tools = Path('/workspace/tools/android-sdk')
        aapt = tools / 'build-tools/36.1.0/aapt2'
        android = tools / 'platforms/android-36/android.jar'
        if not aapt.is_file() or not android.is_file():
            self.skipTest('Local SDK resource integration; real CI APK verifier also checks these rules')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            policy.install(root)
            manifest = root / 'manifest.xml'
            original = (root / 'src/debug/AndroidManifest.xml').read_text()
            manifest.write_text(original.replace('<manifest ', '<manifest package="org.example.backuptest" '))
            subprocess.run([str(aapt), 'compile', '--dir', str(root / 'res'), '-o', str(root / 'resources.zip')], check=True, capture_output=True)
            subprocess.run([str(aapt), 'link', '-I', str(android), '--manifest', str(manifest), '--min-sdk-version', '24', '--target-sdk-version', '36', '-o', str(root / 'fixture.apk'), str(root / 'resources.zip')], check=True, capture_output=True)
            tree = subprocess.check_output([str(aapt), 'dump', 'xmltree', str(root / 'fixture.apk'), '--file', 'AndroidManifest.xml'], text=True)
            self.assertEqual(policy.verify_apk(aapt, root / 'fixture.apk', tree)['device_transfer'], 'excluded')
            with self.assertRaisesRegex(AssertionError, 'does not reference'):
                policy.verify_apk(aapt, root / 'fixture.apk', tree.replace('android:dataExtractionRules', 'android:wrongReference'))


if __name__ == '__main__':
    unittest.main()
