#!/usr/bin/env python3
"""Report actual ZIP sizes, categorization, ABI and compression without editing artifacts."""
import argparse,collections,hashlib,json,zipfile
from pathlib import Path

def analyze(path):
    groups=collections.defaultdict(lambda:{'raw_bytes':0,'stored_bytes':0,'files':0})
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None,'Corrupt artifact'
        entries=z.infolist()
        for entry in entries:
            n=entry.filename
            category=('native/'+n.split('/')[-2] if n.endswith('.so') else
                      'audio' if n.endswith(('.sample','.ogg','.wav')) else
                      'fonts' if n.endswith(('.ttf','.otf','.woff','.woff2')) else
                      'graphics' if n.endswith(('.ctex','.png','.webp','.svg')) else
                      'application/imports/other' if 'assets/' in n else 'Android/metadata/classes')
            g=groups[category];g['raw_bytes']+=entry.file_size;g['stored_bytes']+=entry.compress_size;g['files']+=1
        largest=[{'file':e.filename,'raw_bytes':e.file_size,'stored_bytes':e.compress_size,'zip_method':e.compress_type,**({'raw_sha256':hashlib.sha256(z.read(e)).hexdigest()} if e.filename.endswith('.so') else {})} for e in sorted(entries,key=lambda e:e.compress_size,reverse=True)[:20]]
    payload=sum(g['stored_bytes'] for g in groups.values())
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'groups':dict(groups),'zip_alignment_signing_overhead_bytes':path.stat().st_size-payload,'largest':largest,'note':'APK/AAB archive bytes, not installed footprint or measured Play device download'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('files',nargs='+',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.write_text(json.dumps({'artifacts':[analyze(f) for f in a.files]},indent=2)+'\n')
