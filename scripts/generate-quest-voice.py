#!/usr/bin/env python3
"""Generate bundled, deduplicated offline neural narration for one UI language.

Development only: piper-tts1.4.2, onnxruntime, FFmpeg. Supply a licensed local
model; no download or speech engine in the Android application.
"""
import argparse,hashlib,json,subprocess,tempfile,wave,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

MODELS={'de':('de_DE-kerstin-low','CC0','female'),'en':('en_US-ljspeech-medium','Public Domain','female'),'ru':('ru_RU-denis-medium','CC0','male')}
GLOBALS={
 'de':{'choose':'Wer bist du heute? Wanja und seine Familie freuen sich auf dich. Tippe auf eine Figur. Dann geht es los.','walk':'Tippe auf ein Schild. Deine Figur läuft dorthin. Unten kannst du weitere Bereiche durch Wischen finden.','success':'Das passt! Du hast es geschafft.','again':'Schau noch einmal. Du kannst es ausprobieren.'},
 'en':{'choose':'Who are you today? Wanja and the family are ready. Tap a character, then let us go.','walk':'Tap a sign. Your character walks there. Swipe the subjects along the bottom to discover more.','success':'That is right! You did it.','again':'Take another look. You can try again.'},
 'ru':{'choose':'Кем ты будешь сегодня? Ваня и его семья ждут тебя. Нажми на персонажа, и начнём.','walk':'Нажми на табличку. Персонаж подойдёт к ней. Проведи пальцем по разделам внизу, чтобы найти другие.','success':'Правильно! У тебя получилось.','again':'Посмотри ещё раз. Можно попробовать снова.'}}

def narration_texts(locale):
    languages=json.loads((ROOT/'games/quest/languages.json').read_text())
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
    texts=dict(GLOBALS[locale])
    for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
        texts['area_'+subject]=languages['ui'][subject][locale]
    for task in tasks:
        values=task['texts'][locale]
        prompt=values['prompt']
        # Pictures are named aloud in the interface language. German learning
        # targets are always pronounced by the German recording queued afterwards.
        if task['kind']=='discovery' or (locale=='de' and task['subject']=='german' and task['kind']=='rhyme'):
            names=[languages['objects'][o][locale] for o in task['options']]
            prompt+=' '+languages['ui']['choices'][locale]+' '+'. '.join(names)+'.'
        texts[task['id']]=prompt
        texts[task['id']+'_hint']=values['tip']
    return texts

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locale',choices=MODELS,required=True)
    parser.add_argument('--model',type=Path,required=True)
    parser.add_argument('--threads',type=int,default=2)
    args=parser.parse_args()
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from piper import PiperVoice,SynthesisConfig
    from piper.config import PiperConfig
    options=onnxruntime.SessionOptions();options.intra_op_num_threads=args.threads;options.inter_op_num_threads=1
    voice=PiperVoice(session=onnxruntime.InferenceSession(str(args.model),sess_options=options,providers=['CPUExecutionProvider']),config=PiperConfig.from_dict(json.loads(Path(str(args.model)+'.json').read_text())),download_dir=args.model.parent)
    model,lic,gender=MODELS[args.locale]
    assert args.model.name==model+'.onnx'
    dest=ROOT/'assets/voice/quest'/args.locale;dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.model.parent/'MODEL_CARD',dest/'MODEL_CARD.txt')
    manifest={'schema':2,'locale':args.locale,'engine':'Piper 1.4.2 (development tool only)','model':model,'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),'model_source':'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-'+model+'.tar.bz2','dataset_license':lic,'voice_gender':gender,'runtime':'Bundled Vorbis only; no network, microphone, model or TTS engine','human_listening_review':'OPEN; independent synthetic voice, no actor imitation','clips':[]}
    old={}
    if (dest/'manifest.json').exists():
        for row in json.loads((dest/'manifest.json').read_text())['clips']:old[row['text']]=row
    done={}
    with tempfile.TemporaryDirectory(prefix='kinderwelt-voice.') as temp:
        for index,(id,text) in enumerate(narration_texts(args.locale).items()):
            if text in done:row=dict(done[text])
            elif text in old and (dest/old[text]['file']).exists() and hashlib.sha256((dest/old[text]['file']).read_bytes()).hexdigest()==old[text]['sha256']:
                row=dict(old[text]);done[text]=row
            else:
                filename='voice_'+args.locale+'_'+hashlib.sha256(text.encode()).hexdigest()[:20]+'.ogg'
                wav=Path(temp)/'speech.wav'
                with wave.open(str(wav),'wb') as out:voice.synthesize_wav(text,out,SynthesisConfig(length_scale=1.04,volume=.72))
                output=dest/filename
                subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(wav),'-ac','1','-ar','22050','-c:a','libvorbis','-q:a','4',str(output)],check=True)
                with wave.open(str(wav)) as out:seconds=out.getnframes()/out.getframerate()
                row={'text':text,'file':filename,'seconds':seconds,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()};done[text]=dict(row)
            row['id']=id;manifest['clips'].append(row)
            if index%25==0:print(args.locale,index,id,flush=True)
            # Checkpoint enables a safe interrupted run to resume without resynthesis.
            if index%25==0:(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    keep={r['file'] for r in manifest['clips']}
    for f in dest.glob('voice_*.ogg'):
        if f.name not in keep:f.unlink()
    print(args.locale,len(manifest['clips']),'clip mappings;',len(keep),'unique recordings',flush=True)

if __name__=='__main__':main()
