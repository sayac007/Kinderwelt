"""Apply reviewed finite-vocabulary guidance without altering displayed text.

Qwen's built-in Serena has no phoneme interface. Written guidance is indirect;
this module must never be reported as an acoustic or human listening pass.
"""
import functools,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
WORDS=re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
REVISION='lexical-stress-1'
@functools.lru_cache(maxsize=1)
def lexicon():return json.loads((ROOT/'scripts/voice/pronunciations.json').read_text())
@functools.lru_cache(maxsize=1)
def controls():return json.loads((ROOT/'scripts/voice/controls.json').read_text())
@functools.lru_cache(maxsize=1)
def context_rules():return json.loads((ROOT/'scripts/voice/russian-contexts.json').read_text())['rules']
def preserve_case(value,original):
 if original.isupper():return value.upper()
 if original[:1].isupper():return value[:1].upper()+value[1:]
 return value

def referenced_word(word,text,locale):
 entry=dict(lexicon()['locales'][locale][word])
 if locale=='ru':
  for rule in context_rules():
   if rule['word']==word and re.search(rule['when'],text,re.I):
    value=rule['synthesis'];vowels=[i for i,c in enumerate(value) if c in 'аеёиоуыэюя']
    primary=next((n for n,i in enumerate(vowels) if value[i]=='ё' or value[i+1:i+2]=='\u0301'),0 if len(vowels)==1 else None)
    entry.update(synthesis=value,primary_vowel=primary,source='reviewed-sentence-context',context_rule=rule)
 return entry

def utterance(text,locale):
 entries=lexicon()['locales'][locale];used=[]
 def replace(match):
  original=match.group();key=original.lower()
  if key not in entries:raise ValueError('Unreviewed speech word: '+locale+'/'+original)
  entry=referenced_word(key,text,locale)
  value=entry['synthesis']
  if locale=='de' and key not in controls()['de_written_stress_words']:
   value=original
   entry['control']='native German spelling; lexical stress reference retained'
  if locale=='ru':
   if key in controls()['ru_written_stress_words']:value=value.replace('\u0301',"'")
   else:
    value=original
    entry['control']='native Russian spelling; lexical stress reference retained'
  # Written Russian stress is converted to the separately screened input cue.
  # The visible/spoken reference retains its ordinary spelling.
  used.append({'word':key,**entry})
  if locale=='en':return original
  return preserve_case(value,original)
 synthesis=WORDS.sub(replace,text)
 if locale=='en':synthesis=text
 proof={'revision':REVISION,'locale':locale,'text':text,'synthesis_text':synthesis,'words':used}
 return {'synthesis_text':synthesis,'word_count':len(used),
         'sha256':hashlib.sha256(json.dumps(proof,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
         'control':'stress phonemes where matched; native contextual fallback' if locale=='en' else 'screened written stress cues; native German spelling otherwise' if locale=='de' else 'screened apostrophe cues; native Russian spelling otherwise',
         'acoustic_stress_review':'OPEN; lexical contract and ASR do not certify heard syllable stress'}

@functools.lru_cache(maxsize=1)
def english_corrections():
 candidates={};conflicts=set()
 for entry in lexicon()['locales']['en'].values():
  # Do not turn weak contextual stress into primary stress on every function
  # word. Only a genuine multisyllabic lexical mismatch needs a correction.
  if 'controlled_ipa' not in entry or not entry.get('requires_primary_correction'):continue
  original=entry['ipa'];key=original.replace('ˈ','').replace('ˌ','')
  if key in candidates and candidates[key]!=entry['controlled_ipa']:conflicts.add(key)
  candidates[key]=entry['controlled_ipa']
 return {key:value for key,value in candidates.items() if key not in conflicts}

def english_phonemes(phonemes):
 mapping=english_corrections()
 def replace(match):
  unit=match.group();body=unit.rstrip('.,!?;:');punctuation=unit[len(body):]
  key=body.replace('ˈ','').replace('ˌ','')
  return mapping.get(key,body)+punctuation
 return list(re.sub(r'\S+',replace,''.join(phonemes)))
