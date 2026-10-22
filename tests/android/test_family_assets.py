"""Import only approved derived art from a pinned separate private repository."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('family_assets',ROOT/'scripts/ci/family_assets.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FamilyAssetsTests(unittest.TestCase):
    def fixture(self,root):
        source=root/'private-repo';folder=source/'characters';folder.mkdir(parents=True)
        files={name:b'\x89PNG\r\n\x1a\nfixture-art-'+name.encode() for name in m.FILES if name.endswith('.png')}
        files['names.json']=json.dumps({id:id for id in m.IDS}).encode()
        files['looks.json']=json.dumps({'heroes':{id:{'sha256':hashlib.sha256(files['looks-'+id+'.png']).hexdigest()} for id in m.IDS}}).encode()
        for name,value in files.items():(folder/name).write_bytes(value)
        raw=json.dumps({'schema':1,'files':{name:{'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()} for name,value in files.items()}}).encode()
        (source/'manifest.json').write_bytes(raw)
        return source,files,hashlib.sha256(raw).hexdigest()
    def test_exact_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source,files,expected=self.fixture(root);target=root/'restored'
            m.restore(source,target,expected)
            self.assertEqual({p.name:p.read_bytes() for p in target.iterdir()},files)
            with self.assertRaisesRegex(ValueError,'overwrite'):m.restore(source,target,expected)
    def test_changed_image_or_manifest_leaves_no_partial_pack(self):
        for changed in ['characters/wanja.png','manifest.json']:
            with self.subTest(changed=changed),tempfile.TemporaryDirectory() as d:
                root=Path(d);source,_,expected=self.fixture(root);p=source/changed;p.write_bytes(p.read_bytes()+b'changed')
                with self.assertRaisesRegex(ValueError,'hash mismatch|pinned revision'):m.restore(source,root/'restored',expected)
                self.assertFalse((root/'restored').exists())
    def test_extra_photos_and_symlinked_images_are_rejected(self):
        for kind in ['photo','symlink']:
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                root=Path(d);source,_,expected=self.fixture(root)
                if kind=='photo':(source/'characters/source-photo.jpg').write_bytes(b'private photo')
                else:
                    p=source/'characters/wanja.png';p.rename(root/'outside.png');p.symlink_to(root/'outside.png')
                with self.assertRaisesRegex(ValueError,'source paths|Unsafe'):m.restore(source,root/'restored',expected)
                self.assertFalse((root/'restored').exists())
    def test_arbitrary_repository_expressions_and_floating_refs_are_rejected(self):
        base={'schema':1,'repository':'sayac007/Kinderwelt-family-assets','revision':'a'*40,'manifest_sha256':'b'*64}
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config';p.write_text(json.dumps(base));self.assertEqual(m.plan(p),base)
            for field,value in [('repository','owner/repo\nrevision=attacker'),('repository','../../outside'),('revision','main'),('manifest_sha256','unknown')]:
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                    p.write_text(json.dumps({**base,field:value}));m.plan(p)
    def test_stale_wardrobe_hash_is_rejected_even_after_manifest_is_updated(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source,_,_=self.fixture(root);p=source/'characters/looks-wanja.png';p.write_bytes(p.read_bytes()+b'new art')
            manifest=json.loads((source/'manifest.json').read_text());manifest['files']['looks-wanja.png']={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            raw=json.dumps(manifest).encode();(source/'manifest.json').write_bytes(raw)
            with self.assertRaisesRegex(ValueError,'Costume hash'):m.restore(source,root/'restored',hashlib.sha256(raw).hexdigest())
            self.assertFalse((root/'restored').exists())
