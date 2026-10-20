#!/usr/bin/env python3
"""Deterministic original electronic miniatures. Python standard library only.
No sampled recordings, copyrighted melodies, personal data or network access.
"""
import hashlib,json,math,random,struct,wave
from pathlib import Path
RATE=22050
ROOT=Path(__file__).resolve().parents[1]/'assets/music/adventure'

def compose(name,bpm,root,melody):
    beat=60/bpm
    length=64*beat # 16 four-beat bars, complete phrase and harmony cycle
    count=round(length*RATE)
    sound=[0.0]*count
    rng=random.Random(73 if name=='workshop' else 101)
    def note(start,duration,midi,volume,voice):
        hz=440*2**((midi-69)/12)
        begin=round(start*RATE)
        for k in range(round(duration*RATE)):
            i=begin+k
            if i>=count: break
            t=k/RATE
            env=min(1,t/.008)*min(1,max(0,(duration-t)/.045))
            if voice=='lead':
                sample=(math.sin(math.tau*hz*t)+.32*math.sin(math.tau*2*hz*t)+.12*math.sin(math.tau*3*hz*t))*.68
                env*=math.exp(-1.7*t)
            elif voice=='bass':
                sample=(math.sin(math.tau*hz*t)+.25*math.sin(math.tau*2*hz*t))*.8
            else:
                sample=(math.sin(math.tau*hz*t)+.2*math.sin(math.tau*(hz*1.004)*t))*.7
            sound[i]+=sample*volume*env
            if voice=='lead':
                echo=i+round(beat*.75*RATE)
                if echo<count: sound[echo]+=sample*volume*env*.22
    for bar in range(16):
        chord=[0,5,9,7][bar//2%4]+root
        # Changing inversions, alternating bass, syncopated lead, sparkle arpeggios.
        for pitch in [chord+12,chord+16,chord+19]: note(bar*4*beat,3.85*beat,pitch,.055,'pad')
        for j in range(8):
            note((bar*4+j*.5)*beat,.32*beat,chord-12+(7 if j%4==3 else 0),.17,'bass')
            n=melody[(bar%4)*8+j]
            if n is not None:
                note((bar*4+j*.5)*beat,.36*beat,root+24+n,.16 if bar<8 else .19,'lead')
            if bar>=4 and j%2:
                note((bar*4+j*.5+.25)*beat,.17*beat,chord+24+[0,4,7,12][j%4],.06,'lead')
        # Kick, snare/clap, closed hats and variation at phrase endings.
        for step in range(16):
            when=(bar*4+step*.25)*beat
            begin=round(when*RATE)
            if step in [0,8] or (bar%4==3 and step==14):
                for k in range(round(.19*RATE)):
                    if begin+k>=count: break
                    t=k/RATE
                    phase=math.tau*(48*t+80*.025*(1-math.exp(-t/.025)))
                    sound[begin+k]+=.30*math.sin(phase)*math.exp(-t*24)
            if step in [4,12]:
                for k in range(round(.13*RATE)):
                    if begin+k>=count: break
                    t=k/RATE
                    sound[begin+k]+=(rng.uniform(-1,1)*.15+math.sin(math.tau*180*t)*.06)*math.exp(-t*32)*min(1,t/.002)
            if step%2==0 or (bar%4==3 and step>11):
                previous=0.0
                for k in range(round(.045*RATE)):
                    if begin+k>=count: break
                    noise=rng.uniform(-1,1)
                    sound[begin+k]+=(noise-previous)*.035*math.exp(-k/RATE*95)*min(1,k/(RATE*.002))
                    previous=noise
    # A short boundary fade prevents a discontinuity; no false gapless device claim.
    peak=max(abs(n) for n in sound)
    pcm=bytearray()
    for i,value in enumerate(sound):
        fade=min(1,i/(RATE*.008),(count-1-i)/(RATE*.008))
        pcm.extend(struct.pack('<h',round(value/peak*.82*fade*32767)))
    path=ROOT/(name+'.wav')
    with wave.open(str(path),'wb') as wav:
        wav.setparams((1,2,RATE,0,'NONE','not compressed'));wav.writeframes(pcm)
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'seconds':count/RATE,'bpm':bpm,'bars':16,'original_composition':True,'layers':['melody','echo','bass','chords','arpeggio','kick','snare','hi-hat'],'peak_linear':.82}

if __name__=='__main__':
    ROOT.mkdir(parents=True,exist_ok=True)
    tunes=[compose('workshop',132,48,[0,4,7,12,7,4,2,7, 5,9,12,14,12,9,7,5, 9,12,16,12,7,9,12,7, 7,11,14,19,14,11,7,2]),compose('stars',146,50,[7,12,14,16,14,12,7,4, 9,12,17,16,12,9,5,9, 12,16,19,16,14,12,9,4, 11,14,19,14,11,7,2,7])]
    (ROOT/'manifest.json').write_text(json.dumps({'license':'MIT; original synthesized compositions, no third-party recordings or tunes','generator':'scripts/compose-adventure.py','quality':'experimental procedural audio, console production quality not established','tracks':tunes},indent=2)+'\n')
