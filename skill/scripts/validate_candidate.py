#!/usr/bin/env python3
"""Fail-closed structural validation for generated Skill candidates."""
import json
import re
import sys
from pathlib import Path

NAME = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
STATUSES = {"preserved", "transformed", "merged", "removed_approved", "blocked"}
LANGUAGES = {"zh-TW", "en", "bilingual"}

def validate(root):
    root = Path(root).resolve()
    errors = []
    def check(test, message):
        if not test:
            errors.append(message)

    for rel in ("SKILL.md", "agents/openai.yaml", "FROZEN.md", "manifest.json"):
        check((root / rel).is_file(), f"Required file missing: {rel}")
    if not (root / "manifest.json").is_file():
        return errors
    try:
        data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return errors + [f"Invalid JSON manifest: {exc}"]
    name = data.get("skill_name")
    check(isinstance(name, str) and bool(NAME.fullmatch(name)), "Invalid ASCII slug")
    check(name == root.name, "Folder name does not match skill_name")
    check(data.get("approval") is True, "Explicit specification approval required")
    sources, traces = data.get("source_requirements"), data.get("traceability")
    check(isinstance(sources, list) and bool(sources), "Missing source requirements")
    check(isinstance(traces, list) and bool(traces), "Missing requirement traceability")
    if isinstance(sources, list) and isinstance(traces, list):
        srcids = []
        for item in sources:
            if not isinstance(item, dict):
                errors.append("Invalid source record")
                continue
            sid = item.get("id")
            check(isinstance(sid, str) and bool(sid), "Missing source ID")
            check(isinstance(item.get("original"), str) and bool(item["original"].strip()), f"Missing source text for {sid}")
            srcids.append(sid)
        check(len(srcids) == len(set(srcids)), "Duplicate source IDs")
        traceids = []
        for item in traces:
            if not isinstance(item, dict):
                errors.append("Invalid trace record")
                continue
            sid = item.get("id")
            traceids.append(sid)
            status = item.get("status")
            check(status in STATUSES, f"Invalid trace status: {sid}")
            check(bool(item.get("reason")), f"Trace explanation missing: {sid}")
            if status == "removed_approved":
                check(item.get("removal_approved") is True, f"Unapproved removal: {sid}")
            elif status != "blocked":
                target = item.get("target")
                check(isinstance(target, str) and bool(target), f"Missing mapped target: {sid}")
                if isinstance(target, str) and target:
                    path = (root / target).resolve()
                    check(path.is_relative_to(root) and path.is_file(), f"Missing or escaping target: {target}")
        check(len(traceids) == len(set(traceids)), "Duplicate trace IDs")
        check(set(srcids) == set(traceids), "Original requirements are not fully traced")
    lang = data.get("language_policy")
    check(isinstance(lang, dict), "Missing language policy")
    if isinstance(lang, dict):
        for field in ("interview", "output"):
            check(lang.get(field) in LANGUAGES, f"Invalid language policy: {field}")
        if lang.get("output") == "bilingual":
            cases = root / "references" / "test-cases.md"
            check(cases.is_file(), "Missing bilingual tests")
            if cases.is_file():
                text = cases.read_text(encoding="utf-8").lower()
                check("zh-tw" in text and "english" in text, "Tests lack zh-TW / English coverage")
    deps = data.get("dependencies")
    check(isinstance(deps, list), "Dependency declaration required")
    if isinstance(deps, list):
        for dep in deps:
            check(isinstance(dep, dict) and bool(dep.get("name")) and dep.get("status") in {"blocked", "not_tested", "passed_with_evidence", "not_applicable"}, "Invalid dependency record")
    checks = data.get("checks")
    check(isinstance(checks, dict), "Missing test states")
    if isinstance(checks, dict):
        check(checks.get("functional") in {"not_tested", "failed", "passed_with_evidence"}, "Invalid functional state")
        check(checks.get("external") in {"not_applicable", "not_tested", "blocked", "passed_with_evidence"}, "Invalid integration state")
    if (root / "SKILL.md").is_file():
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        check(body.startswith("---\n") and "\nname:" in body and "\ndescription:" in body, "SKILL.md frontmatter missing")
    for path in root.rglob("*"):
        if path.is_file():
            check(path.relative_to(root).as_posix().isascii(), f"Non-ASCII file path: {path}")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_candidate.py <skill-folder>")
        sys.exit(2)
    problems = validate(sys.argv[1])
    print("PASS" if not problems else "FAIL\n" + "\n".join(problems))
    sys.exit(1 if problems else 0)
