import importlib.util
import json
import unittest
import sys
import tempfile
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("audit",Path(__file__).parents[2]/"scripts/qa/static_audit.py")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)

sys.path.insert(0,str(Path(__file__).parents[2]/"scripts/qa"))
from run import validate_junit


class StaticAuditTests(unittest.TestCase):
    def rules(self,path,text):
        return {f["rule"] for f in AUDIT.inspect_text(path,text)}

    def test_runtime_network_is_rejected(self):
        self.assertIn("network",self.rules("games/new/game.gd","var client = HTTPRequest.new()"))

    def test_native_process_calls_are_rejected(self):
        self.assertIn("process",self.rules("core/helpers.gd",'OS.execute("tool", [])'))

    def test_tracking_sdk_is_rejected(self):
        self.assertIn("tracking",self.rules("addons/new/sdk.gd","FirebaseAnalytics.log_event()"))

    def test_permissions_true_and_custom_are_rejected(self):
        self.assertIn("permission",self.rules("export_presets.cfg","permissions/internet=true"))
        self.assertIn("permission",self.rules("export_presets.cfg",'permissions/custom_permissions=PackedStringArray("example")'))

    def test_disabled_permission_is_not_reported_as_enabled(self):
        self.assertNotIn("permission",self.rules("export_presets.cfg","permissions/internet=false"))

    def test_manifest_permission_requires_review(self):
        self.assertIn("permission",self.rules("android/AndroidManifest.xml",'<uses-permission android:name="example"/>'))

    def test_secret_report_never_contains_value(self):
        synthetic = "gh" + "p_" + "X"*36
        findings = AUDIT.inspect_text("core/key.gd",'var key = "'+synthetic+'"')
        self.assertEqual(findings,[{"rule":"secret","path":"core/key.gd","line":1}])
        self.assertNotIn(synthetic,json.dumps(findings))

    def test_network_examples_in_manuals_are_not_runtime_calls(self):
        self.assertNotIn("network",self.rules("docs/manual.md","HTTPRequest / https://example.org"))

    def test_development_only_framework_is_not_app_runtime(self):
        self.assertEqual(AUDIT.inspect_text("addons/gut/http.gd","HTTPRequest.new()"),[])

    def test_ordinary_shapes_and_local_saves_are_allowed(self):
        self.assertEqual(self.rules("core/save.gd",'FileAccess.open("user://progress.json", FileAccess.WRITE)'),set())



class EvidenceIntegrityTests(unittest.TestCase):
    def validate(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"result.xml"
            path.write_text(content)
            return validate_junit(path)

    def test_zero_tests_is_a_failure(self):
        with self.assertRaises(ValueError):
            self.validate('<testsuites tests="0"/>')

    def test_failed_cases_are_rejected(self):
        with self.assertRaises(ValueError):
            self.validate('<testsuites tests="1"><testcase status="fail" assertions="1"><failure/></testcase></testsuites>')

    def test_pending_cases_are_rejected(self):
        with self.assertRaises(ValueError):
            self.validate('<testsuites tests="1"><testcase status="pending" assertions="1"><skipped/></testcase></testsuites>')

    def test_zero_assertions_is_not_a_pass(self):
        with self.assertRaises(ValueError):
            self.validate('<testsuites tests="1"><testcase status="pass" assertions="0"/></testsuites>')

    def test_inconsistent_counts_are_rejected(self):
        with self.assertRaises(ValueError):
            self.validate('<testsuites tests="9"><testcase status="pass" assertions="1"/></testsuites>')

    def test_passing_current_format_is_counted(self):
        self.assertEqual(self.validate('<testsuites tests="1" failures="0"><testsuite skipped="0"><testcase status="pass" assertions="3"/></testsuite></testsuites>'),{"tests":1,"assertions":3,"failed":0,"skipped":0})

if __name__=="__main__":
    unittest.main()
