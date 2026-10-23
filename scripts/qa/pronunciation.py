#!/usr/bin/env python3
"""Check lexical coverage and delivered synthesis provenance, never certify heard stress."""
import argparse,hashlib,importlib.util,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/voice'))
import pronunciation as guidance

def speech_source():
 spec=importlib.util.spec_from_file_location('pronunciation_speech',ROOT/'scripts/generate-quest-voice.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def inspect(voices=None):
 source=speech_source();data=guidance.lexicon();failures=[];report={}
 for locale in ['de','en','ru']:
  texts=source.narration_texts(locale);words={w.lower() for t in texts.values() for w in guidance.WORDS.findall(t)};entries=data['locales'][locale]
  if words-set(entries):failures.append(locale+': missing lexical entries '+repr(sorted(words-set(entries))))
  if locale=='ru':
   for word in words:
    row=entries.get(word,{})
    if sum(c in 'аеёиоуыэюя' for c in word)>1 and row.get('primary_vowel') is None:failures.append('ru: unresolved stress '+word)
    if row.get('synthesis','').replace('\u0301','')!=word:failures.append('ru: changed letters in stress reference '+word)
  for id,text in texts.items():
   try:proof=guidance.utterance(text,locale)
   except ValueError as e:failures.append(str(e));continue
   if locale=='ru' and re.search('[A-Za-z]',proof['synthesis_text']):failures.append('ru: foreign spelling in '+id)
  report[locale]={'written_words':len(words),'utterances':len(texts),'lexical_coverage':'PASS' if not words-set(entries) else 'FAIL'}
  if voices:
   manifest=json.loads((voices/locale/'manifest.json').read_text());clips=manifest['clips']
   if {r['id']:r['text'] for r in clips}!=texts:failures.append(locale+': incomplete or stale voice/text bindings')
   for row in clips:
    if row.get('pronunciation')!=guidance.utterance(row['text'],locale):failures.append(locale+': synthesis guidance drift '+row['id'])
    if locale!='en':
     digest=row.get('generation_batch_sha256');batch=manifest.get('generation_batches',{}).get(digest)
     if batch is None or hashlib.sha256(json.dumps(batch,ensure_ascii=False).encode()).hexdigest()!=digest:failures.append(locale+': missing generation batch '+row['id'])
     elif row['pronunciation']['synthesis_text'] not in batch:failures.append(locale+': guidance not actually sent to model '+row['id'])
   report[locale]['delivered_mappings']=len(clips)
 return {'status':'FAIL' if failures else 'PASS','failures':sorted(set(failures)),'locales':report,
         'scope':'Finite written-vocabulary coverage and actual synthesis-input provenance, not automatic certification of acoustic stress',
         'voices':'Existing female Serena DE/RU and LJSpeech EN preserved',
         'heard_word_stress':'OPEN: dictionary/phoneme guidance and ASR do not prove every spoken syllable stress'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--voices',type=Path);p.add_argument('--output',type=Path,default=ROOT/'qa-results/pronunciation.json');a=p.parse_args();r=inspect(a.voices);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print('Pronunciation:',r['status'],r['locales'],'; heard stress review OPEN')
 for error in r['failures']:print(error)
 raise SystemExit(1 if r['failures'] else 0)
if __name__=='__main__':main()
