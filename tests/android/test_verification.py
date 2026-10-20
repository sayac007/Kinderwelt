"""Negative fixtures ensure release checks reject realistic packaging drift."""
import importlib.util, struct, unittest, xml.etree.ElementTree as ET
from pathlib import Path
spec=importlib.util.spec_from_file_location('verify',Path(__file__).resolve().parents[2]/'scripts/android/verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

MANIFEST='''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.example.kinderwelt" android:versionCode="1" android:versionName="0.1.0"><uses-sdk android:minSdkVersion="24" android:targetSdkVersion="36"/><application android:allowBackup="false"><activity android:screenOrientation="fullUser"><intent-filter><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>'''
PAYLOAD=['assets/project.binary','assets/core/main.gdc','assets/content/modules.json','assets/content/locales/de.json']+['assets/games/'+m+'/levels.json' for m in ['logic','math','language','autonomy','social']]

class VerificationTests(unittest.TestCase):
    def test_valid_manifest(self):self.assertEqual(v.check_manifest(ET.fromstring(MANIFEST))['permissions'],[])
    def test_permission_rejected(self):
        root=ET.fromstring(MANIFEST);ET.SubElement(root,'uses-permission',{v.ANDROID+'name':'android.permission.INTERNET'})
        with self.assertRaises(AssertionError):v.check_manifest(root)
    def test_identity_version_sdk_backup_rotation_drift_rejected(self):
        for before,after in [('org.example.kinderwelt','org.wrong.app'),('versionCode="1"','versionCode="2"'),('targetSdkVersion="36"','targetSdkVersion="35"'),('allowBackup="false"','allowBackup="true"'),('fullUser','portrait')]:
            with self.subTest(before=before),self.assertRaises(AssertionError):v.check_manifest(ET.fromstring(MANIFEST.replace(before,after)))
    def test_valid_payload(self):self.assertEqual(v.check_payload(PAYLOAD),9)
    def test_development_and_key_files_rejected(self):
        for name in ['assets/addons/gut/test.gdc','assets/tests/smoke.gdc','assets/private.jks','assets/release.yaml','assets/docs/study.txt']:
            with self.subTest(name=name),self.assertRaises(AssertionError):v.check_payload(PAYLOAD+[name])
    def test_missing_modules_rejected(self):
        with self.assertRaises(AssertionError):v.check_payload(PAYLOAD[:-1])
    def test_elf_16kb(self):
        data=bytearray(120);data[:5]=b'\x7fELF\x02';struct.pack_into('<Q',data,32,64);struct.pack_into('<HH',data,54,56,1);struct.pack_into('<IIQQQQQQ',data,64,1,0,0,0,0,0,0,16384)
        v.elf_alignment(data)
        struct.pack_into('<Q',data,112,4096)
        with self.assertRaises(AssertionError):v.elf_alignment(data)
    def test_activity_alias_target_is_checked(self):
        root=ET.fromstring(MANIFEST);app=root.find('application');activity=app.find('activity');activity.set(v.ANDROID+'name','com.godot.game.GodotApp')
        intent=activity.find('intent-filter');activity.remove(intent)
        alias=ET.SubElement(app,'activity-alias',{v.ANDROID+'targetActivity':'com.godot.game.GodotApp'});alias.append(intent)
        self.assertEqual(v.check_manifest(root)['orientation'],'fullUser')
        alias.set(v.ANDROID+'targetActivity','missing')
        with self.assertRaises(AssertionError):v.check_manifest(root)
    def test_debuggable_release_is_rejected(self):
        root=ET.fromstring(MANIFEST);root.find('application').set(v.ANDROID+'debuggable','true')
        with self.assertRaises(AssertionError):v.check_manifest(root)
    def test_non_elf_rejected(self):
        with self.assertRaises(AssertionError):v.elf_alignment(b'invalid')

if __name__=='__main__':unittest.main()
