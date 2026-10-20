#!/usr/bin/env python3
"""Linux x86_64 toolchain. Requires explicit Android SDK licence acceptance."""
import argparse, hashlib, json, os, shutil, subprocess, tarfile, tempfile, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
LOCK=json.loads((HERE/'toolchain.json').read_text())

def fetch(url, path, digest, algorithm='sha256'):
    if not path.exists() or hashlib.new(algorithm,path.read_bytes()).hexdigest()!=digest:
        subprocess.run(['curl','--fail','--location','--retry','3',url,'-o',str(path)],check=True)
    if hashlib.new(algorithm,path.read_bytes()).hexdigest()!=digest:
        raise ValueError('Checksum mismatch: '+path.name)
    return path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path('/workspace/tools'))
    parser.add_argument('--accept-android-sdk-license',action='store_true')
    args=parser.parse_args()
    if not args.accept_android_sdk_license:
        parser.error('Read https://developer.android.com/studio/terms and explicitly accept with --accept-android-sdk-license')
    root=args.root.resolve();root.mkdir(parents=True,exist_ok=True)
    cache=root/'android-downloads';cache.mkdir(exist_ok=True)
    sdk=root/'android-sdk'
    for a in LOCK['sdk_archives']:
        archive=fetch(a['url'],cache/(a['name']+'.zip'),a['sha256'])
        with tempfile.TemporaryDirectory() as temp:
            with zipfile.ZipFile(archive) as z:z.extractall(temp)
            source=next(Path(temp).iterdir());dest=sdk/a['destination']
            shutil.copytree(source,dest,dirs_exist_ok=True)
            for f in dest.rglob('*'):
                if f.is_file() and f.suffix in ['', '.sh']:f.chmod(f.stat().st_mode|0o111)
    # Android SDK licence hash published by Google; no credentials involved.
    (sdk/'licenses').mkdir(exist_ok=True)
    (sdk/'licenses/android-sdk-license').write_text('8933bad161af4178b1185d1a37fbf41ea5269c55\nd56f5187479451eabf01fb78af6dfcb131a6481e\n24333f8a63b6825ea9c5514f83c2829b004d1fee\n')
    jdk=fetch(LOCK['jdk_url'],cache/'jdk.tar.gz',LOCK['jdk_sha256'])
    with tempfile.TemporaryDirectory() as temp:
        with tarfile.open(jdk) as archive:archive.extractall(temp,filter='data')
        if (root/'android-jdk').exists():shutil.rmtree(root/'android-jdk')
        shutil.copytree(next(Path(temp).iterdir()),root/'android-jdk',symlinks=True)
    tools=root/'android-tools';tools.mkdir(exist_ok=True)
    fetch('https://github.com/google/bundletool/releases/download/1.18.2/bundletool-all-1.18.2.jar',tools/'bundletool-1.18.2.jar',LOCK['bundletool_sha256'])
    template=fetch('https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz',cache/'templates.tpz',LOCK['templates_sha512'],'sha512')
    templates=tools/'templates';templates.mkdir(exist_ok=True)
    with zipfile.ZipFile(template) as z:
        for name in ['android_debug.apk','android_release.apk','android_source.zip','version.txt']:
            (templates/name).write_bytes(z.read('templates/'+name))
    subprocess.run([str(root/'android-jdk/bin/java'),'-version'],check=True)
    subprocess.run([str(sdk/'build-tools/36.1.0/aapt2'),'version'],check=True)
    assert '37.0.1' in (sdk/'platform-tools/source.properties').read_text()
    print('Verified toolchain installed in',root)

if __name__=='__main__':main()
