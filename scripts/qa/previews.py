#!/usr/bin/env python3
"""Create optional review copies outside the shipped application."""
import argparse,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('kind',choices=['music','voice']);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 if a.kind=='music':
  folder=ROOT/'assets/music';entries=json.loads((folder/'manifest.json').read_text())['tracks']
  files=[(folder/e['file'],e['id']) for e in entries];shutil.copy2(folder/'NOTICES.txt',a.output/'NOTICES.txt');shutil.copytree(folder/'licenses',a.output/'licenses')
 else:
  files=[]
  for locale in ['de','en','ru']:
   folder=ROOT/'assets/voice/quest'/locale;clips={c['id']:c for c in json.loads((folder/'manifest.json').read_text())['clips']}
   shutil.copy2(folder/'MODEL_CARD.txt',a.output/(locale+'-MODEL_CARD.txt'))
   for key in ['area_physics','math_count','math_count_hint','praise_0']:files.append((folder/clips[key]['file'],locale+'-'+key))
 for source,name in files:subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(source),'-t','30','-c:a','libmp3lame','-q:a','3',str(a.output/(name+'.mp3'))],check=True)
 print('Generated',len(files),'review clips in',a.output)
if __name__=='__main__':main()
