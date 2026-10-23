import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class VoiceModelTests(unittest.TestCase):
    def test_shipped_voice_and_unmodified_model_cards_match_reviewed_provenance(self):
        spec=importlib.util.spec_from_file_location('voice_models',ROOT/'scripts/qa/voice_models.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        report=m.check()
        self.assertEqual(report['de']['model'],'de_DE-thorsten-high')
        self.assertEqual(report['de']['human_intelligibility'],'OPEN')
    def test_recommendation_distinguishes_quality_from_samplerate(self):
        c=json.loads((ROOT/'scripts/qa/voice-models.json').read_text())
        self.assertEqual({v['quality_from_config'] for v in c['german_candidates']},{'medium','high'})
        self.assertEqual({v['sample_rate'] for v in c['german_candidates']},{22050})
        self.assertTrue(all(v['dataset_license']=='CC0' for v in c['german_candidates']))
