#!/usr/bin/env python3
"""Generate bundled, deduplicated offline neural narration for one UI language.

Development only: piper-tts1.4.2, onnxruntime, FFmpeg. Supply a licensed local
model; no download or speech engine in the Android application.
"""
import argparse,hashlib,json,subprocess,tempfile,wave,shutil,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

MODELS={'de':('de_DE-kerstin-low','CC0','female'),'en':('en_US-ljspeech-medium','Public Domain','female'),'ru':('ru_RU-denis-medium','CC0','male')}
GLOBALS={
 'de':{'choose':'Wer bist du heute? Wanja und seine Familie freuen sich auf dich. Tippe auf eine Figur. Dann geht es los.','walk':'Tippe auf ein Schild. Deine Figur läuft dorthin. Unten kannst du alle acht Bereiche direkt antippen.','success':'Wunderbar! Das hast du gut gemacht.','again':'Schau noch einmal. Du kannst es ausprobieren.'},
 'en':{'choose':'Who are you today? Wanja and the family are ready. Tap a character, then let us go.','walk':'Tap a sign. Your character walks there. Tap any of the eight subjects along the bottom.','success':'That is right! You did it.','again':'Take another look. You can try again.'},
 'ru':{'choose':'Кем ты будешь сегодня? Ваня и его семья ждут тебя. Нажми на персонажа, и начнём.','walk':'Нажми на табличку. Персонаж подойдёт к ней. Нажми на любой из восьми разделов внизу.','success':'Правильно! У тебя получилось.','again':'Посмотри ещё раз. Можно попробовать снова.'}}

PRAISE={
'de':['Wunderbar! Das hast du gut gemacht.','Sehr klug entschieden!','Super cool, das gefällt mir!','Toll gelöst! Weiter so!','Du hast genau hingeschaut. Klasse!','Prima! Du hast es herausgefunden.'],
'en':['Wonderful! You did that really well.','That was a clever choice!','Super cool! I like that!','Great work! Keep going!','You looked carefully. Well done!','Brilliant! You worked it out.'],
'ru':['Замечательно! У тебя отлично получилось.','Очень умное решение!','Супер! Мне нравится!','Здорово решено! Так держать!','Ты внимательно посмотрел. Отлично!','Прекрасно! У тебя получилось разобраться.']}
SYNTHESIS={'revision':'articulated-2','length_scale':1.18,'noise_scale':0.5,'noise_w_scale':0.6,'volume':0.68,'lead_seconds':0.18,'tail_seconds':0.35,'sentence_pause_seconds':0.28}

def narration_texts(locale):
    languages=json.loads((ROOT/'games/quest/languages.json').read_text())
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
    texts=dict(GLOBALS[locale])
    texts.update({"praise_"+str(i):text for i,text in enumerate(PRAISE[locale])})
    for look in ['classic','hero','alien','astronaut','scientist']:
        texts['look_'+look]=languages['ui']['look_'+look][locale]
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

def normalized_phonemes(phonemes,id_map):
    """Compose supported IPA graphemes (notably c + cedilla -> ç), never drop a sound."""
    groups=[]
    for char in ''.join(phonemes):
        if unicodedata.combining(char) and groups:groups[-1]+=char
        else:groups.append(char)
    result=[]
    for group in groups:
        composed=unicodedata.normalize('NFC',group)
        result.extend([composed] if composed in id_map else list(group))
    unknown=set(result)-set(id_map)
    if unknown:raise ValueError('Unsupported speech phonemes, refusing incomplete pronunciation: '+repr(sorted(unknown)))
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locale',choices=MODELS,required=True)
    parser.add_argument('--model',type=Path,required=True)
    parser.add_argument('--threads',type=int,default=2)
    args=parser.parse_args()
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from piper import PiperVoice,SynthesisConfig
    class CompleteVoice(PiperVoice):
        def phonemize(self,text):
            return [normalized_phonemes(sentence,self.config.phoneme_id_map) for sentence in super().phonemize(text)]
    from piper.config import PiperConfig
    options=onnxruntime.SessionOptions();options.intra_op_num_threads=args.threads;options.inter_op_num_threads=1
    voice=CompleteVoice(session=onnxruntime.InferenceSession(str(args.model),sess_options=options,providers=['CPUExecutionProvider']),config=PiperConfig.from_dict(json.loads(Path(str(args.model)+'.json').read_text())),download_dir=args.model.parent)
    profile=dict(SYNTHESIS)
    if args.locale=='de':profile['phoneme_normalization']='supported-nfc'
    model,lic,gender=MODELS[args.locale]
    assert args.model.name==model+'.onnx'
    dest=ROOT/'assets/voice/quest'/args.locale;dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.model.parent/'MODEL_CARD',dest/'MODEL_CARD.txt')
    manifest={'schema':3,'synthesis':profile,'locale':args.locale,'engine':'Piper 1.4.2 (development tool only)','model':model,'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),'model_source':'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-'+model+'.tar.bz2','dataset_license':lic,'voice_gender':gender,'runtime':'Bundled Vorbis only; no network, microphone, model or TTS engine','human_listening_review':'OPEN; independent synthetic voice, no actor imitation','clips':[]}
    old={}
    if (dest/'manifest.json').exists():
        previous=json.loads((dest/'manifest.json').read_text())
        if previous.get('synthesis')==profile:
            for row in previous['clips']:old[row['text']]=row
    done={}
    with tempfile.TemporaryDirectory(prefix='kinderwelt-voice.') as temp:
        for index,(id,text) in enumerate(narration_texts(args.locale).items()):
            if text in done:row=dict(done[text])
            elif text in old and (dest/old[text]['file']).exists() and hashlib.sha256((dest/old[text]['file']).read_bytes()).hexdigest()==old[text]['sha256']:
                row=dict(old[text]);done[text]=row
            else:
                filename='voice_'+args.locale+'_'+hashlib.sha256((text+json.dumps(profile,sort_keys=True)).encode()).hexdigest()[:20]+'.ogg'
                wav=Path(temp)/'speech.wav'
                chunks=list(voice.synthesize(text,SynthesisConfig(length_scale=SYNTHESIS['length_scale'],noise_scale=SYNTHESIS['noise_scale'],noise_w_scale=SYNTHESIS['noise_w_scale'],volume=SYNTHESIS['volume'])))
                assert chunks and all(c.sample_rate==chunks[0].sample_rate and c.sample_width==2 and c.sample_channels==1 for c in chunks)
                rate=chunks[0].sample_rate
                with wave.open(str(wav),'wb') as out:
                    out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate)
                    out.writeframes(b'\0'*(round(rate*SYNTHESIS['lead_seconds'])*2))
                    for n,chunk in enumerate(chunks):
                        # Keep every sample of every generated sentence, with a real pause.
                        out.writeframes(chunk.audio_int16_bytes)
                        if n<len(chunks)-1:out.writeframes(b'\0'*(round(rate*SYNTHESIS['sentence_pause_seconds'])*2))
                    out.writeframes(b'\0'*(round(rate*SYNTHESIS['tail_seconds'])*2))
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
        if f.name not in keep:
            f.unlink()
            f.with_suffix('.ogg.import').unlink(missing_ok=True)
    print(args.locale,len(manifest['clips']),'clip mappings;',len(keep),'unique recordings',flush=True)

if __name__=='__main__':main()
