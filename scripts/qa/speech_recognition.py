#!/usr/bin/env python3
"""Optional local independent ASR comparison, never a listening certification.

Development dependencies: sherpa-onnx, NumPy, FFmpeg and a local multilingual
Whisper model. No download, task-text prompt or reference-text bias is used.
"""
import argparse,hashlib,json,re,subprocess,unicodedata
from pathlib import Path

def distance(a,b):
    row=list(range(len(b)+1))
    for i,left in enumerate(a,1):
        new=[i]
        for j,right in enumerate(b,1):new.append(min(new[-1]+1,row[j]+1,row[j-1]+(left!=right)))
        row=new
    return row[-1]

def normalized(text):
    return ' '.join(re.findall(r'[^\W_]+',unicodedata.normalize('NFC',text).casefold()))

def sample_ids():
    areas=['math','german','logic','physics','biology','chemistry','body','geography']
    ids=['area_'+s for s in areas]+['praise_'+str(i) for i in range(6)]+['again']
    # Fixed independent task examples, covering questions and hints in all subjects.
    tasks=['math_count','german_sun','logic_repeat','physics_05','biology_20','chemistry_20','body_20','geography_20']
    return ids+tasks+[id+'_hint' for id in tasks]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--threads',type=int,default=2)
    p.add_argument('--voices',type=Path,default=Path('assets/voice/quest'))
    p.add_argument('--locales',nargs='+',default=['de','en','ru'])
    p.add_argument('--output',type=Path,required=True)
    subset=p.add_mutually_exclusive_group()
    subset.add_argument('--ids',nargs='+',help='Explicit fixed comparison subset; reference text is still never prompted')
    subset.add_argument('--native-words',action='store_true',help='Screen all fifty native learning words; report target recovery separately from whole-question CER')
    a=p.parse_args()
    import numpy as np
    import sherpa_onnx
    encoder=a.model/'small-encoder.int8.onnx';decoder=a.model/'small-decoder.int8.onnx';tokens=a.model/'small-tokens.txt'
    model_files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [encoder,decoder,tokens]}
    report={'scope':'Independent ASR screening, not human intelligibility or exact word alignment; no reference-text prompting','model':'multilingual Whisper small, int8, sherpa-onnx','model_files':model_files,'locales':{}}
    tasks={t['id']:t for t in json.loads((Path(__file__).resolve().parents[2]/'games/quest/tasks.json').read_text())['tasks'] if t['subject']=='german'}
    for locale in a.locales:
        folder=a.voices/locale;manifest=json.loads((folder/'manifest.json').read_text());clips={c['id']:c for c in manifest['clips']}
        recognizer=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(encoder),decoder=str(decoder),tokens=str(tokens),language=locale,num_threads=a.threads)
        rows=[];errors=0;chars=0
        for id in (list(tasks) if a.native_words else a.ids or sample_ids()):
            c=clips[id];path=folder/c['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==c['sha256']
            pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),'-ar','16000','-ac','1','-f','f32le','-']),np.float32)
            stream=recognizer.create_stream();stream.accept_waveform(16000,pcm);recognizer.decode_stream(stream)
            actual=stream.result.text.strip();expected=normalized(c['text']).replace(' ','');recognized=normalized(actual).replace(' ','')
            count=distance(expected,recognized);errors+=count;chars+=len(expected)
            row={'id':id,'reference':c['text'],'recognized':actual,'character_errors':count,'reference_characters':len(expected),'seconds':round(len(pcm)/16000,4),'sha256':c['sha256']}
            if a.native_words:
                t=tasks[id];word=(t if locale=='de' else t['variants'][locale])['word']
                spelling=lambda s:normalized(s).replace(' ','').replace('ё','е')
                row.update(target_word=word,target_spelling_recovered=spelling(word) in spelling(actual))
            rows.append(row);print(locale,id,repr(actual),flush=True)
        report['locales'][locale]={'voice_model':manifest['model'],'samples':len(rows),'character_error_rate':round(errors/max(1,chars),5),'rows':rows}
        if a.native_words:
            report['locales'][locale]['target_spellings_recovered']=sum(r['target_spelling_recovered'] for r in rows)
            report['locales'][locale]['target_scope']='ASR spelling screen only; compound spacing and ё/е normalized; not heard stress or human intelligibility approval'
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Saved independent ASR screening:',a.output)
if __name__=='__main__':main()
