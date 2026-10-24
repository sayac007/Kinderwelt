import hashlib,json,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class HeadgearTests(unittest.TestCase):
    def test_safe_answer_preserved_with_real_alternative_head_coverings(self):
        tasks={t['id']:t for t in json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']}
        languages=json.loads((ROOT/'games/quest/languages.json').read_text())
        catalog=json.loads((ROOT/'art/public/headgear.json').read_text())
        for id in ['physics_09','body_16']:
            task=tasks[id]
            self.assertEqual(task['answer'],'helmet')
            self.assertEqual(set(task['options']),{'helmet','cap','beanie'})
            for locale in ['de','en','ru']:
                self.assertTrue(all(languages['objects'][key][locale] for key in task['options']))
        self.assertEqual(len(catalog['images']),2)
        for row in catalog['images']:
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',raw[16:24])
            self.assertEqual(width,height)
            self.assertGreaterEqual(width,256)
            self.assertLessEqual(width,1536)
            self.assertEqual(raw[25],6,'RGBA with transparency, not a rectangular photo')
