#!/usr/bin/env python3
"""Verify bundled generated character sources; not user-selected local avatars."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def audit(root=ROOT):
    data=json.loads((root/'art/character-origins.json').read_text())
    approved={row['sha256'] for row in data['sources']}
    banned={row['sha256'] for row in data['historical_excluded']}
    if approved&banned:raise ValueError('Historical excluded artwork approved by mistake')
    checked=[];absent=[]
    for row in data['sources']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Invalid provenance resource path')
        p=root/rel
        if not p.exists() and row['path'].startswith('.private/'):
            absent.append(row['path']);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Unreviewed character source: '+row['path'])
        if row.get('generation_source_path'):
            source=Path(row['generation_source_path'])
            if source.is_absolute() or '..' in source.parts:raise ValueError('Invalid generation source path')
            if hashlib.sha256((root/source).read_bytes()).hexdigest()!=row['generation_output_sha256']:
                raise ValueError('Original generation evidence changed: '+str(source))
        checked.append(row['path'])
    manifest=root/'assets/quest/cast.json'
    selected=[]
    if manifest.exists():
        cast=json.loads(manifest.read_text())
        for rel in sorted(set(cast['sprites'].values())|set(cast['atlases'].values())):
            if not rel.endswith('.png'):continue
            p=Path(rel)
            if p.is_absolute() or '..' in p.parts:raise ValueError('Invalid active cast path')
            h=hashlib.sha256((root/p).read_bytes()).hexdigest()
            if h not in approved or h in banned:raise ValueError('Active character does not match approved generated sources: '+rel)
            selected.append(rel)
    return {'status':'PASS','source_files_checked':len(checked),'private_sources_absent':len(absent),'selected_png_resources_checked':len(selected),'historical_characters_blocked':len(banned),'scope':'SHA256 and documented local generation evidence; no assertion of worldwide legal clearance','new_replacements_required':0}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();report=audit()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
