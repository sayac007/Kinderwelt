#!/usr/bin/env python3
"""Research-only: native DE/RU phonemes with the existing English acoustic model.

Does not change shipped recordings. This route was rejected by independent ASR;
see docs/voice-v081.md. No external voice or model is downloaded.
"""
import argparse,hashlib,importlib.util,json,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
IDS=['area_physics','area_chemistry','praise_1','math_count','german_sun','physics_05_hint','world_city']
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('Output must be a new directory')
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from piper import PiperVoice,SynthesisConfig
    from piper.config import PiperConfig
    spec=importlib.util.spec_from_file_location('voice_source',ROOT/'scripts/generate-quest-voice.py');source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
    pinned=json.loads((ROOT/'scripts/qa/voice-models.json').read_text())['selected']['en']
    if hashlib.sha256(a.model.read_bytes()).hexdigest()!=pinned['model_sha256']:raise ValueError('Use the actual shipped English voice model')
    options=onnxruntime.SessionOptions();options.intra_op_num_threads=2;options.inter_op_num_threads=1
    session=onnxruntime.InferenceSession(source.duration_model(a.model),sess_options=options,providers=['CPUExecutionProvider'])
    class NativeVoice(PiperVoice):
        def phonemize(self,text):return [source.normalized_phonemes(row,self.config.phoneme_id_map) for row in super().phonemize(text)]
    a.output.mkdir(parents=True)
    for locale in ['de','ru']:
        config=PiperConfig.from_dict(json.loads(Path(str(a.model)+'.json').read_text()));config.espeak_voice=locale
        voice=NativeVoice(session=session,config=config,download_dir=a.model.parent)
        manifest=json.loads((ROOT/'assets/voice/quest'/locale/'manifest.json').read_text());clips={c['id']:c for c in manifest['clips']};rows=[]
        for id in IDS:
            text=clips[id]['text'];destination=a.output/(locale+'-'+id+'.wav')
            chunks=list(voice.synthesize(text,SynthesisConfig(length_scale=1.3,noise_scale=.5,noise_w_scale=0.,volume=.68),include_alignments=True))
            with wave.open(str(destination),'wb') as out:
                out.setnchannels(1);out.setsampwidth(2);out.setframerate(chunks[0].sample_rate);out.writeframes(b'\0'*7938)
                for chunk in chunks:out.writeframes(chunk.audio_int16_bytes);out.writeframes(b'\0'*12348)
            rows.append({'id':id,'text':text,'file':destination.name})
        (a.output/(locale+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
        print('Research samples only:',locale,len(rows),'— not installed in the app')
if __name__=='__main__':main()
