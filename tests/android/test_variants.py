"""Privacy boundary: public snapshots need no private pack; legacy IDs persist."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('variants',ROOT/'scripts/variants.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class VariantTests(unittest.TestCase):
    def test_public_snapshot_has_all_looks_and_no_private_resource_files(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'app';cast=v.snapshot(target,'public')
            self.assertEqual(cast['names']['wanja'],'Nova')
            self.assertEqual(cast['names']['george'],'Zora')
            self.assertEqual(set(cast['sprites']),{'wanja','mischa','du','mama','katze','george','squirrel'})
            self.assertFalse((target/'.private').exists())
            self.assertFalse(list((target/'assets/quest/characters').glob('outfits-*.png')))
            self.assertFalse(list((target/'assets/quest/characters').glob('actor-*.png')))
            data=json.loads((target/'assets/quest/looks.json').read_text())
            for id in v.IDS:
                self.assertEqual(set(data['heroes'][id]['frames']),set(v.LOOKS))
                self.assertIn('neutral-cast.png',(target/'core/quest/cast.gd').read_text())
            # No actual private PNG bytes may occur under any renamed file.
            private=ROOT/'.private/characters'
            if private.exists():
                forbidden={hashlib.sha256(p.read_bytes()).digest() for p in private.glob('*.png')}
                for p in target.rglob('*.png'):self.assertNotIn(hashlib.sha256(p.read_bytes()).digest(),forbidden)
    def test_missing_private_pack_is_an_explicit_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'Private character pack'):
                v.prepare(Path(d)/'out','family',Path(d))
    def test_legacy_save_contract_is_shared_instead_of_rewriting_progress(self):
        # Both snapshots ship the identical existing save cleaner and task IDs.
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'public';v.snapshot(target,'public')
            for path in ['core/save_store.gd','games/quest/progress.gd','games/quest/tasks.json']:
                self.assertEqual((target/path).read_bytes(),(ROOT/path).read_bytes())

    def test_public_source_export_excludes_history_and_private_notes(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'source';v.export_public(target)
            self.assertFalse((target/'.git').exists())
            self.assertFalse((target/'.private').exists())
            self.assertFalse((target/'docs/internal').exists())
            self.assertFalse((target/'art/private').exists())
            self.assertTrue((target/'scripts/variants.py').exists())
            self.assertTrue((target/'art/public/characters/catalog.json').exists())
            self.assertEqual((target/'ASSETS_LICENSE.md').read_bytes(),(ROOT/'ASSETS_LICENSE.md').read_bytes())

    def test_public_cat_astronaut_frame_excludes_neighboring_tail(self):
        data=json.loads((ROOT/'art/public/characters/frames.json').read_text())
        frames=data['heroes']['katze']['frames']
        x,y,w,h=frames['astronaut']
        self.assertLessEqual(x+w,frames['scientist'][0])
        self.assertLessEqual(x+w,805)
        self.assertEqual(data['source_sha256'],hashlib.sha256((ROOT/'art/public/characters/neutral-cast.png').read_bytes()).hexdigest())
