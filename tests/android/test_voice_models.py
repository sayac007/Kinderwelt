import importlib.util,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class VoiceModelTests(unittest.TestCase):
    def test_shipped_voice_and_unmodified_model_cards_match_reviewed_provenance(self):
        spec=importlib.util.spec_from_file_location('voice_models',ROOT/'scripts/qa/voice_models.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        report=m.check()
        self.assertEqual(report['de']['model'],'Qwen3-TTS-12Hz-0.6B-CustomVoice')
        self.assertEqual(report['de']['speaker'],report['ru']['speaker'])
        self.assertEqual({row['voice_gender'] for row in report.values()},{'female'})
        self.assertEqual(report['de']['human_intelligibility'],'OPEN')
    def test_historical_model_records_distinguish_quality_from_samplerate(self):
        c=json.loads((ROOT/'scripts/qa/voice-models.json').read_text())
        self.assertEqual({v['quality_from_config'] for v in c['historical_german_candidates']},{'medium','high'})
        self.assertEqual({v['sample_rate'] for v in c['historical_german_candidates']},{22050})
        self.assertTrue(all(v['dataset_license']=='CC0' for v in c['historical_german_candidates']))

    def test_regeneration_refuses_old_male_models_for_german_and_russian(self):
        for locale in ['de','ru']:
            result=subprocess.run([sys.executable,str(ROOT/'scripts/generate-quest-voice.py'),'--locale',locale,'--model','/tmp/old-male-voice.onnx'],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertIn('weibliche Qwen-Stimme',result.stderr)
