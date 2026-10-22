import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('origins',ROOT/'scripts/qa/character_origins.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CharacterOriginTests(unittest.TestCase):
    def test_actual_sources_match_reviewed_generated_images(self):
        result=m.audit(ROOT);self.assertEqual(result['status'],'PASS');self.assertEqual(result['historical_characters_blocked'],4)
        data=json.loads((ROOT/'art/character-origins.json').read_text())
        self.assertEqual(len(data['sources']),24)
        self.assertTrue(all(row['generation_output'].startswith('exec-') for row in data['sources']))
        self.assertEqual(sum(row['path'].startswith('.private/') for row in data['sources']),12)
    def fixture(self,root):
        source=ROOT/'art/character-origins.json';data=json.loads(source.read_text());data['sources']=[r for r in data['sources'] if r['path']=='assets/quest/squirrel.png']
        (root/'art').mkdir();(root/'art/character-origins.json').write_text(json.dumps(data))
        target=root/'assets/quest/squirrel.png';target.parent.mkdir(parents=True);shutil.copy2(ROOT/'assets/quest/squirrel.png',target)
    def test_changed_character_is_not_silently_declared_generated(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);p=root/'assets/quest/squirrel.png';p.write_bytes(p.read_bytes()+b'changed')
            with self.assertRaisesRegex(ValueError,'Unreviewed'):m.audit(root)
    def test_renamed_unapproved_active_png_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);folder=root/'assets/quest';(folder/'cast.json').write_text(json.dumps({'sprites':{'wanja':'assets/quest/renamed.png'},'atlases':{}}));(folder/'renamed.png').write_bytes(b'not approved')
            with self.assertRaisesRegex(ValueError,'approved generated sources'):m.audit(root)
