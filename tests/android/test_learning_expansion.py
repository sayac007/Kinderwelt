"""Independent guards for native literacy, bounded rewards and solvable bonuses."""
import importlib.util,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class LearningExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parents=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        cls.by_id={t['id']:t for t in cls.parents}
        cls.all=[t for p in cls.parents for t in [p,*p['bonuses']]]
    def test_two_optional_differently_valued_bonuses_per_station(self):
        self.assertEqual(len(self.all),960)
        self.assertEqual(len({t['id'] for t in self.all}),960)
        self.assertEqual(sum(t['points'] for t in self.all),51200)
        for parent in self.parents:
            self.assertEqual(parent['points'],10)
            self.assertEqual([b['points'] for b in parent['bonuses']],[50,100])
            for bonus in parent['bonuses']:
                self.assertTrue(bonus['optional'])
                self.assertEqual(bonus['parent_id'],parent['id'])
                self.assertEqual(bonus['subject'],parent['subject'])
                self.assertIn(bonus['answer'],bonus['options'])
                self.assertEqual(len(bonus['options']),len(set(bonus['options'])))
                self.assertEqual(set(bonus['texts']),{'de','en','ru'})
    def test_math_bonus_answers_satisfy_the_actual_two_step_equations(self):
        for parent in self.parents:
            if parent['subject']!='math':continue
            a,b=parent['bonuses']
            numbers=list(map(int,re.findall(r'\d+',a['display'])))
            self.assertEqual(numbers[0]+numbers[1]-numbers[2],a['answer'],a['id'])
            numbers=list(map(int,re.findall(r'\d+',b['display'])))
            self.assertEqual(numbers[0]+b['answer']+numbers[1],numbers[2],b['id'])
    def test_literacy_native_words_have_independently_checked_syllables(self):
        sun=self.by_id['german_sun']
        self.assertEqual((sun['variants']['en']['word'],sun['variants']['en']['answer']),('SUN','S'))
        self.assertEqual((sun['variants']['ru']['word'],sun['variants']['ru']['answer']),('СОЛНЦЕ','С'))
        for id,en,ru in [('german_robot',2,2),('german_21',3,3),('german_22',2,4),('german_23',3,4),('german_26',1,1)]:
            self.assertEqual(self.by_id[id]['variants']['en']['answer'],en,id)
            self.assertEqual(self.by_id[id]['variants']['ru']['answer'],ru,id)
        for parent in self.parents:
            if parent['subject']!='german':continue
            for task in [parent,*parent['bonuses']]:
                v=task['variants']['ru']
                self.assertRegex(v['word'],r'^[А-ЯЁ]+$')
                if task['kind']!='rhyme':
                    for option in v['options']:
                        if isinstance(option,str):self.assertRegex(option,r'^[А-ЯЁ]+$')
                for field in ('prompt','tip'):self.assertNotRegex(task['texts']['ru'][field],r'[A-Za-z]')
    def test_native_rhyme_has_a_matching_visible_label(self):
        t=self.by_id['german_rhyme']
        self.assertEqual(t['variants']['en']['option_labels'][t['variants']['en']['answer']],'MOUSE')
        self.assertEqual(t['variants']['ru']['option_labels'][t['variants']['ru']['answer']],'СОМ')
        self.assertIn('Дом',t['texts']['ru']['prompt'])
    def test_science_questions_have_indirect_context_and_short_keyword(self):
        science=[t for t in self.parents if t['kind']=='discovery']
        self.assertEqual(len(science),200)
        for t in science:
            self.assertIn('riddle_scene',t)
            self.assertIsInstance(t['riddle_scene'],str)
            for lang in ('de','en','ru'):
                keyword=t['variants'][lang]['keyword']
                self.assertLessEqual(len(keyword.split()),2)
                self.assertTrue(t['texts'][lang]['prompt'].startswith(keyword+'. '))
            self.assertEqual(len({t['answer'],*[b['answer'] for b in t['bonuses']]}),3,
                             'Science bonuses must not repeat the just-shown correct answer: '+t['id'])
        hearing=self.by_id['body_02']
        self.assertEqual(hearing['riddle_scene'],'sound')
        self.assertEqual(hearing['texts']['de']['prompt'],'Hören. Womit hört der Mensch?')
    def test_russian_ui_and_music_have_no_latin_letters(self):
        languages=json.loads((ROOT/'games/quest/languages.json').read_text())
        self.assertEqual(languages['ui']['german']['en'],'English')
        self.assertEqual(languages['ui']['german']['ru'],'Русский')
        for key,text in languages['ui'].items():self.assertNotRegex(text['ru'],r'[A-Za-z]',key)
        for entry in languages['music'].values():
            for text in entry.values():self.assertNotRegex(text,r'[A-Za-z]')
        for cast in languages['heroes'].values():
            for name in cast.values():self.assertNotRegex(name,r'[A-Za-z]')
    def test_russian_spoken_content_has_no_german_or_latin(self):
        spec=importlib.util.spec_from_file_location('native_voice',ROOT/'scripts/generate-quest-voice.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        clips=m.narration_texts('ru')
        self.assertEqual(len(clips),1947)
        for id,text in clips.items():self.assertNotRegex(text,r'[A-Za-z]',id)
        self.assertNotIn('немецк',clips['german_sun'].lower())
        self.assertIn('Солнце',clips['german_sun'])
