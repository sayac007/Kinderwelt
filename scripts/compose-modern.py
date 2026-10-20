#!/usr/bin/env python3
"""Eight additional original electronic scores; the two 0.3 originals remain.
Uses our own standard-library synth, then Vorbis quality 5. No borrowed melodies.
"""
import importlib.util,json,hashlib,tempfile,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('synth',ROOT/'scripts/compose-adventure.py')
synth=importlib.util.module_from_spec(spec);spec.loader.exec_module(synth)
# Each score has its own melodic contour, harmony root and tempo.
SCORES=[
 ('meadow',116,48,[0,7,4,9,7,2,4,0, 5,12,9,7,5,4,2,5, 9,7,12,16,14,9,7,4, 7,2,11,14,12,7,4,2]),
 ('gears',138,43,[0,3,7,3,10,7,3,12, 5,8,12,8,15,12,8,5, 9,12,16,12,19,16,12,9, 7,10,14,10,17,14,10,7]),
 ('market',128,50,[4,7,12,7,4,2,0,2, 9,12,17,12,9,7,5,7, 12,16,21,16,12,9,7,9, 11,14,19,14,11,9,7,2]),
 ('stories',104,53,[0,4,2,7,4,9,7,12, 5,9,7,12,9,14,12,17, 9,12,11,16,12,19,16,21, 7,11,9,14,11,16,14,7]),
 ('garden',122,48,[0,2,4,7,4,2,9,7, 5,7,9,12,9,7,14,12, 9,11,12,16,12,11,19,16, 7,9,11,14,11,9,16,14]),
 ('together',134,46,[7,4,0,4,12,9,4,7, 12,9,5,9,17,14,9,12, 16,12,9,12,21,19,12,16, 14,11,7,11,19,16,11,14]),
 ('rain',110,51,[0,7,12,14,12,7,4,7, 5,12,17,19,17,12,9,12, 9,16,21,23,21,16,12,16, 7,14,19,21,19,14,11,14]),
 ('victory',154,48,[12,7,12,16,19,16,12,7, 17,12,17,21,24,21,17,12, 21,16,21,24,28,24,21,16, 19,14,19,23,26,23,19,14])]
if __name__=='__main__':
 out=ROOT/'assets/music/modern';out.mkdir(parents=True,exist_ok=True);entries=[]
 with tempfile.TemporaryDirectory(prefix='kinderwelt-music.') as temp:
  synth.ROOT=Path(temp)
  for name,bpm,key,notes in SCORES:
   info=synth.compose(name,bpm,key,notes)
   dest=out/(name+'.ogg')
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(Path(temp)/(name+'.wav')),'-c:a','libvorbis','-q:a','5','-map_metadata','-1',str(dest)],check=True)
   entries.append({'id':name,'bpm':bpm,'root_midi':key,'melody':notes,'seconds':info['seconds'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'format':'Ogg Vorbis q5, mono 22050 Hz','layers':info['layers']})
 (out/'manifest.json').write_text(json.dumps({'license':'MIT, original score and synthesized sounds','generator':'scripts/compose-modern.py','quality':'prototype mix; human listening review required','tracks':entries},indent=2)+'\n')
