#!/usr/bin/env python3
"""Checksum-pinned CI decoder fallback, independent of system package mirrors."""
import argparse,hashlib,json,os,platform,shutil,subprocess,tempfile,time,urllib.request,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(data):return hashlib.sha256(data).hexdigest()
def download(url,path):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=25) as source,path.open('wb') as target:shutil.copyfileobj(source,target)
            return
        except OSError:
            if attempt==2:raise
            time.sleep(1)
def install(config,destination,archive=None):
    destination=Path(destination);exe=destination/'ffmpeg'
    if exe.is_file() and digest(exe.read_bytes())==config['binary_sha256'] and all((destination/n).is_file() for n in ['IMAGEIO-LICENSE.txt','FFMPEG-COPYING.txt']):return exe
    with tempfile.TemporaryDirectory(prefix='kinderwelt-decoder-') as d:
        wheel=Path(archive) if archive else Path(d)/'decoder.whl'
        if not archive:download(config['url'],wheel)
        if digest(wheel.read_bytes())!=config['sha256']:raise ValueError('Decoder archive SHA-256 mismatch; nothing installed')
        with zipfile.ZipFile(wheel) as z:
            binary=z.read(config['binary']);notice=z.read(config['notice'])
        if digest(binary)!=config['binary_sha256']:raise ValueError('Decoder binary SHA-256 mismatch; nothing installed')
        destination.mkdir(parents=True,exist_ok=True)
        (destination/'IMAGEIO-LICENSE.txt').write_bytes(notice)
        shutil.copy2(HERE/'licenses/FFmpeg-GPL-3.txt',destination/'FFMPEG-COPYING.txt')
        temporary=destination/'ffmpeg.tmp';temporary.write_bytes(binary);temporary.chmod(0o755);temporary.replace(exe)
    return exe
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',type=Path,required=True);p.add_argument('--archive',type=Path);a=p.parse_args()
    if platform.system()!='Linux' or platform.machine() not in ['x86_64','AMD64']:p.error('Pinned decoder supports Linux x86_64 only')
    config=json.loads((HERE/'audio-decoder-source.json').read_text());exe=install(config,a.destination.resolve(),a.archive)
    result=subprocess.run([str(exe),'-version'],capture_output=True,text=True,timeout=10,check=True)
    if not result.stdout.startswith(config['version_prefix']):raise ValueError('Unexpected decoder version')
    print(result.stdout.splitlines()[0]);print('Verified development decoder:',exe)
    if os.environ.get('GITHUB_PATH'):
        with Path(os.environ['GITHUB_PATH']).open('a') as path:path.write(str(exe.parent)+'\n')
if __name__=='__main__':main()
