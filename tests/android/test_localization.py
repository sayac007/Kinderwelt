import importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class LocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.tasks={t['id']:t for t in json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']}
    def test_new_multistep_quantities_are_present_in_translations(self):
        for locale in ['de','en','ru']:
            for n in ['9','4','2']:self.assertIn(n,self.tasks['math_count']['texts'][locale]['prompt'])
        self.assertIn('apples',self.tasks['math_take']['texts']['en']['prompt'])
        self.assertIn('яблок',self.tasks['math_take']['texts']['ru']['prompt'])
    def test_native_new_words_and_reconstruction_hints_are_visible(self):
        for t in self.tasks.values():
            if t['subject']!='german':continue
            for locale in ['en','ru']:
                text=t['texts'][locale];native=t['variants'][locale]
                self.assertIn(native['word'].casefold(),text['prompt'].casefold())
                for letter in native['answer']:self.assertIn(letter+'.',text['tip'])
    def test_german_targets_are_not_voiced_by_foreign_phonemizers(self):
        voice=load('voice','scripts/generate-quest-voice.py')
        for locale in ['en','ru']:
            clips=voice.narration_texts(locale)
            self.assertNotIn('Sonne',clips['german_sun'])
            self.assertNotIn('Roboter',clips['german_robot_hint'])
        self.assertIn('Sonnenstrahl',voice.narration_texts('de')['german_sun'])
    def test_review_and_logged_fields_match_delivered_texts(self):
        review=load('locale_review','scripts/qa/localization.py')
        self.assertEqual((ROOT/'docs/localization-review.md').read_text(),review.markdown())
        for c in json.loads((ROOT/'scripts/content/localization-changes.json').read_text())['changes']:
            self.assertEqual(self.tasks[c['id']]['texts'][c['locale']][c['field']],c['after'])

    def test_science_speech_is_short_and_does_not_read_out_the_answer_list(self):
        voice=load('voice_lists','scripts/generate-quest-voice.py')
        for locale in ['de','en','ru']:
            texts=voice.narration_texts(locale)
            for t in self.tasks.values():
                if t['kind']=='discovery':self.assertEqual(texts[t['id']],t['texts'][locale]['prompt'])
