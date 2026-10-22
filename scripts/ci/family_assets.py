#!/usr/bin/env python3
"""Verify/import AI family illustrations from a separately pinned private repository."""
import argparse,hashlib,json,os,re,shutil,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
IDS=('wanja','mischa','du','mama','george','katze')
FILES={id+'.png' for id in IDS}|{'looks-'+id+'.png' for id in IDS}|{'looks.json','names.json'}
MAX_BYTES=64*1024*1024

def plan(config):
    data=json.loads(config.read_text())
    if data.get('schema')!=1 or not re.fullmatch(r'[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+',data.get('repository','')):raise ValueError('Invalid private asset repository configuration')
    if not re.fullmatch(r'[a-f0-9]{40}',data.get('revision','')) or not re.fullmatch(r'[a-f0-9]{64}',data.get('manifest_sha256','')):raise ValueError('Asset revision and manifest hash must be explicitly pinned')
    if data.get('visibility_required','private')!='private':raise ValueError('Family assets must remain in a private repository')
    return data

def validate(files):
    if set(files)!=FILES:raise ValueError('Expected exactly 12 derived PNGs and two catalogues; source photos are not accepted')
    if sum(map(len,files.values()))>MAX_BYTES:raise ValueError('Family assets exceed the size limit')
    names=json.loads(files['names.json']);looks=json.loads(files['looks.json'])
    if set(names)!=set(IDS) or not all(isinstance(n,str) and 0<len(n)<=64 for n in names.values()):raise ValueError('Invalid stable family name IDs')
    if not set(IDS).issubset(looks['heroes']) or set(looks['heroes'])-set(IDS)-{'squirrel'}:raise ValueError('Incomplete family costume catalogue')
    for name,data in files.items():
        if len(data)>16*1024*1024:raise ValueError('Oversized family source: '+name)
        if name.endswith('.png') and not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid derived PNG: '+name)
    for id in IDS:
        if hashlib.sha256(files['looks-'+id+'.png']).hexdigest()!=looks['heroes'][id]['sha256']:raise ValueError('Costume hash mismatch: '+id)

def restore(source,destination,expected_manifest):
    if destination.exists():raise ValueError('Refusing to overwrite an existing family source pack')
    manifest=source/'manifest.json'
    if manifest.is_symlink() or manifest.stat().st_size>1024*1024:raise ValueError('Invalid private asset manifest')
    raw=manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_manifest:raise ValueError('Private asset manifest differs from the pinned revision')
    data=json.loads(raw)
    if data.get('schema')!=1 or set(data.get('files',{}))!=FILES:raise ValueError('Unexpected private asset manifest files')
    folder=source/'characters'
    if folder.is_symlink() or {p.name for p in folder.iterdir()}!=FILES:raise ValueError('Unexpected family source paths; photos and extra files are not accepted')
    files={}
    for name,metadata in data['files'].items():
        path=folder/name
        if path.is_symlink() or not path.is_file() or path.stat().st_size>16*1024*1024:raise ValueError('Unsafe family source: '+name)
        value=path.read_bytes()
        if len(value)!=metadata['bytes'] or hashlib.sha256(value).hexdigest()!=metadata['sha256']:raise ValueError('Family source hash mismatch: '+name)
        files[name]=value
    validate(files)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.family-stage-',dir=destination.parent) as temp:
        stage=Path(temp)/'characters';stage.mkdir(mode=0o700)
        for name,value in files.items():
            p=stage/name;p.write_bytes(value);p.chmod(0o600)
        stage.rename(destination)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['plan','restore']);p.add_argument('--config',type=Path,default=ROOT/'scripts/ci/family-assets.json');p.add_argument('--source',type=Path,default=ROOT/'.private/family-assets');p.add_argument('--output',type=Path,default=ROOT/'.private/characters');a=p.parse_args()
    try:
        config=plan(a.config)
        if a.command=='plan':
            lines='repository='+config['repository']+'\nrevision='+config['revision']+'\n'
            if os.environ.get('GITHUB_OUTPUT'):
                with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write(lines)
            else:print(lines,end='')
        else:
            restore(a.source,a.output,config['manifest_sha256'])
            print('Verified 14 derived family asset files; no original photos or credentials imported')
    except (ValueError,KeyError,FileNotFoundError) as e:
        print('Private family assets: '+str(e),file=sys.stderr);raise SystemExit(1)
if __name__=='__main__':main()
