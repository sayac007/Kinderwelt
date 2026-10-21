"""Negative fixtures ensure release checks reject realistic packaging drift."""
import importlib.util, io, json, struct, zipfile, unittest, xml.etree.ElementTree as ET
from pathlib import Path
spec=importlib.util.spec_from_file_location('verify',Path(__file__).resolve().parents[2]/'scripts/android/verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

MANIFEST='''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.example.kinderwelt" android:versionCode="10" android:versionName="0.7.3"><uses-sdk android:minSdkVersion="24" android:targetSdkVersion="36"/><application android:allowBackup="false" android:extractNativeLibs="true"><activity android:screenOrientation="fullUser"><intent-filter><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>'''
PAYLOAD=['assets/core/quest/wardrobe.gdc','assets/core/quest/score_badge.gdc','assets/core/mobile.gdc','assets/project.binary','assets/core/quest/main.gdc']
PAYLOAD += ['assets/'+n for n in ['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/quest/cast.json','assets/music/manifest.json','assets/quest/Nunito.ttf.import','assets/quest/landscape.png.import','assets/quest/icons.png.import','assets/quest/objects.png.import','assets/quest/appicon.png.import']]
PAYLOAD += ['assets/games/quest/'+s+'.gdc' for s in ['game','world','task','picture','progress','choice']]
CAST=json.loads((Path(__file__).resolve().parents[2]/'assets/quest/cast.json').read_text())
for path in sorted(set(CAST['sprites'].values())|set(CAST['atlases'].values())):
    if path.endswith('.png'):
        PAYLOAD += ['assets/'+path+'.import','assets/.godot/imported/'+Path(path).name+'-fixture.ctex']
    else:PAYLOAD += ['assets/'+path]
PAYLOAD += ['assets/assets/quest/'+image+'.png.import' for image in ['home','castle']]
for track in [t['id'] for t in json.loads((Path(__file__).resolve().parents[2]/'scripts/music/catalog.json').read_text())['tracks']]:
    ext='.ogg'
    PAYLOAD += ['assets/assets/music/'+track+ext+'.import','assets/.godot/imported/'+track+ext+'-fixture'+('.sample' if ext=='.wav' else '.oggvorbisstr')]
for locale in ['de','en','ru']:
    folder='assets/voice/quest/'+locale+'/'
    manifest=json.loads((Path(__file__).resolve().parents[2]/folder/'manifest.json').read_text())
    PAYLOAD += ['assets/'+folder+name for name in ['manifest.json','MODEL_CARD.txt']]
    for filename in sorted({c['file'] for c in manifest['clips']}):
        PAYLOAD += ['assets/'+folder+filename+'.import','assets/.godot/imported/'+filename+'-fixture.oggvorbisstr']
PAYLOAD += ['assets/core/quest/language.gdc']
PAYLOAD += ['assets/assets/quest/'+name+'.png.import' for name in ['science-a','science-b']]
PAYLOAD += ['assets/assets/quest/OFL.txt','assets/.godot/imported/Nunito.ttf-fixture.fontdata']+['assets/.godot/imported/'+image+'.png-fixture.ctex' for image in ['landscape','icons','objects','appicon','science-a','science-b','home','castle']]
PAYLOAD += ['assets/core/quest/pet.gdshader']+['assets/assets/music/'+name for name in ['licenses/CC-BY-SA-4.0.txt','licenses/CC-BY-3.0.txt','licenses/CC-BY-SA-3.0.txt','licenses/CC-BY-SA-2.5.txt','licenses/tnm-MIT.txt','licenses/GeneralUser-GS.txt','NOTICES.txt']]

class VerificationTests(unittest.TestCase):
    def test_preview_identity_is_explicit_and_preserves_main_app(self):
        preview=ET.fromstring(MANIFEST.replace('org.example.kinderwelt','org.example.kinderwelt.preview.family.v073'))
        with self.assertRaises(AssertionError):v.check_manifest(preview)
        self.assertEqual(v.check_manifest(preview,'org.example.kinderwelt.preview.family.v073')['package'],'org.example.kinderwelt.preview.family.v073')
    def test_valid_manifest(self):self.assertEqual(v.check_manifest(ET.fromstring(MANIFEST))['permissions'],[])
    def test_permission_rejected(self):
        root=ET.fromstring(MANIFEST);ET.SubElement(root,'uses-permission',{v.ANDROID+'name':'android.permission.INTERNET'})
        with self.assertRaises(AssertionError):v.check_manifest(root)
    def test_identity_version_sdk_backup_rotation_drift_rejected(self):
        for before,after in [('org.example.kinderwelt','org.wrong.app'),('versionCode="10"','versionCode="99"'),('targetSdkVersion="36"','targetSdkVersion="35"'),('allowBackup="false"','allowBackup="true"'),('fullUser','portrait'),('extractNativeLibs="true"','extractNativeLibs="false"')]:
            with self.subTest(before=before),self.assertRaises(AssertionError):v.check_manifest(ET.fromstring(MANIFEST.replace(before,after)))
    def test_valid_payload(self):self.assertEqual(v.check_payload(PAYLOAD),len(PAYLOAD))
    def test_development_and_key_files_rejected(self):
        for name in ['assets/addons/gut/test.gdc','assets/tests/smoke.gdc','assets/private.jks','assets/release.yaml','assets/docs/study.txt']:
            with self.subTest(name=name),self.assertRaises(AssertionError):v.check_payload(PAYLOAD+[name])
    def test_missing_modules_rejected(self):
        with self.assertRaises(AssertionError):v.check_payload([n for n in PAYLOAD if n!="assets/games/quest/tasks.json"])
    def test_replaced_character_artwork_rejected(self):
        for name in ['mina','leo','sam','jule']:
            with self.subTest(name=name),self.assertRaises(AssertionError):v.check_payload(PAYLOAD+['assets/assets/quest/'+name+'.png.import'])
    def test_missing_music_payload_rejected(self):
        with self.assertRaises(AssertionError):v.check_payload([n for n in PAYLOAD if n!="assets/.godot/imported/babbino.ogg-fixture.oggvorbisstr"])
    def test_every_resource_category_and_family_character_is_checked(self):
        for required in [p for p in PAYLOAD if 'voice_' not in p]+[next(p for p in PAYLOAD if 'voice_'+locale+'_' in p and p.endswith(ext)) for locale in ['de','en','ru'] for ext in ['.import','.oggvorbisstr']]:
            with self.subTest(required=required),self.assertRaises(AssertionError):v.check_payload([p for p in PAYLOAD if p!=required])
    def data_archive(self,prefix='assets/',change=None):
        memory=io.BytesIO()
        root=Path(__file__).resolve().parents[2]
        files=['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/quest/cast.json','assets/music/manifest.json']
        files += ['assets/voice/quest/'+locale+'/'+name for locale in ['de','en','ru'] for name in ['manifest.json','MODEL_CARD.txt']]
        with zipfile.ZipFile(memory,'w') as archive:
            for name in files:
                if change=='missing' and name==files[0]:continue
                data=(root/name).read_bytes()
                if change=='modified' and name==files[0]:data=b'{"tasks":[]}'
                archive.writestr(prefix+name,data)
            if change=='duplicate':archive.writestr('unexpected/assets/'+files[0],(root/files[0]).read_bytes())
        memory.seek(0)
        return zipfile.ZipFile(memory)
    def test_content_integrity_supports_apk_base_and_install_time_aab_assets(self):
        for prefix in ['assets/','base/assets/','assetPackInstallTime/assets/']:
            with self.subTest(prefix=prefix),self.data_archive(prefix) as archive:v.check_packaged_data(archive)
    def test_changed_missing_or_duplicate_data_is_rejected(self):
        for change in ['modified','missing','duplicate']:
            with self.subTest(change=change),self.data_archive(change=change) as archive,self.assertRaises(AssertionError):v.check_packaged_data(archive)
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
