"""Prevent automatic builds from refilling Actions storage with binary/media packs."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / '.github/workflows'


def steps(text):
    return re.split(r'(?m)^      - ', text)[1:]


class ArtifactPolicyTests(unittest.TestCase):
    def test_all_artifact_uploads_have_explicit_three_day_retention(self):
        uploads = []
        for path in WORKFLOWS.glob('*.yml'):
            for step in steps(path.read_text()):
                if 'uses: actions/upload-artifact@' in step:
                    uploads.append((path.name, step))
        self.assertGreaterEqual(len(uploads), 5)
        for workflow, step in uploads:
            with self.subTest(workflow=workflow, step=step.splitlines()[0]):
                self.assertRegex(step, r'(?m)^          retention-days: 3$')

    def test_automatic_workflows_never_upload_artifacts(self):
        for name in ['android.yml', 'test.yml']:
            text = (WORKFLOWS / name).read_text()
            self.assertIn('  push:\n    branches: [main]\n  pull_request:', text)
        for path in WORKFLOWS.glob('*.yml'):
            text = path.read_text()
            if not re.search(r'(?m)^  (?:push|pull_request):', text):
                continue
            for step in steps(text):
                if 'uses: actions/upload-artifact@' in step:
                    with self.subTest(workflow=path.name, step=step.splitlines()[0]):
                        self.assertRegex(step, r"(?m)^        if: .*github.event_name == 'workflow_dispatch'")

    def test_private_family_access_requires_explicit_manual_selection(self):
        text = (WORKFLOWS / 'android.yml').read_text()
        self.assertIn('default: neutral', text)
        private_steps = [step for step in steps(text) if
                         'FAMILY_ASSETS_TOKEN' in step or
                         'python3 scripts/ci/family_assets.py restore' in step]
        self.assertEqual(len(private_steps), 3)
        for step in private_steps:
            self.assertIn("if: github.event_name == 'workflow_dispatch' && inputs.variant != 'neutral'", step)
        self.assertIn("inputs.variant || 'neutral'", text)

    def test_apks_do_not_silently_include_unsigned_bundles(self):
        text = (WORKFLOWS / 'android.yml').read_text()
        self.assertRegex(text, r'(?s)include_unsigned_bundles:.*?type: boolean\n        default: false')
        uploads = [step for step in steps(text) if 'uses: actions/upload-artifact@' in step]
        apk = next(step for step in uploads if 'kinderwelt-debug-*.apk' in step)
        self.assertNotIn('.aab', apk)
        aab = next(step for step in uploads if 'kinderwelt-unsigned-*.aab' in step)
        self.assertIn('&& inputs.include_unsigned_bundles', aab)
        diagnostics = next(step for step in uploads if 'name: android-build-diagnostics' in step)
        for binary in ['.apk', '.aab', '.png', '.ogg', '.html']:
            self.assertNotIn(binary, diagnostics)

    def test_full_listening_and_screenshot_packs_are_individually_opt_in(self):
        text = (WORKFLOWS / 'test.yml').read_text()
        for flag in ['retain_evidence', 'listening_review']:
            self.assertRegex(text, rf'(?s){flag}:.*?type: boolean\n        default: false')
        for step in steps(text):
            if 'build/listening-acceptance' in step:
                self.assertIn("if: github.event_name == 'workflow_dispatch' && inputs.listening_review", step)
            if 'name: child-experience-verification' in step:
                self.assertIn("if: always() && github.event_name == 'workflow_dispatch' && inputs.retain_evidence", step)
        self.assertLess(text.index('bash tests/qa/quest-render.sh'), text.index('uses: actions/upload-artifact@'))

    def test_real_checks_and_release_protections_are_preserved(self):
        android = (WORKFLOWS / 'android.yml').read_text()
        for command in ['python3 -m unittest discover -s tests/android -v',
                        'python3 scripts/android/build_variants.py --variants neutral',
                        'python3 scripts/android/size_report.py']:
            self.assertIn(command, android)
        quality = (WORKFLOWS / 'test.yml').read_text()
        self.assertIn('bash tests/run.sh', quality)
        self.assertIn('bash tests/qa/quest-render.sh', quality)
        release = (WORKFLOWS / 'android-release.yml').read_text()
        self.assertIn("if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'", release)
        self.assertIn('    environment: release', release)
        self.assertIn('  contents: read', release)
        self.assertNotIn('contents: write', release)
