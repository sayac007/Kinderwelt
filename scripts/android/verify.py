#!/usr/bin/env python3
"""Fail closed on Android identity, permissions, packaging and signing drift."""
import sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
import identity
import backup_policy
import upload_signing
import argparse, hashlib, json, re, struct, subprocess, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ANDROID='{http://schemas.android.com/apk/res/android}'
PACKAGE=identity.CONFIG['test_package']
VERSION=identity.CONFIG['version_name']
CODE=identity.CONFIG['version_code']

def command(args):
    # Java writes JAVA_TOOL_OPTIONS notices to stderr. They are diagnostics,
    # not part of bundletool's XML/JSON stdout, even on a successful command.
    return subprocess.check_output([str(x) for x in args],stderr=subprocess.PIPE,text=True)

def check_manifest(root,package=PACKAGE):
    identity.validate_package(package)
    assert root.get('package')==package,'Unexpected package'
    assert root.get(ANDROID+'versionCode')==str(CODE),'Unexpected version code'
    assert root.get(ANDROID+'versionName')==VERSION,'Unexpected version name'
    sdk=root.find('uses-sdk')
    assert sdk is not None and sdk.get(ANDROID+'minSdkVersion')=='24' and sdk.get(ANDROID+'targetSdkVersion')=='36','SDK mismatch'
    assert not root.findall('uses-permission') and not root.findall('uses-permission-sdk-23'),'Unexpected Android permission'
    app=root.find('application');assert app is not None
    assert app.get(ANDROID+'allowBackup')=='false','Backup must be disabled'
    assert all(app.get(ANDROID+name) for name in backup_policy.FILES),'Missing explicit cloud/device-transfer backup exclusions'
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
    return {'package':package,'version_name':VERSION,'version_code':CODE,'min_sdk':24,'target_sdk':36,'permissions':[],'allow_backup':False,'orientation':'fullUser'}

def check_payload(names,app_root=None):
    app_root=Path(app_root) if app_root else Path(__file__).resolve().parents[2]
    assets={n.split('assets/',1)[1] for n in names if 'assets/' in n and not n.endswith('/')}
    assert 'games/quest/legacy-rewards.json' in assets,'Missing first-round lifetime reward migration registry'
    imported={n.split('/')[-1].rsplit('-',1)[0] for n in assets if n.startswith('.godot/imported/') and n.endswith('.oggvorbisstr')}
    assert any(n.endswith('project.binary') for n in assets),'Missing Godot project'
    for n in assets:
        assert not re.search(r'(^|/)(art|tests|scripts|docs|addons|qa-results|android|build)(/|$)',n),'Development files packaged: '+n
        assert not n.endswith(('.keystore','.jks','.p12','.pem','.yaml','.safetensors','.onnx','.pth','.pt')),'Sensitive, specification or development model file packaged'
    required=['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/quest/cast.json','assets/music/manifest.json','assets/quest/Nunito.ttf.import','assets/quest/landscape.png.import','assets/quest/icons.png.import','assets/quest/objects.png.import','assets/quest/appicon.png.import']
    for item in required: assert item in assets,'Missing quest asset: '+item
    for notice in ['assets/quest/OFL.txt','assets/music/licenses/CC-BY-SA-4.0.txt','assets/music/licenses/CC-BY-3.0.txt','assets/music/licenses/CC-BY-SA-3.0.txt','assets/music/licenses/CC-BY-SA-2.5.txt','assets/music/licenses/tnm-MIT.txt','assets/music/licenses/GeneralUser-GS.txt','assets/music/NOTICES.txt']:
        assert notice in assets,'Missing bundled notice: '+notice
    for image in ['landscape','icons','objects','appicon','science-a','science-b','home','castle','adventure-worlds','cap','beanie']:
        assert 'assets/quest/'+image+'.png.import' in assets,'Missing image import: '+image
        assert any(n.startswith('.godot/imported/'+image+'.png-') and n.endswith('.ctex') for n in assets),'Missing actual image texture: '+image
    assert any(n.startswith('.godot/imported/Nunito.ttf-') and n.endswith('.fontdata') for n in assets),'Missing actual font resource'
    for script in ['game','world','world_props','vehicle','task','picture','progress','choice']:
        assert any(n.startswith('games/quest/'+script+'.gd') for n in assets),'Missing quest runtime: '+script
    for script in ['core/quest/score_badge.gd','core/quest/scenery.gd','core/quest/scenery_card.gd','core/mobile.gd','core/quest/wardrobe.gd','core/quest/letter_slots.gd','core/quest/custom_avatar.gd','core/quest/avatar_import.gd','core/quest/avatar_preview.gd']:
        assert any(n.startswith(script) for n in assets),'Missing score or adaptive screen layout: '+script
    assert any(n.startswith('core/quest/main.gd') for n in assets),'Missing application entry'
    cast=json.loads((app_root/'assets/quest/cast.json').read_text())
    for path in set(cast['sprites'].values())|set(cast['atlases'].values()):
        if path.endswith('.png'):
            image=Path(path).name
            assert path+'.import' in assets,'Missing cast import: '+path
            assert any(n.startswith('.godot/imported/'+image+'-') and n.endswith('.ctex') for n in assets),'Missing cast texture: '+path
        else:
            assert any(n==path or n.startswith(path+'.') for n in assets),'Missing cast frame: '+path
    if cast['variant']=='public':
        assert not any(re.search(r'(?:actor|outfits)-[1-6]\.png',n) for n in assets),'Private cast resource in public package'
    for track in [t['id'] for t in json.loads((Path(__file__).resolve().parents[2]/'scripts/music/catalog.json').read_text())['tracks']]:
        ext='.ogg'
        assert 'assets/music/'+track+ext+'.import' in assets,'Missing music import: '+track
        assert any(n.startswith('.godot/imported/'+track+ext+'-') and n.endswith('.sample' if ext=='.wav' else '.oggvorbisstr') for n in assets),'Missing playable music: '+track
    for locale in ['de','en','ru']:
        folder='assets/voice/quest/'+locale+'/'
        for filename in ['manifest.json','MODEL_CARD.txt']:
            assert folder+filename in assets,'Missing localized speech metadata: '+locale+'/'+filename
        manifest=json.loads((Path(__file__).resolve().parents[2]/folder/'manifest.json').read_text())
        if manifest.get('model_license')=='Apache-2.0':assert folder+'LICENSE.txt' in assets,'Missing multilingual voice notice: '+locale
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

def check_packaged_data(archive,app_root=None):
    """Godot uses an install-time asset pack in AABs, ordinary assets in APKs."""
    app_root=Path(app_root) if app_root else Path(__file__).resolve().parents[2]
    data_files=['games/quest/tasks.json','games/quest/languages.json','assets/quest/looks.json','assets/quest/cast.json','assets/music/manifest.json']
    data_files += ['games/quest/legacy-rewards.json','assets/quest/appicon.png']
    data_files += ['assets/voice/quest/'+locale+'/'+name for locale in ['de','en','ru'] for name in ['manifest.json','MODEL_CARD.txt']]
    for locale in ['de','ru']:
        folder='assets/voice/quest/'+locale+'/'
        manifest=json.loads((app_root/folder/'manifest.json').read_text())
        if manifest.get('model_license')=='Apache-2.0':data_files.append(folder+'LICENSE.txt')
    for name in data_files:
        candidates=[n for n in archive.namelist() if 'assets/' in n and n.split('assets/',1)[1]==name]
        assert len(candidates)==1,'Missing or duplicate packaged content: '+name
        assert archive.read(candidates[0])==(app_root/name).read_bytes(),'Packaged content differs from tested source: '+name

def check_launcher_images(archive,app_root=None,aab=False):
    """Decode the actual Android launcher/splash resources, not just game assets.

    Godot and AAPT resize/re-encode these. A small pixel tolerance allows their
    resampler differences while rejecting a stale or substituted illustration.
    FFmpeg is already required for the delivered speech verification.
    """
    app_root=Path(app_root) if app_root else Path(__file__).resolve().parents[2]
    def pixels(data):
        args=['ffmpeg','-nostdin','-v','error','-threads','1','-filter_threads','1','-i','pipe:0',
              '-vf','scale=192:192:flags=lanczos','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-']
        try:result=subprocess.check_output(args,input=data,stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:raise AssertionError('Cannot decode Android icon') from error
        assert len(result)==192*192*3,'Invalid decoded icon size'
        return result
    expected=pixels((app_root/'assets/quest/appicon.png').read_bytes())
    result={};prefix='base/' if aab else ''
    for resource in ['res/mipmap-xxxhdpi-v4/icon.webp','res/mipmap-xxxhdpi-v4/icon_foreground.webp','res/drawable/splash_icon.webp']:
        name=prefix+resource
        assert name in archive.namelist(),'Missing Android launcher/splash image: '+name
        data=archive.read(name)
        assert data[:4]==b'RIFF' and data[8:12]==b'WEBP','Invalid Android WebP image: '+name
        actual=pixels(data)
        error=sum(abs(a-b) for a,b in zip(actual,expected))/len(expected)
        assert error<12,'Android launcher/splash differs from approved generated icon: '+name
        result[resource]={'normalized_rgb_mean_absolute_error':round(error,4),'status':'PASS'}
    return result

def inspect_zip(path,aab=False,app_root=None,signed=False):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None,'Corrupt ZIP'
        names=z.namelist();assert len(names)==len(set(names)),'Duplicate ZIP entries'
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'Unsafe archive path'
        assert ('BundleConfig.pb' in names and 'base/manifest/AndroidManifest.xml' in names) if aab else 'AndroidManifest.xml' in names
        if aab:
            has_signature=any(re.match(r'META-INF/[^/]+\.(RSA|DSA|EC|SF)$',n,re.I) for n in names)
            assert has_signature==signed,'Expected signed AAB' if signed else 'Expected unsigned AAB'
        check_packaged_data(z,app_root)
        icons=check_launcher_images(z,app_root,aab)
        abis=set();native_methods=set()
        for n in names:
            if n.endswith('.so'):
                abis.add(n.split('/')[-2]);elf_alignment(z.read(n));native_methods.add(z.getinfo(n).compress_type)
        assert abis=={'arm64-v8a','x86_64'},'Unexpected native ABI set'
        assert native_methods=={zipfile.ZIP_DEFLATED},'Expected lossless native library compression'
        return {'assets_checked':check_payload(names,app_root),'launcher_images':icons,'abis':sorted(abis),'elf_16kb_alignment':'PASS','native_packaging':'deflated; extracted by Android on installation'}

def verify_bundle(aab,tools,out,source,package,signed=False,certificate=None):
    java=tools/'android-jdk/bin/java';bundle=tools/'android-tools/bundletool-1.18.2.jar'
    validation=command([java,'-jar',bundle,'validate','--bundle='+str(aab)])
    (out/'aab-validation.txt').write_text(validation)
    manifest=command([java,'-jar',bundle,'dump','manifest','--bundle='+str(aab),'--module=base'])
    (out/'aab-manifest.xml').write_text(manifest)
    root=ET.fromstring(manifest)
    data=inspect_zip(aab,True,app_root=source,signed=signed)
    data.update(check_manifest(root,package))
    rendering=root.find('application/meta-data[@'+ANDROID+'name="org.godotengine.rendering.method"]')
    assert rendering is not None and rendering.get(ANDROID+'value')=='gl_compatibility','Unexpected Android rendering backend'
    data['rendering']='gl_compatibility'
    if signed:
        identity.validate_release_package(package)
        data.update(upload_signing.verify(aab,tools/'android-jdk',certificate))
        (out/'aab-signature.txt').write_text('Every payload entry verified against the expected upload certificate; certificate validity checked.\n')
    else:
        signing=command([tools/'android-jdk/bin/jarsigner','-verify',aab])
        assert 'jar is unsigned' in signing,'Expected unsigned bundle'
        data['signature']='UNSIGNED'
        (out/'aab-signature.txt').write_text(signing)
    return data

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));p.add_argument('--output',type=Path,required=True);p.add_argument('--package',type=identity.validate_package,default=PACKAGE);p.add_argument('--release',action='store_true');p.add_argument('--upload-certificate-sha256');a=p.parse_args()
    tools=a.tools;out=a.output;bt=tools/'android-sdk/build-tools/36.1.0';java=tools/'android-jdk/bin/java';bundle=tools/'android-tools/bundletool-1.18.2.jar'
    report={'status':'PASS','upload_readiness':'BLOCKED','artifacts':{}}
    apk=out/'kinderwelt-debug.apk';aab=out/('kinderwelt-release-neutral.aab' if a.release else 'kinderwelt-unsigned.aab')
    if a.release:
        data=verify_bundle(aab,tools,out,a.source,a.package,True,a.upload_certificate_sha256)
        data.update({'bytes':aab.stat().st_size,'sha256':hashlib.sha256(aab.read_bytes()).hexdigest()})
        report['artifacts'][aab.name]=data
        (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
        return
    apk_data=inspect_zip(apk,app_root=a.source)
    badging=command([bt/'aapt2','dump','badging',apk]);(out/'apk-badging.txt').write_text(badging)
    for pattern in [rf"package: name='{re.escape(a.package)}' versionCode='{CODE}' versionName='{re.escape(VERSION)}'",r"minSdkVersion:'24'",r"targetSdkVersion:'36'"]:
        assert re.search(pattern,badging),'APK manifest mismatch'
    permissions=command([bt/'aapt2','dump','permissions',apk]);assert 'uses-permission' not in permissions,'Unexpected APK permissions'
    xmltree=command([bt/'aapt2','dump','xmltree',apk,'--file','AndroidManifest.xml']);(out/'apk-manifest.txt').write_text(xmltree)
    assert re.search(r'android:extractNativeLibs[^\n]*=true\b',xmltree),'Compressed native libraries must be extracted'
    assert re.search(r'android:allowBackup[^\n]*=false\b',xmltree),'APK backup enabled'
    apk_data['backup_policy']=backup_policy.verify_apk(bt/'aapt2',apk,xmltree)
    assert re.search(r'android:screenOrientation[^\n]*=13\b',xmltree),'APK orientation mismatch'
    signature=command([bt/'apksigner','verify','--verbose','--print-certs',apk]);(out/'apk-signature.txt').write_text(signature)
    assert 'CN=Godot' in signature and 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature,'Unexpected development signature'
    provenance=json.loads((out/'provenance.json').read_text())
    expected_certificate=provenance['signing']['development_certificate_sha256']
    assert re.search(r'Signer #1 certificate SHA-256 digest: '+re.escape(expected_certificate),signature,re.I),'APK signer differs from reused development key'
    command([bt/'zipalign','-c','-P','16','-v','4',apk])
    apk_data.update({'package':a.package,'version_name':VERSION,'version_code':CODE,'min_sdk':24,'target_sdk':36,'permissions':[],'allow_backup':False,'orientation':'fullUser','signature':'verified Godot development certificate, v2','certificate_sha256':expected_certificate,'zip_16kb_alignment':'PASS'})
    aab_data=verify_bundle(aab,tools,out,a.source,a.package)
    for file,data in [(apk,apk_data),(aab,aab_data)]:
        data.update({'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()});report['artifacts'][file.name]=data
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':
    try:
        main()
    except (AssertionError, ValueError) as error:
        message=str(error).replace('%','%25').replace('\r','%0D').replace('\n','%0A')
        print('::error::Android artifact verification failed: '+message,flush=True)
        raise
