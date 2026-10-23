#!/usr/bin/env python3
"""Build separately installable family/neutral APKs and unsigned AABs, without duplicates."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
VARIANTS={'family':'family','neutral':'public'}
def collect(directory,label):
    result={}
    pending=[]
    proof=json.loads((directory/'provenance.json').read_text())
    if proof['variant']!=VARIANTS[label]:raise ValueError('Verified cast variant does not match delivery name')
    for original,named in [('kinderwelt-debug.apk',f'kinderwelt-debug-{label}.apk'),('kinderwelt-unsigned.aab',f'kinderwelt-unsigned-{label}.aab')]:
        source=directory/original;expected=proof['artifacts'][original]
        if source.stat().st_size!=expected['bytes'] or hashlib.sha256(source.read_bytes()).hexdigest()!=expected['sha256']:raise ValueError('Artifact differs from verified build: '+original)
        target=directory.parent/named
        if target.exists():raise ValueError('Refusing stale delivery artifact: '+named)
        pending.append((source,target))
        result[named]={'variant':label,'package':proof['package'],'version_name':proof['version_name'],'version_code':proof['version_code'],**expected,'application_source_sha256':proof['application_source_sha256'],'signing':'cached development-only certificate' if target.suffix=='.apk' else 'UNSIGNED'}
    for source,target in pending:source.rename(target)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'build/android-delivery');p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));p.add_argument('--variants',choices=VARIANTS,nargs='+',default=['family','neutral']);a=p.parse_args()
    if len(set(a.variants))!=len(a.variants):p.error('Duplicate variants are not allowed')
    out=a.output.resolve()
    if out.exists():p.error('Output must be a new directory')
    if 'family' in a.variants and not (ROOT/'.private/characters/looks.json').is_file():p.error('Family artwork is missing; restore the pinned private illustration repository first. No neutral substitute is used.')
    out.mkdir(parents=True);artifacts={}
    for label in a.variants:
        destination=out/label
        subprocess.run([sys.executable,str(ROOT/'scripts/android/build.py'),'--tools',str(a.tools.resolve()),'--variant',VARIANTS[label],'--preview','--output',str(destination)],check=True)
        artifacts.update(collect(destination,label))
    packages={value['package'] for name,value in artifacts.items() if name.endswith('.apk')}
    if len(packages)!=len(a.variants):raise ValueError('Variant packages must be separately installable')
    (out/'delivery.json').write_text(json.dumps({'schema':1,'variants':a.variants,'artifacts':artifacts,'release_signing':'NOT CONFIGURED; unsigned AABs; Play readiness BLOCKED'},indent=2)+'\n')
    print('Verified delivery: '+', '.join(name for name in artifacts if name.endswith('.apk')))
if __name__=='__main__':main()
