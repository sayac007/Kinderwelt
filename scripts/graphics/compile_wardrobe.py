#!/usr/bin/env python3
"""Read atlas alpha to compile native Godot sampling metadata; never rewrite PNGs.
Development dependencies: Pillow, NumPy, SciPy. No runtime image processing service.
"""
from PIL import Image
from scipy import ndimage
from pathlib import Path
import json,hashlib,numpy as np
p=Path(__file__).resolve().parents[2]/'assets/quest/looks.json';data=json.loads(p.read_text());data['layout']='Four generated costumes; visible frame bounds and nearest-figure ownership for native atlas sampling. Original PNG pixels unchanged.'
for id,hero in data['heroes'].items():
 source=p.parent/hero['file'];image=Image.open(source);alpha=np.asarray(image)[:,:,3]
 hero['sha256']=hashlib.sha256(source.read_bytes()).hexdigest();hero['pixels']=list(image.size)
 labels,n=ndimage.label(alpha>32);counts=np.bincount(labels.ravel());counts[0]=0
 primary=np.argsort(counts)[-4:];parts=[]
 for label in primary:
  ys,xs=np.where(labels==label);parts.append({'label':int(label),'x':float(xs.mean()),'y':float(ys.mean()),'rect':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]})
 upper=sorted(sorted(parts,key=lambda a:a['y'])[:2],key=lambda a:a['x']);lower=sorted(sorted(parts,key=lambda a:a['y'])[2:],key=lambda a:a['x']);parts=upper+lower
 ownership=np.zeros(labels.shape,dtype=np.uint8);hero['frames']={};hero['probes']={}
 for index,(look,part) in enumerate(zip(['hero','alien','astronaut','scientist'],parts)):
  ownership[labels==part['label']]=index+1
  x0,y0,x1,y1=part['rect'];x0=max(0,x0-5);y0=max(0,y0-5);x1=min(image.width,x1+5);y1=min(image.height,y1+5)
  hero['frames'][look]=[x0,y0,x1-x0,y1-y0]
  ys,xs=np.where(labels==part['label']);mid=len(xs)//2;hero['probes'][look]=[int(xs[mid]),int(ys[mid])]
 # This metadata labels source pixels; Godot builds a tiny R8 sampling mask once.
 nearest=ndimage.distance_transform_edt(ownership==0,return_distances=False,return_indices=True)
 owner=ownership[nearest[0],nearest[1]]
 runs=[]
 for y,row in enumerate(owner):
  cuts=np.r_[0,np.flatnonzero(row[1:]!=row[:-1])+1,image.width]
  for left,right in zip(cuts[:-1],cuts[1:]):runs.append([y,int(left),int(right-left),int(row[left])])
 hero['mask_runs']=runs
 print(id,'native mask runs',len(runs),'frames',hero['frames'])
p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
