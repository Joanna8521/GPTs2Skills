"""Offline regression tests for GPTs Transform candidate validation."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_candidate import validate

class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "sample-gpt"
        (self.root / "agents").mkdir(parents=True)
        (self.root / "references").mkdir()
        (self.root / "SKILL.md").write_text("---\nname: sample-gpt\ndescription: Test\n---\n# Test\n", encoding="utf-8")
        (self.root / "FROZEN.md").write_text("# Rules", encoding="utf-8")
        (self.root / "agents" / "openai.yaml").write_text("interface:\n  display_name: Test\n", encoding="utf-8")
        (self.root / "references" / "test-cases.md").write_text("zh-TW example\nEnglish example", encoding="utf-8")
        self.data = {"skill_name":"sample-gpt","approval":True,
          "source_requirements":[{"id":"R001","original":"Make a summary"}],
          "traceability":[{"id":"R001","status":"preserved","target":"SKILL.md","reason":"Retained"}],
          "language_policy":{"interview":"en","output":"bilingual"},
          "dependencies":[], "checks":{"functional":"not_tested","external":"not_applicable"}}
        self.write()
    def tearDown(self):
        self.tmp.cleanup()
    def write(self):
        (self.root / "manifest.json").write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
    def test_valid(self):
        self.assertEqual(validate(self.root), [])
    def test_no_approval(self):
        self.data["approval"]=False; self.write(); self.assertTrue(validate(self.root))
    def test_missing_source(self):
        self.data["source_requirements"]=[]; self.write(); self.assertTrue(validate(self.root))
    def test_trace_gap(self):
        self.data["traceability"]=[]; self.write(); self.assertTrue(validate(self.root))
    def test_unapproved_removal(self):
        self.data["traceability"][0]["status"]="removed_approved"; self.write(); self.assertTrue(validate(self.root))
    def test_missing_target(self):
        self.data["traceability"][0]["target"]="nonexistent.md"; self.write(); self.assertTrue(validate(self.root))
    def test_path_escape(self):
        self.data["traceability"][0]["target"]="../elsewhere"; self.write(); self.assertTrue(validate(self.root))
    def test_bad_language(self):
        self.data["language_policy"]["output"]="fr"; self.write(); self.assertTrue(validate(self.root))
    def test_bilingual_coverage(self):
        (self.root / "references" / "test-cases.md").write_text("only Chinese", encoding="utf-8")
        self.assertTrue(validate(self.root))
    def test_missing_dependency_status(self):
        self.data["dependencies"]=[{"name":"Gmail"}]; self.write(); self.assertTrue(validate(self.root))

if __name__ == "__main__":
    unittest.main()
