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
        self.assertEqual(len(self.all),1200)
        self.assertEqual(len({t['id'] for t in self.all}),1200)
        self.assertEqual(sum(t['points'] for t in self.all),64000)
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
    def test_every_new_math_equation_is_independently_solvable(self):
        import ast,operator
        def arithmetic(text):
            node=ast.parse(text,mode='eval').body
            def visit(n):
                if isinstance(n,ast.Constant) and type(n.value)==int:return n.value
                self.assertIsInstance(n,ast.BinOp)
                self.assertIn(type(n.op),(ast.Add,ast.Sub))
                return (operator.add if isinstance(n.op,ast.Add) else operator.sub)(visit(n.left),visit(n.right))
            return visit(node)
        for parent in self.parents:
            if parent['subject']!='math':continue
            for task in [parent,*parent['bonuses']]:
                left,right=task['display'].replace('−','-').replace('?',str(task['answer'])).split('=')
                self.assertEqual(arithmetic(left.strip()),arithmetic(right.strip()),task['id'])
    def test_every_base_task_replaces_the_completed_first_round(self):
        old=json.loads((ROOT/'scripts/content/round-one-questions.json').read_text())['questions']
        self.assertEqual(len(old),320)
        for t in self.parents:
            self.assertEqual(t['content_revision'],2)
            for locale in ('de','en','ru'):
                if t['id'] in old:self.assertNotEqual(t['texts'][locale]['prompt'],old[t['id']][locale],(t['id'],locale))
        for subject in ('math','german','logic'):
            self.assertEqual(len({json.dumps({k:t.get(k) for k in ('display','sequence','counts','order','ask_first')},sort_keys=True) for t in self.parents if t['subject']==subject}),50)
        for lang in ('de','en','ru'):
            science=[t for t in self.parents if t['kind']=='discovery']
            self.assertEqual(len({t['texts'][lang]['prompt'] for t in science}),250)
        legacy=json.loads((ROOT/'games/quest/legacy-rewards.json').read_text())['rewards']
        self.assertEqual(set(legacy),set(old))
        self.assertEqual(sum(legacy.values()),3200)
    def test_native_letter_puzzles_reconstruct_the_new_word(self):
        sun=self.by_id['german_sun']
        self.assertEqual((sun['word'],sun['answer']),('SONNENSTRAHL','SS'))
        self.assertEqual((sun['variants']['en']['word'],sun['variants']['en']['answer']),('SUNSHINE','SH'))
        self.assertEqual((sun['variants']['ru']['word'],sun['variants']['ru']['answer']),('СОЛНЫШКО','СЫ'))
        foot=next(t for t in self.parents if t.get('word')=='FUSSABDRUCK')
        for task in [foot,*foot['bonuses']]:
            self.assertIn('Fußabdruck',task['texts']['de']['spoken_prompt'])
            self.assertNotIn('Fußabdruck',task['texts']['de']['prompt'])
        for parent in self.parents:
            if parent['subject']!='german':continue
            for task in [parent,*parent['bonuses']]:
                for lang in ('de','en','ru'):
                    v=task if lang=='de' else task['variants'][lang]
                    letters=iter(v['answer'])
                    reconstructed=''.join(next(letters) if c=='_' else c for c in v['display'])
                    self.assertEqual(reconstructed,v['word'])
                    self.assertGreaterEqual(len(v['answer']),2 if task==parent else 3)
                    self.assertEqual(len(v['options']),len(set(v['options'])))
                    for j in range(len(v['answer'])):
                        self.assertTrue(any(option[j]!=v['answer'][j] for option in v['options']),
                                        'A gap must not be identical in every answer choice')
                v=task['variants']['ru']
                self.assertRegex(v['word'],r'^[А-ЯЁ]+$')
                for option in v['options']:self.assertRegex(option,r'^[А-ЯЁ]+$')
                for field in ('prompt','tip'):self.assertNotRegex(task['texts']['ru'][field],r'[A-Za-z]')
    def test_visual_logic_combines_two_rules_and_ordering_composes_constraints(self):
        first=self.by_id['logic_odd']
        self.assertEqual(first['sequence'],['sun','moon','star','sun','moon'])
        self.assertEqual(first['counts'],[1,3,4,6,7])
        self.assertEqual(first['answer'],'star:9')
        order=self.by_id['logic_shadow']
        self.assertEqual(set(order['options']),{'cat','frog','bird'})
        self.assertEqual(order['order'],['bird','cat','frog'])
        self.assertEqual(order['answer'],'bird')
        for t in self.parents:
            if t['kind']=='reasoning_choice':
                self.assertEqual(t['answer'],t['order'][0 if t['ask_first'] else -1])
    def test_correct_answer_slots_do_not_form_a_repeating_cycle(self):
        from collections import Counter
        for subject in {t['subject'] for t in self.parents}:
            slots=[t['options'].index(t['answer']) for t in self.parents if t['subject']==subject]
            self.assertEqual(set(slots),{0,1,2})
            self.assertTrue(any(slots[i]!=slots[i+3] for i in range(len(slots)-3)))
            self.assertLessEqual(max(Counter(slots).values()),25)
    def test_science_questions_have_indirect_context_and_short_keyword(self):
        science=[t for t in self.parents if t['kind']=='discovery']
        self.assertEqual(len(science),250)
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
        self.assertIn('Augen sind zu',hearing['texts']['de']['prompt'])
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
        self.assertEqual(len(clips),2427)
        for id,text in clips.items():self.assertNotRegex(text,r'[A-Za-z]',id)
        self.assertNotIn('немецк',clips['german_sun'].lower())
        self.assertIn('Солнышко',clips['german_sun'])
