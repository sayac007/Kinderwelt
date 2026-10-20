#!/usr/bin/env python3
"""Original offline retro miniature studies; no recordings, samples or dependencies."""
from pathlib import Path
import math,struct,wave,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
RATE=22050
# Newly voiced/transposed miniature motifs inspired by public-domain compositions.
# These are playful studies, not critical transcriptions or modern arrangements.
THEMES={
 'logic':('Liszt · Liebesträume Nr. 3',84,[72,72,72,71,72,76,75,72,70,68,67,68,72,70,68,0], [56,63,65,60]),
 'math':('Liszt · Ungarische Rhapsodie Nr. 2',108,[69,70,73,74,73,70,69,0,76,74,73,70,69,68,69,0],[45,52,50,52]),
 'language':('Puccini · O mio babbino caro',78,[67,72,71,72,76,74,72,71,69,67,69,72,71,69,67,0],[48,55,57,55]),
 'autonomy':('Liszt · La Campanella',104,[83,0,83,82,83,78,79,83,81,79,78,76,78,81,79,0],[52,59,57,59]),
 'social':('Puccini · Nessun dorma',82,[71,74,76,78,76,74,71,0,72,76,79,78,76,74,71,0],[43,50,48,50])}

def voice(freq,t):
 return sum(math.sin(2*math.pi*freq*h*t)/(h*h) for h in [1,3,5]) / 1.16

def compose(module,bpm,notes,chords):
 beat=60/bpm; steps=64; duration=steps*beat/2
 samples=[0.0]*int(duration*RATE)
 def note(midi,start,length,gain):
  if not midi:return
  frequency=440*2**((midi-69)/12)
  for i in range(int(length*RATE)):
   index=int(start*RATE)+i
   if index>=len(samples):break
   t=i/RATE
   envelope=min(1,t/.018)*min(1,(length-t)/.07)
   samples[index]+=voice(frequency,t)*gain*envelope
 for step in range(steps):
  start=step*beat/2; n=notes[step%len(notes)]
  # Repetition with an octave-answer in the second phrase, restrained range.
  note(n,start,beat*.46,.19)
  root=chords[(step//16)%4]
  if step%4==0:note(root,start,beat*.85,.12)
  note(root+[12,19,24,19][step%4],start,beat*.34,.055)
 # Quiet boundaries, seamless cyclic timing; no abrupt full-amplitude loop join.
 for i in range(len(samples)):
  samples[i]*=min(1,i/(RATE*.08),(len(samples)-1-i)/(RATE*.1))
 path=ROOT/'assets/music'/f'{module}.wav'
 with wave.open(str(path),'wb') as wav:
  wav.setparams((1,2,RATE,0,'NONE','not compressed'))
  wav.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,x))*22000)) for x in samples))
 return {'file':str(path.relative_to(ROOT)),'duration_seconds':len(samples)/RATE,'sample_rate':RATE,'peak':round(max(abs(x) for x in samples)*22000/32768,5),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

if __name__=='__main__':
 manifest={'provenance':'Original synthesized retro miniature studies; public-domain compositional inspiration, no sampled recordings or third-party arrangements.','license':'MIT (original code and generated recordings); underlying works require jurisdiction-specific public-domain review before distribution.','orchestral_variant':'not produced; shared MIDI-note themes are the production input','themes':{}}
 for module,(work,bpm,notes,chords) in THEMES.items():
  manifest['themes'][module]=compose(module,bpm,notes,chords)|{'inspiration':work,'bpm':bpm,'notes_midi':notes,'bass_midi':chords}
 (ROOT/'assets/music/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
