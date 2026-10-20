#!/usr/bin/env python3
"""Bounded source audit; reports locations/rules, never credential values."""
import json
import re
import subprocess
from pathlib import Path

RULES = {
    "network": re.compile(r"\b(?:HTTPRequest|HTTPClient|WebSocketPeer|WebSocketMultiplayerPeer|ENetMultiplayerPeer|PacketPeerUDP|TCPServer|StreamPeerTCP|JavaScriptBridge)\b|https?://"),
    "process": re.compile(r"\bOS\.(?:execute|create_process|shell_open)\s*\("),
    "tracking": re.compile(r"\b(?:FirebaseAnalytics|Appsflyer|AdjustSdk|Mixpanel|AdMob|Amplitude|Sentry|FacebookSdk)\b", re.I),
    "secret": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api_key|password|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9+/=_-]{16,})", re.I),
    "permission": re.compile(r"(?:permissions/[\w_]+\s*=\s*true|<uses-permission\b|permissions/custom_permissions\s*=\s*PackedStringArray\(\s*[\"'])", re.I),
}
EXCLUDED = (".git/", ".godot/", "addons/gut/", "qa-results/")
DEVELOPMENT = ("tests/", "scripts/", "docs/", ".github/")
RUNTIME_SUFFIXES = {".gd", ".cs", ".godot", ".tscn", ".tres", ".json", ".cfg", ".xml", ".gdextension", ".js"}
NATIVE_SUFFIXES = {".aar", ".jar", ".so", ".dll", ".dylib"}


def inspect_text(path, text):
    if path.startswith(EXCLUDED):
        return []
    runtime = not path.startswith(DEVELOPMENT) and Path(path).suffix in RUNTIME_SUFFIXES
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for rule, expression in RULES.items():
            if rule != "secret" and not runtime:
                continue
            if expression.search(line):
                findings.append({"rule": rule, "path": path, "line": number})
    return findings


def inventory(root, policy):
    registrations = json.loads((root / "content/modules.json").read_text())
    seen = set()
    tasks = []
    for entry in registrations:
        module = entry["id"]
        if module in seen or module not in policy["minimum_tasks"]:
            raise ValueError("Unknown or duplicate module registration")
        seen.add(module)
        for field in ["levels", "runtime"]:
            path = root / entry[field].removeprefix("res://")
            if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError("Missing or escaping runtime/content path")
        bundle = json.loads((root / entry["levels"].removeprefix("res://")).read_text())
        if bundle["schema"] != 1 or bundle["module"] != module:
            raise ValueError("Invalid bundle identity")
        levels = bundle["levels"]
        ids = [level["id"] for level in levels]
        if len(ids) != len(set(ids)) or len(ids) < policy["minimum_tasks"][module]:
            raise ValueError("Missing or duplicate authored tasks")
        tasks.extend({"module": module, "task": task} for task in ids)
    if seen != set(policy["minimum_tasks"]):
        raise ValueError("Missing registered area")
    return tasks


def audit(root, policy):
    names = subprocess.check_output(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=root
    ).decode().split("\0")
    findings = []
    count = 0
    permissions = []
    for name in sorted(set(filter(None, names))):
        if name.startswith(EXCLUDED):
            continue
        path = root / name
        if not path.is_file():
            continue
        if path.suffix.lower() in NATIVE_SUFFIXES and not name.startswith(DEVELOPMENT):
            findings.append({"rule": "native-dependency-review", "path": name, "line": 0})
        if path.name in ["export_presets.cfg", "AndroidManifest.xml"]:
            permissions.append(name)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        count += 1
        findings.extend(inspect_text(name, content))
    exceptions = policy.get("static_exceptions", [])
    for exception in exceptions:
        if (exception.get("rule") not in {*RULES, "native-dependency-review"}
                or not exception.get("reason") or not exception.get("path")
                or any(char in exception["path"] for char in "*?")):
            raise ValueError("Static exceptions require an exact path, known rule and rationale")
    waived = [f for f in findings if any(f["rule"] == e["rule"] and f["path"] == e["path"] for e in exceptions)]
    findings = [f for f in findings if f not in waived]
    return {
        "status": "PASS" if not findings else "FAIL",
        "scope": "tracked and non-ignored first-party source; bounded pattern checks, not a security/privacy certification",
        "files_examined": count, "findings": findings, "reviewed_exceptions": waived,
        "permission_manifests": permissions,
        "permission_scope": "source configuration only; no Android package/device audit",
        "tasks": inventory(root, policy),
    }
