"""Negative fixtures ensure release checks reject realistic packaging drift."""
import importlib.util, struct, unittest, xml.etree.ElementTree as ET
from pathlib import Path
spec=importlib.util.spec_from_file_location('verify',Path(__file__).resolve().parents[2]/'scripts/android/verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

MANIFEST='''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.example.kinderwelt" android:versionCode="5" android:versionName="0.5.0"><uses-sdk android:minSdkVersion="24" android:targetSdkVersion="36"/><application android:allowBackup="false" android:extractNativeLibs="true"><activity android:screenOrientation="fullUser"><intent-filter><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>'''
TASK_IDS=['math_count','math_add','math_take','math_ten','math_compare','math_steps','math_twenty','math_split','german_sun','german_mouse','german_apple','german_rhyme','german_robot','german_read','german_flower','german_fish','logic_repeat','logic_triple','logic_odd','logic_shadow','logic_size','logic_double','logic_shape','logic_rule']
PAYLOAD=['assets/project.binary','assets/core/quest/main.gdc']
PAYLOAD += ['assets/'+n for n in ['games/quest/tasks.json','assets/voice/quest/manifest.json','assets/music/manifest.json','assets/quest/Nunito.ttf.import','assets/quest/landscape.png.import','assets/quest/icons.png.import','assets/quest/objects.png.import','assets/quest/appicon.png.import']]
PAYLOAD += ['assets/games/quest/'+s+'.gdc' for s in ['game','world','task','picture','progress','choice']]
for name in ['mina','leo','sam','jule']:
    PAYLOAD += ['assets/assets/quest/'+name+'.png.import','assets/.godot/imported/'+name+'.png-fixture.ctex']
for track in ['funkenflug','stars','meadow','gears','bounce','stories','garden','friends','rain','victory']:
    ext='.wav' if track in ['funkenflug','stars'] else '.ogg'
    PAYLOAD += ['assets/assets/music/'+track+ext+'.import','assets/.godot/imported/'+track+ext+'-fixture'+('.sample' if ext=='.wav' else '.oggvorbisstr')]
for name in ['choose','walk','success','again']+[task+suffix for task in TASK_IDS for suffix in ['', '_hint']]:
    PAYLOAD += ['assets/assets/voice/quest/'+name+'.ogg.import','assets/.godot/imported/'+name+'.ogg-fixture.oggvorbisstr']
PAYLOAD += ['assets/assets/quest/OFL.txt','assets/assets/voice/quest/MODEL_CARD.txt','assets/.godot/imported/Nunito.ttf-fixture.fontdata']+['assets/.godot/imported/'+image+'.png-fixture.ctex' for image in ['landscape','icons','objects','appicon']]

class VerificationTests(unittest.TestCase):
    def test_preview_identity_is_explicit_and_preserves_main_app(self):
        preview=ET.fromstring(MANIFEST.replace('org.example.kinderwelt','org.example.kinderwelt.preview'))
        with self.assertRaises(AssertionError):v.check_manifest(preview)
        self.assertEqual(v.check_manifest(preview,'org.example.kinderwelt.preview')['package'],'org.example.kinderwelt.preview')
    def test_valid_manifest(self):self.assertEqual(v.check_manifest(ET.fromstring(MANIFEST))['permissions'],[])
    def test_permission_rejected(self):
        root=ET.fromstring(MANIFEST);ET.SubElement(root,'uses-permission',{v.ANDROID+'name':'android.permission.INTERNET'})
        with self.assertRaises(AssertionError):v.check_manifest(root)
    def test_identity_version_sdk_backup_rotation_drift_rejected(self):
        for before,after in [('org.example.kinderwelt','org.wrong.app'),('versionCode="5"','versionCode="99"'),('targetSdkVersion="36"','targetSdkVersion="35"'),('allowBackup="false"','allowBackup="true"'),('fullUser','portrait'),('extractNativeLibs="true"','extractNativeLibs="false"')]:
            with self.subTest(before=before),self.assertRaises(AssertionError):v.check_manifest(ET.fromstring(MANIFEST.replace(before,after)))
    def test_valid_payload(self):self.assertEqual(v.check_payload(PAYLOAD),len(PAYLOAD))
    def test_development_and_key_files_rejected(self):
        for name in ['assets/addons/gut/test.gdc','assets/tests/smoke.gdc','assets/private.jks','assets/release.yaml','assets/docs/study.txt']:
            with self.subTest(name=name),self.assertRaises(AssertionError):v.check_payload(PAYLOAD+[name])
    def test_missing_modules_rejected(self):
        with self.assertRaises(AssertionError):v.check_payload([n for n in PAYLOAD if n!="assets/games/quest/tasks.json"])
    def test_missing_music_payload_rejected(self):
        with self.assertRaises(AssertionError):v.check_payload([n for n in PAYLOAD if n!="assets/.godot/imported/stars.wav-fixture.sample"])
    def test_every_required_runtime_asset_is_checked(self):
        for required in PAYLOAD:
            with self.subTest(required=required),self.assertRaises(AssertionError):v.check_payload([p for p in PAYLOAD if p!=required])
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
