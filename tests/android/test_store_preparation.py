"""Store material must be reproducible, fictional, private-free and still a draft."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def module(name):
    spec=importlib.util.spec_from_file_location('store_'+name,ROOT/'scripts/store'/f'{name}.py')
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
listing=module('listing');privacy=module('privacy');render=module('render')
class StorePreparationTests(unittest.TestCase):
    def test_listing_counts_and_all_generated_text_match_current_catalogs(self):
        c=listing.check()
        self.assertEqual(c,dict(subjects=8,per_subject=50,base=400,bonus=800,scenes=7,music=20,languages=3))
    def test_stale_human_listing_text_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'docs/play').mkdir(parents=True)
            for name,text in listing.documents().items():(root/'docs/play'/name).write_text(text.replace('50','49'))
            from unittest.mock import patch
            with patch.object(listing,'counts',return_value=listing.counts()),self.assertRaisesRegex(ValueError,'Stale listing'):listing.check(root)
    def test_privacy_drafts_render_offline_and_unfilled_final_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'draft';privacy.build(out)
            for locale in listing.LOCALES:
                html=(out/f'{locale}.html').read_text()
                self.assertIn(f'lang="{locale}"',html)
                self.assertIn('{{HERAUSGEBER}}',html)
                self.assertNotIn('<script',html)
                self.assertNotIn('<img',html)
                self.assertNotIn('<iframe',html)
            final=Path(d)/'final'
            with self.assertRaisesRegex(ValueError,'placeholders'):privacy.build(final,True)
            self.assertFalse(final.exists())
    def test_geometric_placeholder_has_no_photo_or_external_input(self):
        render.validate_placeholder(ROOT/'art/store/silhouette.svg')
        for bad in ['<svg><image href="family.png"/></svg>','<svg><path fill="url(https://invalid/)"/></svg>','<!DOCTYPE svg><svg/>','<svg onload="x"/>']:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'bad.svg';p.write_text(bad)
                with self.assertRaises(ValueError):render.validate_placeholder(p)
    def test_renderer_rejects_family_and_unknown_character_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'assets/quest/characters').mkdir(parents=True)
            (root/'core/quest').mkdir(parents=True)
            original=json.loads((ROOT/'assets/quest/cast.json').read_text())
            self.assertEqual(original['variant'],'public')
            for name in ['neutral-cast.png',*[f'actor-{i}.tres' for i in range(1,7)]]:(root/'assets/quest/characters'/name).touch()
            (root/'core/quest/cast.gd').write_text('const FAMILY = false')
            (root/'assets/quest/cast.json').write_text(json.dumps(original));render.validate_cast(root)
            for variant,path in [('family','assets/quest/characters/actor-1.png'),('public','/tmp/personal.png')]:
                altered=json.loads(json.dumps(original));altered['variant']=variant;altered['sprites']['wanja']=path
                (root/'assets/quest/cast.json').write_text(json.dumps(altered))
                with self.assertRaises(ValueError):render.validate_cast(root)
    def test_pages_workflow_is_inactive_manual_main_only_and_has_no_family_secrets(self):
        path=ROOT/'.github/workflow-templates/privacy-pages.yml'
        self.assertTrue(path.exists());self.assertFalse((ROOT/'.github/workflows/privacy-pages.yml').exists())
        text=path.read_text()
        self.assertIn('workflow_dispatch:',text);self.assertIn("github.ref == 'refs/heads/main'",text)
        self.assertIn('privacy.py --final',text);self.assertNotIn('secrets.',text);self.assertNotIn('FAMILY_ASSETS',text)
