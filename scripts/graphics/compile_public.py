#!/usr/bin/env python3
"""Derive tight frames/ownership from original public atlas alpha; no PNG edits."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2]
def main():
 folder=ROOT/'art/public/characters';catalog=json.loads((folder/'catalog.json').read_text());path=folder/catalog['source'];image=Image.open(path);alpha=np.asarray(image)[:,:,3]
 labels,n=ndimage.label(alpha>32);counts=np.bincount(labels.ravel());counts[0]=0
 primary=np.flatnonzero(counts>10000);assert len(primary)==30,'Expected 30 separated public figures'
 parts=[]
 for label in primary:
  ys,xs=np.where(labels==label);parts.append({'label':int(label),'x':float(xs.mean()),'y':float(ys.mean()),'box':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]})
 parts.sort(key=lambda p:p['y']);heroes={}
 for row,id in enumerate(catalog['names']):
  group=sorted(parts[row*5:row*5+5],key=lambda p:p['x']);low=max(0,min(p['box'][1] for p in group)-2);high=min(image.height,max(p['box'][3] for p in group)+2)
  ownership=np.zeros((high-low,image.width),dtype=np.uint8);frames={};probes={}
  for column,(look,part) in enumerate(zip(['classic','hero','alien','astronaut','scientist'],group)):
   ownership[labels[low:high]==part['label']]=max(1,column)
   x0,y0,x1,y1=part['box'];x0=max(0,x0-1);y0=max(0,y0-1);x1=min(image.width,x1+1);y1=min(image.height,y1+1)
   frames[look]=[x0,y0,x1-x0,y1-y0];ys,xs=np.where(labels==part['label']);mid=len(xs)//2;probes[look]=[int(xs[mid]),int(ys[mid])]
  near=ndimage.distance_transform_edt(ownership==0,return_distances=False,return_indices=True);owner=ownership[near[0],near[1]];runs=[]
  for y in range(image.height):
   if not low<=y<high:runs.append([y,0,image.width,1]);continue
   line=owner[y-low];cuts=np.r_[0,np.flatnonzero(line[1:]!=line[:-1])+1,image.width]
   for left,right in zip(cuts[:-1],cuts[1:]):runs.append([y,int(left),int(right-left),int(line[left])])
  heroes[id]={'file':'characters/neutral-cast.png','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pixels':list(image.size),'frames':frames,'probes':probes,'mask_runs':runs}
 (folder/'frames.json').write_text(json.dumps({'schema':1,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'heroes':heroes},separators=(',',':'))+'\n')
 print('Compiled 30 public figures with tight alpha bounds and neighboring-outfit masks')
if __name__=='__main__':main()
