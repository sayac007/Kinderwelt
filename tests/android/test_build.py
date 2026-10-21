"""Exercise subprocess failure handling, including long real-shaped Gradle logs."""
import contextlib
import importlib.util
import io
import os
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('android_build', Path(__file__).resolve().parents[2]/'scripts/android/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BuildDiagnosticsTests(unittest.TestCase):
    def invoke(self, code, timeout=10):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            log = path/'apk.log'
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                try:
                    build.run([sys.executable, '-c', code], os.environ.copy(), path, log, timeout=timeout)
                except RuntimeError as error:
                    return output.getvalue(), log.read_text(), str(error)
            return output.getvalue(), log.read_text(), None

    def test_nonzero_export_prints_middle_cause_and_tail(self):
        code = "print('task output\\n'*200); print('* What went wrong:'); print('Concrete export failure'); print('stack frame\\n'*500); print('last diagnostic'); raise SystemExit(7)"
        output, log, error = self.invoke(code)
        self.assertIn('status 7', error)
        self.assertIn('Concrete export failure', output)
        self.assertIn('last diagnostic', output)
        self.assertIn('::error::apk.log:', output)
        self.assertLess(len(output.splitlines()), 200)
        self.assertGreater(len(log.splitlines()), 700)

    def test_godot_zero_exit_error_is_rejected_and_ansi_removed(self):
        output, log, error = self.invoke("print('\\x1b[31mERROR: Failed to export project\\x1b[0m')")
        self.assertIsNotNone(error)
        self.assertIn('Failed to export project', output)
        self.assertNotIn('\x1b', output)
        self.assertIn('\x1b', log)

    def test_timeout_preserves_and_prints_partial_output(self):
        output, log, error = self.invoke("import time; print('export started', flush=True); time.sleep(10)", timeout=0.2)
        self.assertIn('timed out', error)
        self.assertIn('export started', output)
        self.assertIn('export started', log)

    def test_success_is_not_marked_failed(self):
        output, log, error = self.invoke("print('BUILD SUCCESSFUL')")
        self.assertIsNone(error)
        self.assertIn('apk.log: PASS', output)
        self.assertNotIn('::error::', output)

    def test_tool_output_cannot_inject_workflow_commands(self):
        output, _, error = self.invoke("print('::error::injected command'); raise SystemExit(1)")
        self.assertIsNotNone(error)
        self.assertNotIn('\n::error::injected', output)
        self.assertIn('| ::error::injected', output)

    def test_missing_executable_reports_start_failure(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as output:
            path = Path(directory)
            with self.assertRaisesRegex(RuntimeError, 'could not start process'):
                build.run([str(path/'absent')], {}, path, path/'apk.log')
            self.assertIn('could not start process (FileNotFoundError)', output.getvalue())


class SourceProvenanceTests(unittest.TestCase):
    def test_snapshot_without_git_is_identified_honestly(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(build.git_provenance(Path(d)),{'source_tracking':'unversioned-snapshot','source_commit':None,'source_dirty':None})
    def test_nested_ignored_capsule_does_not_inherit_parent_git_identity(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','--quiet',str(root)],check=True)
            capsule=root/'build/capsule';capsule.mkdir(parents=True)
            self.assertEqual(build.git_provenance(capsule)['source_tracking'],'unversioned-snapshot')
    def test_real_worktree_tracks_clean_and_modified_sources(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','--quiet',str(root)],check=True)
            (root/'app.txt').write_text('source')
            subprocess.run(['git','-C',str(root),'add','app.txt'],check=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Regression Fixture','-c','user.email=fixture@example.invalid','commit','--quiet','-m','fixture'],check=True)
            clean=build.git_provenance(root)
            self.assertEqual(clean['source_tracking'],'git-worktree');self.assertFalse(clean['source_dirty'])
            self.assertEqual(len(clean['source_commit']),40)
            (root/'app.txt').write_text('changed');self.assertTrue(build.git_provenance(root)['source_dirty'])


if __name__ == '__main__':
    unittest.main()
