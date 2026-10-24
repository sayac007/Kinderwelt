import importlib.util,json,unittest
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('adult_review',ROOT/'scripts/qa/review_pack.py');qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
class ReviewPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=qa.catalog()
    def receipt(self):
        return {'schema':1,'contract_sha256':self.data['contract_sha256'],'reviews':[{'key':c['key'],'sha256':c['sha256'],'text_sha256':c['text_sha256'],'status':'PASS','issue':''} for c in self.data['cases']]}
    def test_catalog_covers_every_actual_language_binding_without_private_assets(self):
        for locale in ['de','en','ru']:
            bank=json.loads((ROOT/'assets/voice/quest'/locale/'manifest.json').read_text())
            rows=[c for c in self.data['cases'] if c['locale']==locale]
            self.assertEqual({id for c in rows for id in c['ids']},{c['id'] for c in bank['clips']})
            self.assertEqual({c['sha256'] for c in rows},{c['sha256'] for c in bank['clips']})
            self.assertTrue(all(Path(c['audio']).parts[0]==locale and len(Path(c['audio']).parts)==2 for c in rows))
    def test_open_or_flagged_reviews_never_turn_green(self):
        receipt=self.receipt();receipt['reviews']=[]
        self.assertEqual(qa.verify(receipt,self.data)['status'],'INCOMPLETE')
        receipt=self.receipt();receipt['reviews'][0].update(status='ISSUE',issue='stress')
        self.assertEqual(qa.verify(receipt,self.data)['status'],'ISSUES')
        self.assertIn('not an independently',qa.verify(self.receipt(),self.data)['scope'])
    def test_stale_duplicate_and_personal_fields_are_rejected(self):
        receipt=self.receipt();receipt['contract_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Stale'):qa.verify(receipt,self.data)
        receipt=self.receipt();receipt['reviews'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Stale'):qa.verify(receipt,self.data)
        receipt=self.receipt();receipt['reviews'].append(deepcopy(receipt['reviews'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):qa.verify(receipt,self.data)
        receipt=self.receipt();receipt['reviews'][0]['child_name']='not permitted'
        with self.assertRaisesRegex(ValueError,'personal'):qa.verify(receipt,self.data)
