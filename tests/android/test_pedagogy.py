"""Reject the reported defects, not only one particular generator output."""
from copy import deepcopy
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('pedagogy_qa',ROOT/'scripts/qa/pedagogy.py');qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
class PedagogyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        cls.baseline=json.loads((ROOT/'tests/fixtures/pedagogy/baseline-cases.json').read_text())
    def data(self):
        data=deepcopy(self.tasks)
        return data,{t['id']:t for p in data for t in [p,*p['bonuses']]}
    def errors(self,data):return qa.inspect(data)['failures']
    def test_known_whole_object_properties_are_not_false_distractors(self):
        # These are independent factual counterexamples found in source review:
        # a screwdriver also rotates about an axis, and an oak takes up water.
        # A consistent matrix alone would not detect an omitted true fact.
        facts=qa.properties()
        self.assertIn('screwdriver',facts['physics']['axis']['members'])
        self.assertIn('tree',facts['biology']['uptake']['members'])
    def test_reported_terminology_and_long_word_are_corrected(self):
        _,by=self.data()
        self.assertEqual(len(self.baseline['original_flower_cases']),12)
        for id in self.baseline['original_flower_cases']:
            t=by[id]
            if '_bonus_' in id:
                self.assertIn('comparison',t,'Recycled plant-part bonus must be replaced: '+id)
            else:
                for lang,name in [('de','Blüte'),('en','blossom'),('ru','цветок')]:
                    self.assertEqual(t['variants'][lang]['option_labels']['flower'],name)
        words={t.get('word') for t in by.values() if t['subject']=='german'}
        self.assertNotIn('SCHILDKRÖTENEI',words)
        self.assertIn('ENTENEI',words)
    def test_all_tasks_languages_and_original_33_cases_are_reviewed(self):
        report=qa.inspect(self.tasks)
        self.assertEqual(report['failures'],[])
        self.assertEqual(len(report['baseline_33_rechecks']),33)
        self.assertTrue(all(r['review'] for r in report['baseline_33_rechecks']))
        self.assertEqual({r['id'] for r in report['baseline_33_rechecks'] if r['remaining_image_warning']},{'physics_09','body_16'})
        self.assertEqual(len(report['difficulty_review']),640)
        self.assertFalse(any(r['probably_easier_structurally'] for r in report['difficulty_review']))
    def test_solution_prefixes_and_bare_science_answers_fail_in_each_language(self):
        for locale,text in [('de','Gesucht ist: Rad.'),('en','The answer is wheel.'),('ru','Ответ: колесо.')]:
            data,by=self.data();by['physics_01']['texts'][locale]['tip']=text
            self.assertTrue(any('solution-prefix' in e for e in self.errors(data)),locale)
        data,by=self.data();by['physics_05']['texts']['de']['tip']='Das passende Material ist ein Eisenstück.'
        self.assertTrue(any('named-science-answer' in e for e in self.errors(data)))
    def test_spelled_missing_answers_fail_without_requiring_a_known_prefix(self):
        for locale in ('de','en','ru'):
            data,by=self.data();t=by['german_sun'];v=t if locale=='de' else t['variants'][locale]
            t['texts'][locale]['tip']='. '.join(v['answer'])+'.'
            self.assertTrue(any('missing-letter-list' in e for e in self.errors(data)),locale)
    def test_final_math_answer_fails_but_real_intermediate_and_short_word_do_not(self):
        for locale,prefix in [('de','Zuletzt '),('de','Das Ergebnis ist '),('en','The result is '),('ru','Результат равен ')]:
            data,by=self.data();t=by['math_count'];t['texts'][locale]['tip']=prefix+str(t['answer'])+'.'
            self.assertTrue(any('final-result' in e for e in self.errors(data)))
        data,by=self.data();by['math_count']['texts']['de']['tip']='9 plus 4 sind 13. Danach 2 weg.'
        by['biology_29']['texts']['de']['tip']='Eine Eigenschaft ist die schützende Hülle.'
        self.assertEqual(self.errors(data),[])
    def test_each_of_the_five_old_constant_step_cases_is_rejected(self):
        for id in self.baseline['reported_alternation_ids']:
            data,by=self.data();t=by[id]
            t['logic_rule'].update(given=[1,2,3,4],steps=[1,1],continuation=[5,6]);t['answer']=11;t['options']=[10,11,12]
            self.assertTrue(any('alternating-steps' in e for e in self.errors(data)),id)
    def test_wrong_continuation_and_inverse_answers_fail_even_when_in_options(self):
        for suffix in (1,2):
            data,by=self.data();t=by['logic_repeat_bonus_'+str(suffix)];t['answer']+=1
            self.assertIn(t['answer'],t['options'])
            self.assertTrue(any('answer' in e for e in self.errors(data)))
    def test_visible_spoken_and_hint_rule_data_must_agree(self):
        for field in ('display','prompt','tip'):
            data,by=self.data();t=by['logic_repeat_bonus_1']
            if field=='display':t['display']='1 → 2 → 3 → 4 → ? → ?'
            else:t['texts']['en'][field]='99, 98, 97.'
            self.assertTrue(any('drift' in e for e in self.errors(data)),field)
    def test_cross_station_science_and_logic_duplicates_are_rejected(self):
        for first,second in [('geography_01_bonus_2','geography_31_bonus_2'),('logic_repeat_bonus_1','logic_triple_bonus_1')]:
            data,by=self.data()
            for lang in ('de','en','ru'):by[second]['texts'][lang]['prompt']=by[first]['texts'][lang]['prompt']
            self.assertTrue(any('Duplicate non-math bonuses' in e for e in self.errors(data)))
    def test_math_template_exception_requires_different_actual_equations(self):
        data,by=self.data();first,second=by['math_count_bonus_2'],by['math_compare_bonus_2']
        second['display']=first['display']
        for lang in ('de','en','ru'):second['texts'][lang]['prompt']=first['texts'][lang]['prompt']
        self.assertTrue(any('Duplicate identical math bonuses' in e for e in self.errors(data)))
    def test_duplicate_or_missing_answer_choices_are_rejected(self):
        for opts in [['wheel','wheel','gear'],['gear','lever','pulley']]:
            data,by=self.data();by['physics_35']['options']=opts
            self.assertTrue(any('duplicate/missing answer' in e for e in self.errors(data)))
    def test_unrelated_distractors_and_unreviewed_exception_mutations_fail(self):
        data,by=self.data();by['physics_35']['options']=['wheel','salt','scissors']
        self.assertTrue(any('unrelated comparison categories' in e for e in self.errors(data)))
        data,by=self.data();by['physics_09']['options']=['helmet','paper','salt']
        self.assertTrue(any('unreviewed exception options' in e for e in self.errors(data)))
    def test_bonus_parent_and_source_references_must_match(self):
        for parent in ('german_sun','physics_02'):
            data,by=self.data();by['physics_01_bonus_1']['parent_id']=parent
            self.assertTrue(any('inconsistent parent/reward' in e for e in self.errors(data)))
        data,by=self.data();by['physics_01_bonus_1']['points']=100
        self.assertTrue(any('inconsistent parent/reward' in e for e in self.errors(data)))
        data,by=self.data();by['physics_01_bonus_1']['comparison']['property_ids'][0]='missing-property'
        self.assertTrue(any('invalid property source reference' in e for e in self.errors(data)))
    def test_ambiguous_property_comparison_and_stale_text_are_rejected(self):
        data,by=self.data();t=by['biology_01_bonus_1'];facts=qa.properties()[t['subject']];selected=[facts[k] for k in t['comparison']['property_ids']]
        pool=set().union(*(x['members'] for x in facts.values()))
        other=next((o for o in pool if o not in t['options'] and sum(o in f['members'] for f in selected)==t['comparison']['required_matches']),None)
        # Some fact sets identify one model only. A sibling with the same
        # truth vector guarantees a concrete second solution in this fixture.
        if other is None:
            t['comparison']['property_ids']=['animal','mammal','not_plant'];t['comparison']['required_matches']=2
            t['answer']='bird';t['options']=['bird','fish','cat']
        else:t['options']=[t['answer'],other,t['options'][0] if t['options'][0]!=t['answer'] else t['options'][1]]
        self.assertTrue(any('ambiguous answer' in e or 'duplicate/missing answer' in e for e in self.errors(data)))
        data,by=self.data();by['physics_01_bonus_1']['texts']['en']['prompt']='Stale old question.'
        self.assertTrue(any('source/content reference drift' in e for e in self.errors(data)))
    def test_task_ids_and_counts_cannot_silently_change(self):
        data,_=self.data();data.pop()
        self.assertTrue(any('IDs/count changed' in e for e in self.errors(data)))
