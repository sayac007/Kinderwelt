"""Guard curated content independently of its source generator."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('distractors',ROOT/'scripts/qa/distractors.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
class DistractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        cls.by_id={t['id']:t for t in cls.tasks}
        cls.changes=json.loads((ROOT/'scripts/content/distractor-changes.json').read_text())
    def test_approved_answers_and_subjects_remain_unchanged(self):
        baseline=json.loads((ROOT/'scripts/content/science-answer-fixtures.json').read_text())['tasks']
        self.assertEqual(len(baseline),200)
        for key,expected in baseline.items():
            self.assertEqual({field:self.by_id[key][field] for field in expected},expected,key)
    def test_living_plant_is_not_a_wrong_living_answer(self):
        self.assertEqual(set(self.by_id['biology_32']['options']),{'mouse','paper','glass'})
    def test_screening_separates_categories_and_exemptions(self):
        self.assertFalse(qa.evaluate(self.by_id['physics_38'])['weak'])
        old=dict(self.by_id['physics_38'],options=['wheel','leaf','salt'])
        self.assertTrue(qa.evaluate(old)['weak'])
        self.assertGreater(qa.evaluate(self.by_id['body_01'])['score'],.5)
        self.assertIsNone(qa.evaluate(self.by_id['math_count'])['score'])
        self.assertIsNone(qa.evaluate(self.by_id['biology_32'])['score'])
    def test_missing_image_tasks_remain_untouched(self):
        self.assertFalse(set(qa.REQUIRES_IMAGES)&{c['id'] for c in self.changes})
    def test_review_is_reproducible_and_changes_have_stable_answers(self):
        document,rows=qa.markdown(self.tasks,self.changes)
        self.assertEqual((ROOT/'docs/distractor-review.md').read_text(),document)
        self.assertEqual(len(rows),1200)
        for change in self.changes:self.assertEqual(change['answer_before'],change['answer_after'])
