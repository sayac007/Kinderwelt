"""The entry point, historical evidence and CI must not acquire dangling links."""
import importlib.util,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('documentation',ROOT/'scripts/qa/documentation.py');docs=importlib.util.module_from_spec(spec);spec.loader.exec_module(docs)
class DocumentationTests(unittest.TestCase):
    def test_current_documentation_and_ci_targets_exist(self):
        result=docs.check()
        self.assertEqual(result['findings'],[])
        self.assertEqual(result['archive_files'],139)
        self.assertGreater(result['ci_file_references'],0)
    def test_missing_local_link_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'docs/qa').mkdir(parents=True)
            shutil.copy2(ROOT/'docs/qa/ARCHIVE_INDEX.tsv',root/'docs/qa/ARCHIVE_INDEX.tsv')
            (root/'README.md').write_text(docs.COMMAND+'\n[Broken](docs/not-present.md)\n')
            (root/'docs/QUALITY_ASSURANCE.md').write_text(docs.COMMAND)
            result=docs.check(root)
            self.assertEqual(len(result['findings']),1)
            self.assertIn('docs/not-present.md',result['findings'][0])
