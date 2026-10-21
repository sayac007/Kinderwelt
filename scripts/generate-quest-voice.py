#!/usr/bin/env python3
"""Generate bundled, deduplicated offline neural narration for one UI language.

Development only: piper-tts1.4.2, onnxruntime, FFmpeg. Supply a licensed local
model; no download or speech engine in the Android application.
"""
import array,math
import argparse,hashlib,json,subprocess,tempfile,wave,shutil,unicodedata,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

MODELS={'de':('de_DE-thorsten-high','CC0','male'),'en':('en_US-ljspeech-medium','Public Domain','female'),'ru':('ru_RU-denis-medium','CC0','male')}
GLOBALS={
 'de':{'choose':'Wer bist du heute? Suche dir eine Figur aus. Tippe dann auf Start.','walk':'Tippe auf ein Schild. Deine Figur läuft dorthin. Unten kannst du alle acht Bereiche direkt antippen.','success':'Wunderbar! Das hast du gut gemacht.','again':'Schau noch einmal. Du kannst es ausprobieren.'},
 'en':{'choose':'Who will you be today? Choose a character. Then tap Start.','walk':'Tap a sign. Your character walks there. Tap any of the eight subjects along the bottom.','success':'That is right! You did it.','again':'Take another look. You can try again.'},
 'ru':{'choose':'Кем ты будешь сегодня? Выбери персонажа. Затем нажми «Начать».','walk':'Нажми на табличку. Персонаж подойдёт к ней. Нажми на любой из восьми разделов внизу.','success':'Правильно! У тебя получилось.','again':'Посмотри ещё раз. Можно попробовать снова.'}}

PRAISE={
'de':['Wunderbar! Das hast du gut gemacht.','Sehr klug entschieden!','Super cool, das gefällt mir!','Toll gelöst! Weiter so!','Du hast genau hingeschaut. Klasse!','Prima! Du hast es herausgefunden.'],
'en':['Wonderful! You did that really well.','That was a clever choice!','Super cool! I like that!','Great work! Keep going!','You looked carefully. Well done!','Brilliant! You worked it out.'],
'ru':['Замечательно! У тебя отлично получилось.','Очень умное решение!','Супер! Мне нравится!','Здорово решено! Так держать!','Ты внимательно посмотрел. Отлично!','Прекрасно! У тебя получилось разобраться.']}
SYNTHESIS={'revision':'articulated-2','length_scale':1.18,'noise_scale':0.5,'noise_w_scale':0.6,'volume':0.68,'lead_seconds':0.18,'tail_seconds':0.35,'sentence_pause_seconds':0.28}

def synthesis_profile(locale):
    profile=dict(SYNTHESIS)
    if locale=='de':
        profile.update(revision='articulated-3',length_scale=1.6,noise_w_scale=0.0,
                       phoneme_normalization='supported-nfc',duration_alignment='vits-ceil-frames')
    return profile

def clip_profile(locale,id,text=''):
    profile=synthesis_profile(locale)
    if locale!='de' and id.startswith(('area_','look_')):
        profile.update(revision='articulated-short-3',length_scale=1.5,noise_w_scale=0.0,
                       duration_alignment='vits-ceil-frames')
    if locale=='de' and re.search(r'\bChemie\b',text):
        profile['pronunciations']={'Chemie':'çeˈmiː'}
    return profile

def pronunciation_phonemes(phonemes,text,locale):
    # Keep the full sentence and its punctuation. eSpeak's extra long first
    # vowel/misplaced stress makes this subject unclear in the chosen model.
    if locale=='de' and re.search(r'\bChemie\b',text):
        return list(''.join(phonemes).replace('çeːmˈiː','çeˈmiː'))
    return phonemes

def duration_model(path):
    """Expose the existing VITS duration tensor; audio computation is unchanged.

    Development-only ONNX instrumentation. No model is shipped in the app.
    Reject other graphs instead of guessing which tensor represents duration.
    """
    import onnx
    model=onnx.load(str(path))
    nodes=[n for n in model.graph.node if n.op_type=='Ceil']
    if len(nodes)!=1 or len(model.graph.output)!=1:
        raise ValueError('Unsupported VITS graph for duration inspection')
    model.graph.output.append(onnx.helper.make_tensor_value_info(nodes[0].output[0],onnx.TensorProto.FLOAT,[1,1,None]))
    return model.SerializeToString()

def speech_units(chunk,offset):
    """Model-aligned phonetic words, not human-validated forced alignment.

    Space boundaries come from the phonemizer. Numbers may expand into several
    units; do not falsely label these as exact orthographic word timestamps.
    """
    if chunk.phoneme_alignments is None:raise ValueError('Missing speech-duration alignment')
    if int(chunk.phoneme_id_samples.sum())!=chunk.audio_float_array.size:
        raise ValueError('Predicted phoneme duration does not match generated samples')
    units=[];start=0;cursor=0;phonemes=''
    def flush():
        if any(c.isalpha() for c in phonemes):
            units.append({'phonemes':phonemes,'start':round(offset+start/chunk.sample_rate,6),
                          'end':round(offset+cursor/chunk.sample_rate,6),
                          'seconds':round((cursor-start)/chunk.sample_rate,6)})
    for item in chunk.phoneme_alignments:
        if item.phoneme in ['^','$',' ']:
            flush();phonemes='';cursor+=item.num_samples;start=cursor
        else:
            phonemes+=item.phoneme;cursor+=item.num_samples
    flush()
    return units

def narration_texts(locale):
    languages=json.loads((ROOT/'games/quest/languages.json').read_text())
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
    texts=dict(GLOBALS[locale])
    texts.update({"praise_"+str(i):text for i,text in enumerate(PRAISE[locale])})
    for look in ['classic','hero','alien','astronaut','scientist']:
        texts['look_'+look]=languages['ui']['look_'+look][locale]+'.'
    for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
        texts['area_'+subject]=languages['ui'][subject][locale]+'.'
    # Isolated synthetic words can lose consonants. Natural context stabilizes
    # intonation; it is spoken audio, never a prompt supplied to the ASR checker.
    if locale=='de':
        for subject in ['logic','chemistry','geography']:
            texts['area_'+subject]='Hier entdecken wir die '+languages['ui'][subject][locale]+'.'
    elif locale=='en':
        texts['area_math']='Mathematics.'
        texts['area_logic']='This is logic.'
        texts['area_geography']="Let's explore geography."
    else:
        for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
            texts['area_'+subject]='Это '+languages['ui'][subject][locale].lower()+'.'
    for task in tasks:
        values=task['texts'][locale]
        prompt=values['prompt']
        # Pictures are named aloud in the interface language. German learning
        # targets are always pronounced by the German recording queued afterwards.
        if task['kind']=='discovery' or (locale=='de' and task['subject']=='german' and task['kind']=='rhyme'):
            names=[languages['objects'][o][locale] for o in task['options']]
            if locale=='de':prompt+=' Zur Auswahl stehen '+', '.join(names[:-1])+' und '+names[-1]+'.'
            elif locale=='en':prompt+=' Choose from '+', '.join(names[:-1])+' or '+names[-1]+'.'
            else:prompt+=' '+languages['ui']['choices'][locale]+' '+'. '.join(names)+'.'
        hint=values['tip']
        if locale!='de' and task['subject']=='german':
            # Never teach German targets through an English/Russian phonemizer.
            # The runtime queues the matching full German question/hint next.
            leads={
                'initial':('Listen to the German word. Which letter does it start with?', 'Послушай немецкое слово. С какой буквы его пишут?', 'Listen to the German word and its first letter.', 'Послушай немецкое слово и его первую букву.'),
                'syllables':('Listen to the German word. How many syllables can you hear?', 'Послушай немецкое слово. Сколько слогов ты слышишь?', 'Listen to the German example and clap along.', 'Послушай немецкий пример и хлопай по слогам.'),
                'word':('Which German word matches the picture?', 'Какое немецкое слово подходит к картинке?', 'Listen to the German word and how its letters are spelled.', 'Послушай немецкое слово и как оно произносится по буквам.'),
                'rhyme':('Listen to the German words. Which ones rhyme?', 'Послушай немецкие слова. Какие из них рифмуются?', 'Listen to the two German words that rhyme.', 'Послушай два немецких слова, которые рифмуются.')}
            leads=leads[task['kind']];prompt=leads[0 if locale=='en' else 1];hint=leads[2 if locale=='en' else 3]
        texts[task['id']]=prompt
        texts[task['id']+'_hint']=hint
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

def decoded_peak(path):
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),'-ac','1','-ar','22050','-f','f32le','-'])
    pcm=array.array('f');pcm.frombytes(raw)
    if not pcm or not all(math.isfinite(v) for v in pcm):raise ValueError('Empty or non-finite encoded speech')
    return max(abs(v) for v in pcm)

def valid_cached_audio(path,expected_hash):
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected_hash:return False
    try:return .005<decoded_peak(path)<=.999
    except (subprocess.CalledProcessError,ValueError):return False


def encode_speech(wav,output,ceiling=.95):
    """Measure Vorbis overshoot; attenuate from the original WAV, never trim."""
    gain=1.0
    for attempt in range(4):
        subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(wav),'-af',f'volume={gain:.10f}','-ac','1','-ar','22050','-c:a','libvorbis','-q:a','4',str(output)],check=True)
        peak=decoded_peak(output)
        if .005<peak<=ceiling:
            return {'policy':'decoded-vorbis-peak-1','uniform_gain':gain,'decoded_peak':peak,'ceiling':ceiling,'encodes':attempt+1}
        if peak<=.005:raise ValueError('Speech too quiet after encoding')
        gain*=ceiling/peak*.98
    raise ValueError('Encoded speech still exceeds safe peak after four attempts')


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
            return [pronunciation_phonemes(normalized_phonemes(sentence,self.config.phoneme_id_map),text,args.locale) for sentence in super().phonemize(text)]
    from piper.config import PiperConfig
    options=onnxruntime.SessionOptions();options.intra_op_num_threads=args.threads;options.inter_op_num_threads=1
    model_input=duration_model(args.model)
    voice=CompleteVoice(session=onnxruntime.InferenceSession(model_input,sess_options=options,providers=['CPUExecutionProvider']),config=PiperConfig.from_dict(json.loads(Path(str(args.model)+'.json').read_text())),download_dir=args.model.parent)
    profile=synthesis_profile(args.locale)
    model,lic,gender=MODELS[args.locale]
    assert args.model.name==model+'.onnx'
    dest=ROOT/'assets/voice/quest'/args.locale;dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.model.parent/'MODEL_CARD',dest/'MODEL_CARD.txt')
    manifest={'schema':3,'synthesis':profile,'locale':args.locale,'engine':'Piper 1.4.2 (development tool only)','model':model,'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),'model_source':'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-'+model+'.tar.bz2','dataset_license':lic,'voice_gender':gender,'runtime':'Bundled Vorbis only; no network, microphone, model or TTS engine','human_listening_review':'OPEN; independent synthetic voice, no actor imitation','clips':[]}
    old={}
    old_profile={}
    if (dest/'manifest.json').exists():
        previous=json.loads((dest/'manifest.json').read_text())
        old_profile=previous.get('synthesis',{})
        if previous.get('model_sha256')==manifest['model_sha256']:
            for row in previous['clips']:old[row['text']]=row
    done={}
    with tempfile.TemporaryDirectory(prefix='kinderwelt-voice.') as temp:
        for index,(id,text) in enumerate(narration_texts(args.locale).items()):
            applied=clip_profile(args.locale,id,text)
            cache_key=(text,json.dumps(applied,sort_keys=True))
            if cache_key in done:row=dict(done[cache_key])
            elif text in old and old[text].get('generation_profile',old_profile)==applied and valid_cached_audio(dest/old[text]['file'],old[text]['sha256']):
                row=dict(old[text]);done[cache_key]=row
            else:
                filename='voice_'+args.locale+'_'+hashlib.sha256((text+manifest['model_sha256']+json.dumps(applied,sort_keys=True)).encode()).hexdigest()[:20]+'.ogg'
                wav=Path(temp)/'speech.wav'
                chunks=list(voice.synthesize(text,SynthesisConfig(length_scale=applied['length_scale'],noise_scale=applied['noise_scale'],noise_w_scale=applied['noise_w_scale'],volume=applied['volume']),include_alignments=True))
                assert chunks and all(c.sample_rate==chunks[0].sample_rate and c.sample_width==2 and c.sample_channels==1 for c in chunks)
                rate=chunks[0].sample_rate
                units=[];offset=profile['lead_seconds']
                for chunk in chunks:
                    units.extend(speech_units(chunk,offset))
                    offset+=chunk.audio_float_array.size/rate+profile['sentence_pause_seconds']
                with wave.open(str(wav),'wb') as out:
                    out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate)
                    out.writeframes(b'\0'*(round(rate*profile['lead_seconds'])*2))
                    for n,chunk in enumerate(chunks):
                        # Keep every sample of every generated sentence, with a real pause.
                        out.writeframes(chunk.audio_int16_bytes)
                        if n<len(chunks)-1:out.writeframes(b'\0'*(round(rate*profile['sentence_pause_seconds'])*2))
                    out.writeframes(b'\0'*(round(rate*profile['tail_seconds'])*2))
                output=dest/filename
                encoding=encode_speech(wav,output)
                with wave.open(str(wav)) as out:seconds=out.getnframes()/out.getframerate()
                row={'text':text,'file':filename,'seconds':seconds,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
                row['encoding']=encoding
                row['phonetic_units']=units
                row['generation_profile']=applied
                done[cache_key]=dict(row)
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
