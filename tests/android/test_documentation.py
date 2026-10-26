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

    def test_only_named_long_term_audit_references_are_allowed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'docs/qa').mkdir(parents=True)
            shutil.copy2(ROOT/'docs/qa/ARCHIVE_INDEX.tsv',root/'docs/qa/ARCHIVE_INDEX.tsv')
            (root/'README.md').write_text(docs.COMMAND);(root/'docs/QUALITY_ASSURANCE.md').write_text(docs.COMMAND)
            (root/'docs/qa/VISUAL_IP_AUDIT.md').write_text('Current hand-maintained audit')
            (root/'docs/qa/visual-ip-manifest.json').write_text('{}')
            self.assertEqual(docs.check(root)['findings'],[])
            (root/'docs/qa/arbitrary-new-run.log').write_text('Must remain a runtime artifact')
            self.assertTrue(any('arbitrary-new-run.log' in f for f in docs.check(root)['findings']))

    def test_jekyll_navigation_checks_extensionless_sibling_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'docs/qa').mkdir(parents=True)
            shutil.copy2(ROOT/'docs/qa/ARCHIVE_INDEX.tsv',root/'docs/qa/ARCHIVE_INDEX.tsv')
            (root/'README.md').write_text(docs.COMMAND)
            (root/'docs/QUALITY_ASSURANCE.md').write_text(docs.COMMAND)
            pages=root/'docs/privacy';pages.mkdir()
            (pages/'index.md').write_text('---\ntitle: Privacy\n---\n[English](en)')
            (pages/'en.md').write_text('---\nlang: en\n---\nPolicy')
            self.assertEqual(docs.check(root)['findings'],[])
            (pages/'index.md').write_text('---\ntitle: Privacy\n---\n[Missing](ru)')
            self.assertTrue(any('missing ru' in f for f in docs.check(root)['findings']))
            # Ordinary documentation does not silently reinterpret missing paths.
            (pages/'index.md').write_text('[English](en)')
            self.assertTrue(any('missing en' in f for f in docs.check(root)['findings']))
