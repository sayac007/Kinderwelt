#!/usr/bin/env python3
"""One-way authoring optimization; retain a private original backup first.

Pillow Lanczos resampling, RGBA, no palette quantization. Metadata must be
recompiled afterwards with compile_wardrobe.py family. Already-sized inputs
are not resampled. No private asset is written into a tracked source path.
"""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def main():
    targets={}
    for p in (ROOT/'.private/characters').glob('*.png'):
        targets[p]=(768,1152) if p.name.startswith('looks-') else (512,768)
    targets[ROOT/'assets/quest/squirrel.png']=(640,768)
    targets[ROOT/'assets/quest/looks-squirrel.png']=(768,1152)
    targets[ROOT/'assets/quest/appicon.png']=(512,512)
    for name in ['landscape','home','castle']:targets[ROOT/'assets/quest'/f'{name}.png']=(1296,864)
    public=ROOT/'art/public/characters/neutral-cast.png';targets[public]=(1024,1536)
    rows=[]
    for p,size in targets.items():
        if not p.exists():continue
        before=p.read_bytes();im=Image.open(p).convert('RGBA');old=list(im.size)
        if im.size!=size:im=im.resize(size,Image.Resampling.LANCZOS)
        im.save(p,optimize=True,compress_level=9)
        rows.append({'asset':str(p.relative_to(ROOT)) if '.private' not in p.parts else 'private/'+p.name,'before_pixels':old,'after_pixels':list(im.size),'before_bytes':len(before),'after_bytes':p.stat().st_size,'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    catalog=ROOT/'art/public/characters/catalog.json';data=json.loads(catalog.read_text());data['sha256']=hashlib.sha256(public.read_bytes()).hexdigest();catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    # Keep private asset paths out of the public optimization report.
    private=[r for r in rows if r['asset'].startswith('private/')]
    report=ROOT/'build/reports';report.mkdir(parents=True,exist_ok=True)
    (report/'private-graphics-optimization.json').write_text(json.dumps(private,indent=2)+'\n')
    (ROOT/'docs/qa/graphics-optimization.json').write_text(json.dumps({'method':'Pillow Lanczos RGBA; optimize PNG; no palette quantization','shared':[r for r in rows if r not in private],'private_summary':{'files':len(private),'before_bytes':sum(r['before_bytes'] for r in private),'after_bytes':sum(r['after_bytes'] for r in private),'classic_pixels':[512,768],'costume_pixels':[768,1152]}},indent=2)+'\n')
    print('Optimized',len(rows),'images:',sum(r['before_bytes'] for r in rows),'->',sum(r['after_bytes'] for r in rows),'source PNG bytes')
if __name__=='__main__':main()
