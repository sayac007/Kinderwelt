#!/usr/bin/env python3
"""Bundled offline German prototype speech from original text, using eSpeak NG.
Generation-only tool; no speech engine, recording, microphone or network in app.
"""
import argparse,hashlib,json,os,subprocess,tempfile
from pathlib import Path
TEXT={
 'logic':'Baue eine Brücke.','math':'Komm mit zum Markt.','language':'Entdecke Bildergeschichten.',
 'autonomy':'Willkommen in der Entdeckerwerkstatt.','social':'Gemeinsam im Dorf.',
 'heroes':'Wähle ein Kind. Alle können alles lernen.','musicbox':'Tippe auf ein Bild. So hörst du die Musik.',
 'settings':'Hier stellst du Ton und Schrift ein.','parents':'Dieser Bereich ist für begleitende Erwachsene.',
 'mina':'Mina.','leo':'Leo.','sam':'Sam.','jule':'Jule.',
 'water_0':'Die Pflanze hat Durst. Verbinde die Rohre. Tippe ein Rohr an, um es zu drehen.',
 'water_1':'Pflanze und Vogel haben Durst. Verbinde die Rohre mit beiden Zielen.',
 'water_2':'Beide Pflanzen haben Durst. Sechs Tropfen müssen reichen. Schließe alle offenen Rohrenden.',
 'water_help':'Tippe ein Rohr zum Drehen an. Ziehe es auf einen anderen Platz. Mit dem Wasserknopf öffnest du den Hahn.',
 'water_success':'Geschafft! Das Wasser kommt an. Jetzt wächst die Pflanze.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tools',type=Path,default=Path('/workspace/tools/voice'));a=p.parse_args()
 root=Path(__file__).resolve().parents[1];out=root/'assets/voice';out.mkdir(parents=True,exist_ok=True)
 lib=a.tools/'usr/lib/x86_64-linux-gnu';env=os.environ.copy();env['LD_LIBRARY_PATH']=str(lib);env['ESPEAK_DATA_PATH']=str(lib)
 entries=[]
 with tempfile.TemporaryDirectory(prefix='kinderwelt-voice.') as directory:
  for name,text in TEXT.items():
   wav=Path(directory)/(name+'.wav');clip=out/(name+'.ogg')
   subprocess.run([str(a.tools/'usr/bin/espeak-ng'),'--path='+str(lib),'-v','de','-s','145','-p','48','-w',str(wav),text],env=env,check=True)
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-ar','22050','-ac','1','-c:a','libvorbis','-q:a','4','-map_metadata','-1',str(clip)],check=True)
   entries.append({'id':name,'text':text,'file':name+'.ogg','sha256':hashlib.sha256(clip.read_bytes()).hexdigest()})
 deps=[{'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(a.tools.glob('*.deb'))]
 (out/'manifest.json').write_text(json.dumps({'language':'de','voice':'eSpeak NG 1.52.0, de, 145 words/min, pitch 48','quality':'SYNTHETIC PROTOTYPE, not natural production narration','generator':'scripts/generate-voice.py','license':'Original text and generated output: repository MIT. eSpeak NG GPLv3 tool only; no binary or dictionaries shipped.','generation_packages':deps,'clips':entries},ensure_ascii=False,indent=2)+'\n')
