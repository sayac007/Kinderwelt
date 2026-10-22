import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('delivery',ROOT/'scripts/android/build_variants.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class DeliveryTests(unittest.TestCase):
    def fixture(self,root):
        folder=root/'family';folder.mkdir()
        data={'variant':'family','package':'org.example.kinderwelt.preview.family.v081','version_name':'0.8.1','version_code':12,'application_source_sha256':'source-fixture','artifacts':{}}
        for name,raw in [('kinderwelt-debug.apk',b'APK fixture already verified by builder'),('kinderwelt-unsigned.aab',b'AAB fixture already verified by builder')]:
            (folder/name).write_bytes(raw);data['artifacts'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        (folder/'provenance.json').write_text(json.dumps(data));return folder
    def test_delivery_names_preserve_verified_hashes_without_duplicate_large_files(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=self.fixture(root);result=m.collect(folder,'family')
            self.assertEqual(set(result),{'kinderwelt-debug-family.apk','kinderwelt-unsigned-family.aab'})
            self.assertEqual(len(list(root.rglob('*.apk'))),1)
            self.assertEqual(len(list(root.rglob('*.aab'))),1)
            for name,data in result.items():self.assertEqual(hashlib.sha256((root/name).read_bytes()).hexdigest(),data['sha256'])
            self.assertEqual(result['kinderwelt-unsigned-family.aab']['signing'],'UNSIGNED')
    def test_modified_artifact_is_not_published_under_expected_name(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=self.fixture(root);(folder/'kinderwelt-debug.apk').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'differs'):m.collect(folder,'family')
            self.assertFalse((root/'kinderwelt-debug-family.apk').exists())

    def test_cast_variant_cannot_be_relabelled_as_family(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=self.fixture(root)
            proof=json.loads((folder/'provenance.json').read_text());proof['variant']='public';(folder/'provenance.json').write_text(json.dumps(proof))
            with self.assertRaisesRegex(ValueError,'variant'):m.collect(folder,'family')
            self.assertFalse((root/'kinderwelt-debug-family.apk').exists())
    def test_changed_bundle_does_not_publish_only_half_of_the_pair(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=self.fixture(root);(folder/'kinderwelt-unsigned.aab').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'differs'):m.collect(folder,'family')
            self.assertFalse((root/'kinderwelt-debug-family.apk').exists())
