"""Pronunciation data and context, independently of a subjective acoustic claim."""
import hashlib,importlib.util,json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('guidance_tests',ROOT/'scripts/voice/pronunciation.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class PronunciationTests(unittest.TestCase):
 def test_pinned_sources_have_real_notices_and_dictionary_identity(self):
  data=g.lexicon()['sources']
  self.assertEqual(data['russian_g2p']['revision'],'20305523bfe4ccb632c7538e9a5e925bde54b52e')
  self.assertEqual(data['russian_g2p']['sha256'],'9a85c8dabfba5d0a8acc6a634cbb06110b602813c3034185762c126042ad02bf')
  for p in (ROOT/'scripts/voice/licenses').glob('*.txt'):self.assertIn('Copyright',p.read_text())
 def test_every_current_spoken_word_has_lexical_guidance(self):
  spec=importlib.util.spec_from_file_location('pron_qa_test',ROOT/'scripts/qa/pronunciation.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
  r=q.inspect();self.assertEqual(r['failures'],[]);self.assertIn('OPEN',r['heard_word_stress'])
 def test_new_unknown_words_are_not_silently_accepted(self):
  with self.assertRaisesRegex(ValueError,'Unreviewed speech word'):g.utterance('Несуществующееслово.','ru')
 def test_context_sensitive_russian_stress(self):
  words=g.lexicon()['locales']['ru']
  self.assertEqual(words['оси']['synthesis'],'оси́')
  self.assertEqual(words['органы']['synthesis'],'о́рганы')
  self.assertEqual(words['белки']['synthesis'],'бе́лки')
  self.assertEqual(g.referenced_word('руки','Чем ополоснуть руки?','ru')['primary_vowel'],0)
  self.assertEqual(g.referenced_word('руки','Внутри руки','ru')['primary_vowel'],1)
  self.assertIn("ру'ки",g.utterance('Чем ополоснуть руки?','ru')['synthesis_text'])
  self.assertIn("руки'",g.utterance('Внутри руки','ru')['synthesis_text'])
  self.assertIn("о'блака",g.utterance('Облака закрывают.','ru')['synthesis_text'].lower())
  self.assertIn("облака'",g.utterance('Из облака','ru')['synthesis_text'].lower())
  self.assertIn("ноги'",g.utterance('У взрослого четыре ноги.','ru')['synthesis_text'])
  self.assertIn("но'ги",g.utterance('Вырастают ноги.','ru')['synthesis_text'])
  self.assertIn("бе'рега",g.utterance('Два берега.','ru')['synthesis_text'].lower())
  self.assertIn("бе'рега",g.utterance('Соединяет оба берега.','ru')['synthesis_text'])
 def test_native_voices_and_clean_visible_spelling_remain_separate(self):
  self.assertEqual(g.utterance('Which two letters are missing?','en')['synthesis_text'],'Which two letters are missing?')
  self.assertEqual(g.utterance('Welche beiden Buchstaben fehlen?','de')['synthesis_text'],'Welche beiden Buchstaben fehlen?')
  self.assertIn('Physík',g.utterance('Physik.','de')['synthesis_text'])
  self.assertIn('OPEN',g.utterance('Physik.','de')['acoustic_stress_review'])
  self.assertEqual(g.utterance('Домик. Какие две буквы пропущены?','ru')['synthesis_text'],'Домик. Какие две буквы пропущены?')
 def test_cmu_primary_stress_keeps_secondary_and_all_phonemes(self):
  row=g.lexicon()['locales']['en']['mathematics']
  self.assertEqual(row['primary_nucleus'],2);self.assertIn('ˌ',row['controlled_ipa'])
  stripped=lambda s:s.replace('ˈ','').replace('ˌ','')
  self.assertEqual(stripped(row['ipa']),stripped(''.join(g.english_phonemes(list(row['ipa'])))))
 def test_english_contextual_weak_stress_is_preserved(self):
  self.assertEqual(''.join(g.english_phonemes(list('wˌɪtʃ ɪz juː.'))),'wˌɪtʃ ɪz juː.')
  row=g.lexicon()['locales']['en']['conducts']
  self.assertTrue(row['requires_primary_correction'])
  self.assertEqual(''.join(g.english_phonemes(list(row['ipa']))),row['controlled_ipa'])
 def test_audio_reuse_requires_exact_original_input_and_preserves_generation_metadata(self):
  sys.path.insert(0,str(ROOT/'scripts/voice'))
  from reuse import exact_input_rows
  batch=['Mensch.','Physik.'];key=hashlib.sha256(json.dumps(batch,ensure_ascii=False).encode()).hexdigest()
  bank={'locale':'de','speaker':'Serena','model_sha256':'model','model_revision':'revision','speech_tokenizer_sha256':'tokenizer',
        'generation_batches':{key:batch},'clips':[{'id':str(i),'text':text,'file':str(i)+'.ogg','generation_batch_sha256':key,'generation_profile':{'revision':'original'},'seed':123} for i,text in enumerate(batch)]}
  wanted={'same':'Mensch.','changed':'Physik.'}
  rows=exact_input_rows(bank,bank,wanted,'de','manifest')
  self.assertEqual(set(rows),{'Mensch.'}) # Physik now has an actual written stress cue.
  self.assertEqual(rows['Mensch.']['seed'],123)
  self.assertEqual(rows['Mensch.']['generation_profile'],{'revision':'original'})
  self.assertIn('not regenerated',rows['Mensch.']['pronunciation_review']['policy'])
  self.assertNotIn('pronunciation',bank['clips'][0])
  self.assertFalse(exact_input_rows(bank,dict(bank,speaker='Other'),wanted,'de','manifest'))
  bank['generation_batches'][key].append('tampered')
  self.assertFalse(exact_input_rows(bank,bank,wanted,'de','manifest'))
 def test_resume_skips_retired_text_before_looking_up_its_old_vocabulary(self):
  sys.path.insert(0,str(ROOT/'scripts/voice'))
  from reuse import reviewed_current_rows
  current='Это физика.'
  prior={'clips':[{'text':'Несуществующееслово.'},{'text':current,'pronunciation':g.utterance(current,'ru')}]}
  self.assertEqual(set(reviewed_current_rows(prior,{'area':current},'ru')),{current})
  with self.assertRaisesRegex(ValueError,'Unreviewed speech word'):
   reviewed_current_rows(prior,{'new':'Несуществующееслово.'},'ru')
 def test_piper_reuse_requires_actual_phonemes_and_synthesis_parameters_to_match(self):
  from copy import deepcopy
  sys.path.insert(0,str(ROOT/'scripts/voice'))
  from reuse import reviewed_piper_row
  bank={'locale':'en','model':'LJSpeech','model_sha256':'weights','voice_gender':'female'}
  old={'text':'English.','generation_profile':{'revision':'original','length_scale':1.18},'phonetic_units':[{'phonemes':'ˈɪŋɡlɪʃ.'}],'sha256':'original-audio'}
  current=dict(old,generation_profile={'revision':'new','length_scale':1.18},pronunciation=g.utterance('English.','en'))
  row=reviewed_piper_row(old,current,bank,bank,'source-manifest')
  self.assertEqual(row['sha256'],'original-audio');self.assertEqual(row['generation_profile']['revision'],'original')
  self.assertEqual(row['pronunciation_review']['reviewed_generation_profile'],current['generation_profile'])
  changed=deepcopy(current);changed['phonetic_units'][0]['phonemes']='different'
  self.assertIsNone(reviewed_piper_row(old,changed,bank,bank,'source'))
  changed=deepcopy(current);changed['generation_profile']['length_scale']=1.5
  self.assertIsNone(reviewed_piper_row(old,changed,bank,bank,'source'))
  self.assertIsNone(reviewed_piper_row(old,current,bank,dict(bank,model_sha256='other'),'source'))
 def test_complete_listening_page_handles_sharp_s_and_all_native_words(self):
  import tempfile
  spec=importlib.util.spec_from_file_location('listening_test',ROOT/'scripts/qa/listening_pack.py');page=importlib.util.module_from_spec(spec);spec.loader.exec_module(page)
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'listening.html';page.generate(path);document=path.read_text()
  data=json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>',document,re.S).group(1))
  actual={(r['locale'],r['id']) for r in data}
  words=[t['id'] for t in json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks'] if t['subject']=='german']
  for locale in ['de','en','ru']:
   for id in words:self.assertIn((locale,id),actual)
  self.assertIn('Fußabdruck',document)
  self.assertIn('CMUdict-BSD.txt',document)
  self.assertIn('russian-g2p-MIT.txt',document)
