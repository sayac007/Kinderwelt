#!/usr/bin/env python3
"""Build bundled German neural clips locally; no speech service in the app.

Run with piper-tts==1.4.2 and ffmpeg. Supply the extracted pinned Thorsten
medium model; the generator never downloads a model or sends text to a server.
"""
import argparse, hashlib, json, subprocess, tempfile, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-medium.tar.bz2'

def main():
    from piper import PiperVoice, SynthesisConfig
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True)
    args = parser.parse_args()
    voice = PiperVoice.load(args.model)
    tasks = json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
    texts = {'choose':'Wer bist du heute? Tippe auf eine Figur. Dann geht es los.',
             'walk':'Tippe auf ein Schild. Deine Figur läuft dorthin.',
             'success':'Das passt! Du hast es geschafft.',
             'again':'Das passt noch nicht. Schau noch einmal. Du kannst es ausprobieren.'}
    for task in tasks:
        texts[task['id']] = task['prompt']
        texts[task['id']+'_hint'] = task['tip']
    destination = ROOT/'assets/voice/quest'
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {'engine':'Piper 1.4.2 (development tool only)',
                'model':'de_DE-thorsten-medium', 'model_source':'k2-fsa/sherpa-onnx: tts-models release, vits-piper-de_DE-thorsten-medium.tar.bz2 (URL in docs/subject-adventure-v05.md)',
                'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),
                'dataset_license':'CC0, see Thorsten MODEL_CARD.txt',
                'runtime':'Bundled Vorbis only; no network, microphone, model or TTS engine',
                'human_listening_review':'OPEN; synthetic voice, not an actor recording', 'clips':[]}
    with tempfile.TemporaryDirectory() as temp:
        for name, text in texts.items():
            wav = Path(temp)/(name+'.wav')
            with wave.open(str(wav),'wb') as stream:
                voice.synthesize_wav(text,stream,SynthesisConfig(length_scale=1.08,volume=.8))
            out = destination/(name+'.ogg')
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(wav),'-ac','1','-ar','22050','-c:a','libvorbis','-q:a','4',str(out)],check=True)
            with wave.open(str(wav)) as stream: duration=stream.getnframes()/stream.getframerate()
            manifest['clips'].append({'id':name,'text':text,'seconds':duration,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
            print(name, round(duration,2), flush=True)
    (destination/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
