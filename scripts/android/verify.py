#!/usr/bin/env python3
"""Fail closed on Android identity, permissions, packaging and signing drift."""
import argparse, hashlib, json, re, struct, subprocess, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ANDROID='{http://schemas.android.com/apk/res/android}'
PACKAGE='org.example.kinderwelt'

def command(args):
    return subprocess.check_output([str(x) for x in args],stderr=subprocess.STDOUT,text=True)

def check_manifest(root,package=PACKAGE):
    assert root.get('package')==package,'Unexpected package'
    assert root.get(ANDROID+'versionCode')=='7','Unexpected version code'
    assert root.get(ANDROID+'versionName')=='0.7.0','Unexpected version name'
    sdk=root.find('uses-sdk')
    assert sdk is not None and sdk.get(ANDROID+'minSdkVersion')=='24' and sdk.get(ANDROID+'targetSdkVersion')=='36','SDK mismatch'
    assert not root.findall('uses-permission') and not root.findall('uses-permission-sdk-23'),'Unexpected Android permission'
    app=root.find('application');assert app is not None
    assert app.get(ANDROID+'allowBackup')=='false','Backup must be disabled'
    assert app.get(ANDROID+'extractNativeLibs')=='true','Compressed libraries must be extracted'
    assert app.get(ANDROID+'debuggable','false')=='false','Release bundle must not be debuggable'
    launcher=[a for a in list(app.findall('activity'))+list(app.findall('activity-alias')) if a.find('intent-filter/category[@'+ANDROID+'name="android.intent.category.LAUNCHER"]') is not None]
    assert len(launcher)==1,'Missing launcher'
    activity=launcher[0]
    if activity.tag=='activity-alias':
        targets=[a for a in app.findall('activity') if a.get(ANDROID+'name')==activity.get(ANDROID+'targetActivity')]
        assert len(targets)==1,'Invalid launcher target'
        activity=targets[0]
    assert activity.get(ANDROID+'screenOrientation') in {'13','fullUser'},'Expected deliberate portrait and landscape rotation'
    return {'package':package,'version_name':'0.7.0','version_code':7,'min_sdk':24,'target_sdk':36,'permissions':[],'allow_backup':False,'orientation':'fullUser'}

def check_payload(names):
    assets={n.split('assets/',1)[1] for n in names if 'assets/' in n and not n.endswith('/')}
    imported={n.split('/')[-1].rsplit('-',1)[0] for n in assets if n.startswith('.godot/imported/') and n.endswith('.oggvorbisstr')}
    assert any(n.endswith('project.binary') for n in assets),'Missing Godot project'
    for n in assets:
        assert not re.search(r'(^|/)(tests|scripts|docs|addons|qa-results|android|build)(/|$)',n),'Development files packaged: '+n
        assert not n.endswith(('.keystore','.jks','.p12','.pem','.yaml')),'Sensitive or specification file packaged'
    required=['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/music/manifest.json','assets/quest/Nunito.ttf.import','assets/quest/landscape.png.import','assets/quest/icons.png.import','assets/quest/objects.png.import','assets/quest/appicon.png.import']
    for item in required: assert item in assets,'Missing quest asset: '+item
    for notice in ['assets/quest/OFL.txt','assets/music/licenses/CC-BY-SA-4.0.txt','assets/music/licenses/CC-BY-3.0.txt','assets/music/licenses/CC-BY-SA-3.0.txt','assets/music/licenses/CC-BY-SA-2.5.txt','assets/music/licenses/tnm-MIT.txt','assets/music/licenses/GeneralUser-GS.txt','assets/music/NOTICES.txt']:
        assert notice in assets,'Missing bundled notice: '+notice
    for image in ['landscape','icons','objects','appicon','science-a','science-b','home','castle']:
        assert 'assets/quest/'+image+'.png.import' in assets,'Missing image import: '+image
        assert any(n.startswith('.godot/imported/'+image+'.png-') and n.endswith('.ctex') for n in assets),'Missing actual image texture: '+image
    assert any(n.startswith('.godot/imported/Nunito.ttf-') and n.endswith('.fontdata') for n in assets),'Missing actual font resource'
    for script in ['game','world','task','picture','progress','choice']:
        assert any(n.startswith('games/quest/'+script+'.gd') for n in assets),'Missing quest runtime: '+script
    for script in ['core/quest/score_badge.gd','core/mobile.gd','core/quest/wardrobe.gd']:
        assert any(n.startswith(script) for n in assets),'Missing score or adaptive screen layout: '+script
    assert any(n.startswith('core/quest/main.gd') for n in assets),'Missing application entry'
    for child in ['wanja','mischa','du','mama','katze','george','squirrel']:
        assert 'assets/quest/'+child+'.png.import' in assets,'Missing character: '+child
        assert any(n.startswith('.godot/imported/'+child+'.png-') and n.endswith('.ctex') for n in assets),'Missing character texture: '+child
    for id in ['wanja','mischa','du','mama','katze','george','squirrel']:
        image='looks-'+id
        assert 'assets/quest/'+image+'.png.import' in assets,'Missing wardrobe atlas: '+id
        assert any(n.startswith('.godot/imported/'+image+'.png-') and n.endswith('.ctex') for n in assets),'Missing wardrobe texture: '+id
    for track in [t['id'] for t in json.loads((Path(__file__).resolve().parents[2]/'scripts/music/catalog.json').read_text())['tracks']]:
        ext='.ogg'
        assert 'assets/music/'+track+ext+'.import' in assets,'Missing music import: '+track
        assert any(n.startswith('.godot/imported/'+track+ext+'-') and n.endswith('.sample' if ext=='.wav' else '.oggvorbisstr') for n in assets),'Missing playable music: '+track
    for locale in ['de','en','ru']:
        folder='assets/voice/quest/'+locale+'/'
        for filename in ['manifest.json','MODEL_CARD.txt']:
            assert folder+filename in assets,'Missing localized speech metadata: '+locale+'/'+filename
        manifest=json.loads((Path(__file__).resolve().parents[2]/folder/'manifest.json').read_text())
        for filename in {c['file'] for c in manifest['clips']}:
            assert folder+filename+'.import' in assets,'Missing neural speech: '+locale+'/'+filename
            assert filename in imported,'Missing playable neural speech: '+filename
    assert any(n.startswith('core/quest/language.gd') for n in assets),'Missing localization runtime'
    assert not any(n.startswith(('games/adventure/','games/water/','core/modern/','content/')) for n in assets),'Obsolete runtime packaged'
    assert not any('gut' in n.lower() for n in assets),'Development framework packaged'
    assert not any(any(old+'.png' in n for old in ['mina','leo','sam','jule']) for n in assets),'Replaced character artwork packaged'
    assert any(n.startswith('core/quest/pet.gdshader') for n in assets),'Missing animated cat shader'
    return len(assets)

def elf_alignment(data):
    assert data[:4]==b'\x7fELF' and data[4]==2,'Expected 64-bit ELF'
    offset=struct.unpack_from('<Q',data,32)[0];size,count=struct.unpack_from('<HH',data,54)
    loads=[struct.unpack_from('<IIQQQQQQ',data,offset+i*size) for i in range(count) if struct.unpack_from('<I',data,offset+i*size)[0]==1]
    assert loads and all(p[7]>=16384 and (p[2]-p[3])%16384==0 for p in loads),'ELF not compatible with 16 KB pages'

def check_packaged_data(archive):
    """Godot uses an install-time asset pack in AABs, ordinary assets in APKs."""
    app_root=Path(__file__).resolve().parents[2]
    data_files=['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/music/manifest.json']
    data_files += ['assets/voice/quest/'+locale+'/'+name for locale in ['de','en','ru'] for name in ['manifest.json','MODEL_CARD.txt']]
    for name in data_files:
        candidates=[n for n in archive.namelist() if 'assets/' in n and n.split('assets/',1)[1]==name]
        assert len(candidates)==1,'Missing or duplicate packaged content: '+name
        assert archive.read(candidates[0])==(app_root/name).read_bytes(),'Packaged content differs from tested source: '+name

def inspect_zip(path,aab=False):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None,'Corrupt ZIP'
        names=z.namelist();assert len(names)==len(set(names)),'Duplicate ZIP entries'
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'Unsafe archive path'
        assert ('BundleConfig.pb' in names and 'base/manifest/AndroidManifest.xml' in names) if aab else 'AndroidManifest.xml' in names
        if aab:assert not any(re.match(r'META-INF/[^/]+\.(RSA|DSA|EC|SF)$',n,re.I) for n in names),'Expected unsigned AAB'
        check_packaged_data(z)
        abis=set();native_methods=set()
        for n in names:
            if n.endswith('.so'):
                abis.add(n.split('/')[-2]);elf_alignment(z.read(n));native_methods.add(z.getinfo(n).compress_type)
        assert abis=={'arm64-v8a','x86_64'},'Unexpected native ABI set'
        assert native_methods=={zipfile.ZIP_DEFLATED},'Expected lossless native library compression'
        return {'assets_checked':check_payload(names),'abis':sorted(abis),'elf_16kb_alignment':'PASS','native_packaging':'deflated; extracted by Android on installation'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));p.add_argument('--output',type=Path,required=True);p.add_argument('--package',choices=[PACKAGE,PACKAGE+'.preview.v07'],default=PACKAGE);a=p.parse_args()
    tools=a.tools;out=a.output;bt=tools/'android-sdk/build-tools/36.1.0';java=tools/'android-jdk/bin/java';bundle=tools/'android-tools/bundletool-1.18.2.jar'
    report={'status':'PASS','upload_readiness':'BLOCKED','artifacts':{}}
    apk=out/'kinderwelt-debug.apk';aab=out/'kinderwelt-unsigned.aab'
    apk_data=inspect_zip(apk)
    badging=command([bt/'aapt2','dump','badging',apk]);(out/'apk-badging.txt').write_text(badging)
    for pattern in [rf"package: name='{re.escape(a.package)}' versionCode='7' versionName='0.7.0'",r"minSdkVersion:'24'",r"targetSdkVersion:'36'"]:
        assert re.search(pattern,badging),'APK manifest mismatch'
    permissions=command([bt/'aapt2','dump','permissions',apk]);assert 'uses-permission' not in permissions,'Unexpected APK permissions'
    xmltree=command([bt/'aapt2','dump','xmltree',apk,'--file','AndroidManifest.xml']);(out/'apk-manifest.txt').write_text(xmltree)
    assert re.search(r'android:extractNativeLibs[^\n]*=true\b',xmltree),'Compressed native libraries must be extracted'
    assert re.search(r'android:allowBackup[^\n]*=false\b',xmltree),'APK backup enabled'
    assert re.search(r'android:screenOrientation[^\n]*=13\b',xmltree),'APK orientation mismatch'
    signature=command([bt/'apksigner','verify','--verbose','--print-certs',apk]);(out/'apk-signature.txt').write_text(signature)
    assert 'CN=Godot' in signature and 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature,'Unexpected development signature'
    command([bt/'zipalign','-c','-P','16','-v','4',apk])
    apk_data.update({'package':a.package,'version_name':'0.7.0','version_code':7,'min_sdk':24,'target_sdk':36,'permissions':[],'allow_backup':False,'orientation':'fullUser','signature':'verified Godot development certificate, v2','zip_16kb_alignment':'PASS'})
    validation=command([java,'-jar',bundle,'validate','--bundle='+str(aab)]);(out/'aab-validation.txt').write_text(validation)
    manifest=command([java,'-jar',bundle,'dump','manifest','--bundle='+str(aab),'--module=base']);(out/'aab-manifest.xml').write_text(manifest)
    aab_data=inspect_zip(aab,True);aab_data.update(check_manifest(ET.fromstring(manifest),a.package));aab_data['signature']='UNSIGNED'
    rendering=ET.fromstring(manifest).find('application/meta-data[@'+ANDROID+'name="org.godotengine.rendering.method"]')
    assert rendering is not None and rendering.get(ANDROID+'value')=='gl_compatibility','Unexpected Android rendering backend'
    aab_data['rendering']='gl_compatibility'
    signing=command([tools/'android-jdk/bin/jarsigner','-verify',aab]);assert 'jar is unsigned' in signing,'Expected unsigned bundle'
    (out/'aab-signature.txt').write_text(signing)
    for file,data in [(apk,apk_data),(aab,aab_data)]:
        data.update({'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()});report['artifacts'][file.name]=data
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
