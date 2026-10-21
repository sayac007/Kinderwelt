import importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class LocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.tasks={t['id']:t for t in json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']}
    def test_apple_information_is_present_in_both_translations(self):
        for locale,word in [('en','apples'),('ru','яблок')]:self.assertIn(word,self.tasks['math_count']['texts'][locale]['prompt'])
        self.assertIn('leaves',self.tasks['math_take']['texts']['en']['prompt'])
        self.assertIn('звезды',self.tasks['math_ten']['texts']['ru']['prompt'])
    def test_german_learning_targets_and_syllables_are_visible(self):
        for t in self.tasks.values():
            if t['subject']!='german':continue
            for locale in ['en','ru']:
                text=t['texts'][locale]
                if t['kind'] in ['initial','syllables']:self.assertIn(t['word'].casefold(),text['prompt'].casefold())
                if t['kind']=='syllables':
                    for part in t['syllables']:self.assertIn(part.casefold()+'.',text['tip'].casefold())
                if t['kind']=='word':
                    for letter in t['word']:self.assertIn(letter+'.',text['tip'])
    def test_german_targets_are_not_voiced_by_foreign_phonemizers(self):
        voice=load('voice','scripts/generate-quest-voice.py')
        for locale in ['en','ru']:
            clips=voice.narration_texts(locale)
            self.assertNotIn('Sonne',clips['german_sun'])
            self.assertNotIn('Roboter',clips['german_robot_hint'])
        self.assertIn('Sonne',voice.narration_texts('de')['german_sun'])
    def test_review_and_logged_fields_match_delivered_texts(self):
        review=load('locale_review','scripts/qa/localization.py')
        self.assertEqual((ROOT/'docs/localization-review.md').read_text(),review.markdown())
        for c in json.loads((ROOT/'scripts/content/localization-changes.json').read_text())['changes']:
            self.assertEqual(self.tasks[c['id']]['texts'][c['locale']][c['field']],c['after'])
