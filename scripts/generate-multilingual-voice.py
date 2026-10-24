#!/usr/bin/env python3
"""Generate offline female DE/RU recordings from a pinned local Qwen3 model.

Development only. No model, Python, network or TTS engine enters the app.
English remains the existing LJSpeech voice. No human reference recording.
"""
import argparse,hashlib,importlib.util,json,math,os,re,shutil,tempfile,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/voice'))
import pronunciation
from reuse import reviewed_current_rows
MODEL='Qwen3-TTS-12Hz-0.6B-CustomVoice'
REVISION='85e237c12c027371202489a0ec509ded67b5e4b5'
MODEL_SHA='bc3c7e785eb961179c25450d1acff03f839e0002f2f3a5aeb67b5735c0fa2adb'
TOKENIZER_SHA='836b7b357f5ea43e889936a3709af68dfe3751881acefe4ecf0dbd30ba571258'
SOURCE='https://huggingface.co/Qwen/'+MODEL+'/tree/'+REVISION
LANGUAGES={'de':'German','ru':'Russian'}
def synthesis_profile(speaker='Serena',batch_size=48):
    return {'revision':'female-lexical-stress-3','pronunciation_revision':pronunciation.REVISION,'decoder_batch_size':4,'speaker':speaker,'precision':'bfloat16',
            'attention':'sdpa','batch_size':batch_size,'do_sample':True,'subtalker_dosample':True,'temperature':.65,'top_p':.85,'top_k':30,
            'lead_seconds':.20,'tail_seconds':.40,'waveform_policy':'Complete decoder output, no trimming, pitch or formant conversion',
            'duration_alignment':'not available; no fabricated word timestamps',
            'sentence_pause_seconds':None,'runtime_sample_rate':22050}
def verify_model(root):
    contract=json.loads((ROOT/'scripts/qa/qwen-source.json').read_text())
    if contract['revision']!=REVISION:raise ValueError('Unexpected Qwen model revision')
    for row in contract['files']+contract['notices']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Invalid model resource path')
        file=root/rel
        if file.stat().st_size!=row['size'] or hashlib.sha256(file.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Unexpected official model resource: '+str(rel))
def load_source():
    spec=importlib.util.spec_from_file_location('speech_source',ROOT/'scripts/generate-quest-voice.py')
    source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source);return source

def calibrate_playback(manifest):
    if manifest.get('model')!=MODEL or manifest.get('speaker') not in ['Serena','Ono_Anna','Sohee']:
        raise ValueError('Playback calibration is only for the reviewed female bank')
    manifest['playback_level']={'method':'Static gain from decoded Vorbis peak; applied by player, no audio re-encoding',
                                'target_peak':.70,'minimum_gain_db':-6.,'maximum_gain_db':20.}
    for row in manifest['clips']:
        peak=row['encoding']['decoded_peak']
        if not .005<peak<=.999:raise ValueError('Invalid measured encoded peak')
        gain=max(-6.,min(20.,20*math.log10(.70/peak)))
        if not .60<=peak*10**(gain/20)<=.701:raise ValueError('Voice too quiet for safe calibration: '+row['id'])
        row['playback_gain_db']=round(gain,6)
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--locale',choices=LANGUAGES,required=True);p.add_argument('--model',type=Path)
    p.add_argument('--calibrate-only',action='store_true',help='Update measured playback gain in an existing complete manifest; no model or audio changes')
    p.add_argument('--output',type=Path,required=True,help='Voice-bank root; start in build/ for review before installation')
    p.add_argument('--speaker',choices=['Serena','Ono_Anna','Sohee'],default='Serena')
    p.add_argument('--threads',type=int,default=4);p.add_argument('--batch-size',type=int,default=48);p.add_argument('--ids',nargs='+')
    p.add_argument('--reuse-bank',type=Path,help='Existing locale folder; only provably identical original model inputs can be reused')
    a=p.parse_args()
    if not 1<=a.batch_size<=64:p.error('Batch size must be between 1 and 64')
    if a.calibrate_only:
        import fcntl
        path=a.output/a.locale/'manifest.json'
        with (path.parent/'.generation.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            manifest=json.loads(path.read_text())
            if {c['id']:c['text'] for c in manifest['clips']}!=load_source().narration_texts(a.locale):
                raise ValueError('Refusing to calibrate an incomplete or stale delivery bank')
            calibrate_playback(manifest)
            checkpoint=path.with_suffix('.json.tmp');checkpoint.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');checkpoint.replace(path)
        print('Calibrated',a.locale,len(manifest['clips']),'mappings; audio bytes unchanged');return
    if a.model is None:p.error('--model is required for synthesis')
    verify_model(a.model)
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    os.environ.setdefault('OMP_WAIT_POLICY','PASSIVE');os.environ.setdefault('KMP_BLOCKTIME','0')
    import numpy as np
    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel
    torch.set_num_threads(a.threads)
    source=load_source();profile=synthesis_profile(a.speaker,a.batch_size)
    texts=source.narration_texts(a.locale)
    if a.ids:texts={key:texts[key] for key in a.ids}
    dest=a.output/a.locale;dest.mkdir(parents=True,exist_ok=True)
    import fcntl
    lock_file=(dest/'.generation.lock').open('a')
    fcntl.flock(lock_file,fcntl.LOCK_EX)  # Only one writer per locale; kernel releases on interruption.
    manifest={'schema':4,'locale':a.locale,'engine':'Qwen3-TTS 0.1.1 (development only)',
              'model':MODEL,'model_sha256':MODEL_SHA,'model_source':SOURCE,'model_revision':REVISION,
              'speech_tokenizer_sha256':TOKENIZER_SHA,'speaker':a.speaker,
              'model_license':'Apache-2.0','dataset_license':'Not separately specified by publisher',
              'voice_gender':'female','synthesis':profile,'runtime':'Bundled Vorbis only; no network, microphone, model or TTS engine',
              'human_listening_review':'OPEN; built-in synthetic female speaker, no actor imitation',
              'clips':[]}
    shutil.copy2(a.model/'README.md',dest/'MODEL_CARD.txt')
    shutil.copy2(a.model/'LICENSE.txt',dest/'LICENSE.txt')
    prior={}
    if (dest/'manifest.json').is_file():
        previous=json.loads((dest/'manifest.json').read_text())
        manifest['generation_batches']=previous.get('generation_batches',{})
        legacy={**profile,'revision':'female-multilingual-1','do_sample':False,'subtalker_dosample':False}
        for key in ['temperature','top_p','top_k']:legacy.pop(key)
        if previous.get('synthesis') in [profile,legacy,dict(profile,batch_size=32),dict(profile,batch_size=16),dict(legacy,batch_size=32),dict(legacy,batch_size=16)] and previous.get('model_sha256')==MODEL_SHA and previous.get('speaker')==a.speaker:
            prior=reviewed_current_rows(previous,texts,a.locale)
    if a.reuse_bank:
        from reuse import exact_input_rows
        original_manifest=(a.reuse_bank/'manifest.json').read_bytes()
        original=json.loads(original_manifest)
        reusable=exact_input_rows(original,manifest,texts,a.locale,hashlib.sha256(original_manifest).hexdigest())
        adopted=0
        for text,row in reusable.items():
            if text in prior:continue
            path=a.reuse_bank/row['file']
            if not source.valid_cached_audio(path,row['sha256']):continue
            shutil.copy2(path,dest/row['file']);prior[text]=row;adopted+=1
        manifest.setdefault('generation_batches',{}).update(original.get('generation_batches',{}))
        print('Reused',adopted,'unchanged recordings with exact original input proof; original synthesis metadata retained',flush=True)
    model=None;done={};start=time.monotonic()
    spec=importlib.util.spec_from_file_location('asr_sample_ids',ROOT/'scripts/qa/speech_recognition.py')
    screening=importlib.util.module_from_spec(spec);spec.loader.exec_module(screening)
    priority={texts[id] for id in screening.sample_ids() if id in texts}
    word_ids=[t['id'] for t in json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks'] if t['subject']=='german']
    priority.update(texts[id] for id in word_ids if id in texts)
    unique=sorted(set(texts.values()),key=lambda t:(t not in priority,len(t),t))
    for text in unique:
        if text in prior and source.valid_cached_audio(dest/prior[text]['file'],prior[text]['sha256']):done[text]=prior[text]
    def checkpoint():
        rows=[];batches=manifest.setdefault('generation_batches',{})
        for id,text in texts.items():
            if text not in done:continue
            row=dict(done[text],id=id)
            if 'generation_batch' in row:
                batch=row.pop('generation_batch');key=hashlib.sha256(json.dumps(batch,ensure_ascii=False).encode()).hexdigest()
                batches[key]=batch;row['generation_batch_sha256']=key
            rows.append(row)
        manifest['clips']=rows
        calibrate_playback(manifest)
        checkpoint_path=dest/'manifest.json.tmp'
        checkpoint_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        checkpoint_path.replace(dest/'manifest.json')
    def synthesize(batch,sampling=False,attempt=0):
        nonlocal model
        if model is None:
            model=Qwen3TTSModel.from_pretrained(str(a.model),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
            print('Loaded official local Qwen3 model; offline',flush=True)
        spoken=[pronunciation.utterance(text,a.locale)['synthesis_text'] for text in batch]
        seed=(int(hashlib.sha256((a.locale+json.dumps(spoken,ensure_ascii=False)).encode()).hexdigest()[:8],16)+104729*attempt)%2**32
        torch.manual_seed(seed)
        # Compounds and number sequences expand beyond a simple written-word
        # estimate. Leave room to finish; the independent duration guard still
        # rejects repetitions before waveform decoding.
        budget=min(480,max(96,max(len(re.findall(r'\w+',t)) for t in batch)*12+64+32*attempt))
        kwargs={'do_sample':sampling,'subtalker_dosample':sampling,'max_new_tokens':budget}
        if sampling:kwargs.update(temperature=.65+.05*max(0,attempt-1),top_p=.85,top_k=30,subtalker_temperature=.65)
        decoder=model.model.speech_tokenizer.decode
        def checked_decode(items):
            # Inspect codec length before waveform decoding. A failed EOS must
            # not force every valid item through a huge padded audio batch.
            waves=[None]*len(items);output_rate=24000;valid=[]
            for index,(text,item) in enumerate(zip(batch,items)):
                seconds=item['audio_codes'].shape[0]/12.5
                words=len(re.findall(r'\w+',text))
                if seconds>=(budget-2)/12.5 or seconds>max(5.,1.1*words+2):
                    print('Reject codec overrun before decoding:',repr(text),round(seconds,2),flush=True)
                    waves[index]=np.zeros(0,np.float32);continue
                valid.append(index)
            # Bound waveform-decoder memory independently of the text batch.
            # Length buckets limit padding; official decode retains each item's
            # complete original length. Four items fit the 32-GiB environment.
            valid.sort(key=lambda i:items[i]['audio_codes'].shape[0])
            for offset in range(0,len(valid),profile['decoder_batch_size']):
                indexes=valid[offset:offset+profile['decoder_batch_size']]
                decoded,output_rate=decoder([items[i] for i in indexes])
                if len(decoded)!=len(indexes):raise ValueError('Incomplete decoder batch')
                for index,waveform in zip(indexes,decoded):waves[index]=waveform
            return waves,output_rate
        model.model.speech_tokenizer.decode=checked_decode
        try:
            wavs,rate=model.generate_custom_voice(text=spoken,language=LANGUAGES[a.locale],speaker=a.speaker,**kwargs)
        finally:model.model.speech_tokenizer.decode=decoder
        if len(wavs)!=len(batch):raise ValueError('Missing batch output')
        return wavs,rate,seed,budget,kwargs
    with tempfile.TemporaryDirectory(prefix='kinderwelt-female.') as tmp:
        # An explicit existing bank is a new incremental generation operation.
        # Compact its missing inputs; actual new batch/seed are recorded below.
        # Never synthesize hundreds of already verified clips just for padding.
        work=[text for text in unique if text not in done] if a.reuse_bank else unique
        for offset in range(0,len(work),a.batch_size):
            # Keep the original grouping on resume: changes in batch shape can
            # affect numerical rounding even with deterministic greedy decoding.
            group=work[offset:offset+a.batch_size]
            if all(text in done for text in group):continue
            print(a.locale,'synthesizing',len(group),'inputs;',len(done),'of',len(unique),'verified',flush=True)
            wavs,rate,seed,budget,kwargs=synthesize(group,sampling=True)
            for text,waveform in zip(group,wavs):
                if text in done:continue
                pcm=np.asarray(waveform,dtype=np.float32)
                if pcm.ndim!=1 or not np.isfinite(pcm).all():raise ValueError('Invalid synthesized waveform: '+text)
                words=len(re.findall(r'\w+',text))
                duration=len(pcm)/rate
                actual_seed,actual_budget,actual_kwargs=seed,budget,kwargs
                if duration>=(budget-2)/12.5 or duration>max(4.,.9*words+2) or duration<max(.45,.10*words):
                    print('Retry abnormal duration with recorded sampling parameters:',repr(text),duration,flush=True)
                    for attempt in range(1,5):
                        retry,rate,actual_seed,actual_budget,actual_kwargs=synthesize([text],sampling=True,attempt=attempt)
                        pcm=np.asarray(retry[0],dtype=np.float32);duration=len(pcm)/rate
                        if np.isfinite(pcm).all() and max(.45,.10*words)<=duration<(actual_budget-2)/12.5 and duration<=max(5.,1.1*words+2) and float(np.max(np.abs(pcm)))>.01:break
                        print('Rejected retry',attempt,repr(text),'seconds',duration,flush=True)
                    else:
                        checkpoint();raise ValueError('Failed all bounded duration attempts; not installed: '+text)
                peak=float(np.max(np.abs(pcm)))
                if peak<.01:raise ValueError('Silent synthesized waveform: '+text)
                gain=min(1.,.78/peak)
                padded=np.concatenate([np.zeros(round(rate*profile['lead_seconds']),np.float32),pcm*gain,np.zeros(round(rate*profile['tail_seconds']),np.float32)])
                wav=Path(tmp)/'complete.wav';sf.write(wav,padded,rate,subtype='PCM_16')
                filename='voice_'+a.locale+'_'+hashlib.sha256((text+MODEL_SHA+json.dumps(profile,sort_keys=True)+str(actual_seed)+json.dumps(actual_kwargs,sort_keys=True)+pronunciation.utterance(text,a.locale)['sha256']).encode()).hexdigest()[:20]+'.ogg'
                target=dest/filename;encoding=source.encode_speech(wav,target)
                row={'text':text,'file':filename,'seconds':len(padded)/rate,'synthesized_seconds':duration,
                     'source_sample_rate':rate,'source_samples':len(pcm),'source_waveform_sha256':hashlib.sha256(pcm.tobytes()).hexdigest(),
                     'uniform_waveform_gain':gain,'synthesis_threads':a.threads,'encoding':encoding,'generation_profile':profile,'seed':actual_seed,
                     'generation_parameters':actual_kwargs,
                     'pronunciation':pronunciation.utterance(text,a.locale),
                     'generation_batch':[pronunciation.utterance(t,a.locale)['synthesis_text'] for t in (group if actual_seed==seed else [text])],
                     'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
                done[text]=row
                checkpoint()
            print(a.locale,'unique',len(done),'/',len(unique),'mappings',len(manifest['clips']),'wall',round(time.monotonic()-start),flush=True)
    checkpoint()
    if not a.ids:
        referenced={r['generation_batch_sha256'] for r in manifest['clips']}
        manifest['generation_batches']={key:value for key,value in manifest['generation_batches'].items() if key in referenced}
        (dest/'manifest.json.tmp').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        (dest/'manifest.json.tmp').replace(dest/'manifest.json')
        keep={c['file'] for c in manifest['clips']}
        for path in dest.glob('voice_*.ogg'):
            if path.name not in keep:path.unlink();path.with_suffix('.ogg.import').unlink(missing_ok=True)
    print(a.locale,len(texts),'mappings;',len(done),'unique; seconds',round(time.monotonic()-start),flush=True)
if __name__=='__main__':main()
