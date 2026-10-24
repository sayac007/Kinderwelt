#!/usr/bin/env python3
"""Compile finite speech vocabulary from pinned sources; models remain development-only.

Requires the existing Piper development environment (embedded eSpeak NG).
This is lexical/source validation, not an acoustic or human stress certification.
"""
import argparse,collections,hashlib,importlib.util,json,re,unicodedata,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
WORD=r"[^\W\d_]+(?:['’][^\W\d_]+)*"
NUCLEUS=re.compile(r'aɪ|aʊ|ɔɪ|eɪ|oʊ|əʊ|[aeiouyɑɐɒæəɚɛɜɝɞɪʊʌɔœøɶɯɤɨʉʏɘɵ]')
def unstress(s):return s.replace('ˈ','').replace('ˌ','')
def primary(ipa):
 mark=ipa.find('ˈ')
 return None if mark<0 else len(NUCLEUS.findall(ipa[:mark]))
def acute(s):
 out=''
 for c in s:
  if c=='+':
   if out and out[-1]!='ё':out+='\u0301'
  else:out+=c
 return out

def compile_lexicon(russian,cmu):
 import onnxruntime;onnxruntime.disable_telemetry_events()
 from piper.phonemize_espeak import EspeakPhonemizer
 phonemizer=EspeakPhonemizer()
 spec=importlib.util.spec_from_file_location('speech',ROOT/'scripts/generate-quest-voice.py');speech=importlib.util.module_from_spec(spec);spec.loader.exec_module(speech)
 sources=json.loads((ROOT/'scripts/voice/sources.json').read_text())
 for path,key in [(russian,'russian_g2p'),(cmu,'cmudict')]:
  if hashlib.sha256(path.read_bytes()).hexdigest()!=sources[key]['sha256']:raise ValueError('Wrong pronunciation source: '+str(path))
 homographs,forms=json.loads(zipfile.ZipFile(russian).read('Accents_new.json'))
 manual=dict(line.split('|') for line in (ROOT/'scripts/voice/russian-context.tsv').read_text().splitlines() if line)
 cmudict=collections.defaultdict(list)
 for line in cmu.read_text().splitlines():
  if not line or line.startswith(';;;'):continue
  spelling,*phones=line.split();cmudict[re.sub(r'\(\d+\)$','',spelling)].append(phones)
 result={'schema':1,'sources':sources,'scope':'Lexical stress guidance only; Qwen uses indirect written accents, English uses stress phonemes. No human/acoustic certification.','locales':{}}
 unresolved=[]
 vocab={lang:sorted({w.lower() for t in speech.narration_texts(lang).values() for w in re.findall(WORD,t)}) for lang in ['de','en','ru']}
 lookup=collections.defaultdict(set);russian_words=set(vocab['ru'])
 for form in forms:
  w=form.replace('+','')
  if w in russian_words:lookup[w].add(form)
 for w in vocab['ru']:
  if w in homographs:lookup[w].update(homographs[w].values())
 for lang in ['de','en','ru']:
  entries={}
  for word in vocab[lang]:
   ipa=' '.join(''.join(x) for x in phonemizer.phonemize({'de':'de','en':'en','ru':'ru'}[lang],word)).strip()
   row={'ipa':ipa,'primary_nucleus':primary(ipa),'synthesis':word,'source':'espeak-ng-development-phonemizer','control':'native spelling'}
   if lang=='ru':
    if word in manual:
     value=manual[word];row.update(source='reviewed-current-context',dictionary_variants=sorted(lookup[word]))
    elif sum(c in 'аеёиоуыэюя' for c in word)<=1:value=word;row['source']='single-vowel-or-no-vowel'
    elif len(lookup[word])==1:value=acute(next(iter(lookup[word])));row['source']='russian_g2p'
    elif 'ё' in word and not lookup[word]:value=word;row['source']='written-yo'
    else:unresolved.append((word,sorted(lookup[word])));value=word
    row.pop('ipa');row.pop('primary_nucleus')
    vowels=[i for i,c in enumerate(value) if c in 'аеёиоуыэюя']
    stressed=[n for n,i in enumerate(vowels) if value[i]=='ё' or value[i+1:i+2]=='\u0301']
    row.update(synthesis=value,primary_vowel=(stressed[0] if stressed else 0 if len(vowels)==1 else None),control='indirect written stress; not a guaranteed phoneme command')
   elif lang=='de':
    nuclei=list(re.finditer(r'(?i)(?:au|äu|eu|ei|ai|ie|[aeiouyäöü])',word))
    n=primary(ipa);phone_count=len(NUCLEUS.findall(ipa))
    if len(nuclei)>1 and len(nuclei)==phone_count and n is not None and n<len(nuclei):
     at=nuclei[n].start();row['synthesis']=word[:at+1]+'\u0301'+word[at+1:];row['control']='indirect written stress; not a guaranteed phoneme command'
   else:
    phones=cmudict.get(word,[]);indices={next((i for i,p in enumerate(p for p in group if re.search('[012]$',p)) if p.endswith('1')),None) for group in phones}
    count=len(NUCLEUS.findall(ipa));variants=[sum(bool(re.search('[012]$',p)) for p in group) for group in phones]
    if len(indices)==1 and None not in indices and variants and all(n==count for n in variants):
     n=indices.pop();bare=unstress(ipa);positions=list(NUCLEUS.finditer(bare))
     row.update(source='cmudict-and-espeak-ng',primary_nucleus=n,requires_primary_correction=count>1 and primary(ipa)!=n)
     if n<len(positions):
      markers={positions[n].start():'ˈ'}
      for mark in re.finditer('ˌ',ipa):
       secondary=len(NUCLEUS.findall(ipa[:mark.start()]))
       if secondary<len(positions) and secondary!=n:markers[positions[secondary].start()]='ˌ'
      row['controlled_ipa']=''.join(markers.get(i,'')+c for i,c in enumerate(bare));row['control']='explicit stress phoneme on matching phonetic word'
    else:row['control']='native contextual eSpeak pronunciation; ambiguous or unmatched CMU form'
   entries[word]=row
  result['locales'][lang]=entries
 if unresolved:raise ValueError('Unreviewed Russian stress: '+repr(unresolved))
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--russian',type=Path,required=True);p.add_argument('--cmu',type=Path,required=True);p.add_argument('--output',type=Path,default=ROOT/'scripts/voice/pronunciations.json');a=p.parse_args()
 data=compile_lexicon(a.russian,a.cmu);a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Compiled words:',{l:len(v) for l,v in data['locales'].items()})
if __name__=='__main__':main()
