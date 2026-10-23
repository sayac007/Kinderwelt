#!/usr/bin/env python3
"""Bounded local source/content audit; not a privacy or educational certification."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
findings=[]
for folder in ['core','games']:
 for path in (ROOT/folder).rglob('*.gd'):
  if re.search(r'HTTPRequest|HTTPClient|WebSocket|JavaScriptBridge|OS\.(execute|create_process|shell_open)',path.read_text()):findings.append(str(path.relative_to(ROOT)))
for line in (ROOT/'export_presets.cfg').read_text().splitlines():
 if re.search(r'permissions/\w+\s*=true',line):findings.append('enabled Android permission')
tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
assert len(tasks)==400 and len({t['id'] for t in tasks})==400
assert {t['subject'] for t in tasks}=={'math','german','logic','physics','biology','chemistry','body','geography'}
for s in ['math','german','logic','physics','biology','chemistry','body','geography']:assert sum(t['subject']==s for t in tasks)==50
for path in ['core/main.gd','core/modern','games/adventure','games/water','content']:
 if (ROOT/path).exists():findings.append('obsolete project component: '+path)
report={'technical_status':'PASS' if not findings else 'FAIL','task_count':400,'bonus_count':sum(len(t['bonuses']) for t in tasks),'maximum_points':sum(t['points']+sum(b['points'] for b in t['bonuses']) for t in tasks),'content_revision':2,'legacy_reward_count':320,'maximum_lifetime_points':67200,'subjects':8,'findings':findings,'scope':'Bounded runtime network/permission/source checks, not a security certification','device_testing':'OPEN','child_usability':'NOT EMPIRICALLY EVALUATED','learning_effect':'NOT ESTABLISHED'}
output=ROOT/'qa-results';output.mkdir(exist_ok=True)
(output/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(findings))
