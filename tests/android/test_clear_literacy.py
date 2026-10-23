"""Visible puzzles must not disclose their spelling or lose letter positions."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class ClearLiteracyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
 def test_fifty_stations_each_language_and_existing_ids_preserved(self):
  self.assertEqual(len(self.tasks),400)
  self.assertEqual(len({t['id'] for t in self.tasks}),400)
  old=set(json.loads((ROOT/'games/quest/legacy-rewards.json').read_text())['rewards'])
  self.assertTrue(old <= {t['id'] for t in self.tasks})
  for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
   tasks=[t for t in self.tasks if t['subject']==subject];self.assertEqual(len(tasks),50)
   for t in tasks:
    for child in [t,*t['bonuses']]:self.assertEqual(set(child['texts']),{'de','en','ru'})
   self.assertEqual({t['id'] for t in tasks if t['id'] not in old},{f'{subject}_{n:02d}' for n in range(41,51)})
 def test_visible_word_hidden_but_native_audio_has_a_spelling_cue(self):
  for parent in self.tasks:
   if parent['subject']!='german':continue
   for t in [parent,*parent['bonuses']]:
    for lang in ['de','en','ru']:
     v=t if lang=='de' else t['variants'][lang];text=t['texts'][lang]
     self.assertNotIn(v['word'].casefold(),text['prompt'].casefold())
     self.assertIn(v['word'].casefold(),text['spoken_prompt'].casefold())
     self.assertNotIn(v['word'].casefold(),text['tip'].casefold())
 def test_simple_slots_and_positioned_answer_rows(self):
  for parent in self.tasks:
   if parent['subject']!='german':continue
   for t in [parent,*parent['bonuses']]:
    for lang in ['de','en','ru']:
     v=t if lang=='de' else t['variants'][lang];word=v['word'];mask=v['display']
     self.assertEqual(len(mask),len(word));self.assertNotIn('＿',mask)
     holes=[i for i,c in enumerate(mask) if c=='_'];self.assertEqual(holes,v['missing_positions'])
     self.assertEqual(''.join(word[i] for i in holes),v['answer'])
     for option in v['options']:
      pattern=v['option_displays'][option];self.assertEqual(len(pattern),len(word))
      self.assertEqual([i for i,c in enumerate(pattern) if c!='_'],holes)
      self.assertEqual(''.join(pattern[i] for i in holes),option)
      self.assertTrue(all(mask[i]==word[i] for i in range(len(word)) if i not in holes))
 def test_russian_rows_only_cyrillic_and_underscores(self):
  for p in self.tasks:
   if p['subject']!='german':continue
   for t in [p,*p['bonuses']]:
    v=t['variants']['ru']
    for text in [v['display'],*v['option_displays'].values()]:self.assertRegex(text,r'^[А-ЯЁ_]+$')
 def test_russian_science_audio_keeps_every_written_comparison_clause(self):
  for parent in self.tasks:
   if parent['subject'] not in ['physics','biology','chemistry','body','geography']:continue
   for i,task in enumerate(parent['bonuses']):
    text=task['texts']['ru'];written=text['prompt'];spoken=text['spoken_prompt']
    prefix=['Два признака подходят. ','Три признака подходят. '][i]
    self.assertTrue(spoken.startswith(prefix),(task['id'],spoken))
    # Only the introductory count is rephrased, never the scientific clauses.
    self.assertEqual(spoken[len(prefix):],written.split('. ',1)[1],task['id'])
