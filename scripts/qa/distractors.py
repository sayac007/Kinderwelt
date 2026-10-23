#!/usr/bin/env python3
"""Deterministic topical screening; not an answer or learning-effect oracle."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
# The two unresolved image gaps are intentionally visible review warnings.
REQUIRES_IMAGES={key:row['reason'] for key,row in json.loads((ROOT/'scripts/content/answer-categories.json').read_text())['exceptions'].items() if key in ('physics_09','body_16')}

def evaluate(task):
    if task['kind']!='discovery':
        return {'id':task['id'],'score':None,'weak':False,'reason':'Non-science task; topical categories do not apply.'}
    catalog=json.loads((ROOT/'scripts/content/answer-categories.json').read_text())
    if 'comparison' in task:
        facts={}
        for line in (ROOT/'scripts/content/science-properties.tsv').read_text().splitlines():
            if not line or line.startswith('#'):continue
            subject,key,members,*text=line.split('|')
            if subject==task['subject']:facts[key]=set(members.split())
        selected=[facts[key] for key in task['comparison']['property_ids']]
        scores={o:sum(o in f for f in selected) for o in task['options']}
        valid=[o for o,n in scores.items() if n==task['comparison']['required_matches']]
        ok=valid==[task['answer']] and all(n>0 for n in scores.values())
        return {'id':task['id'],'score':None,'weak':not ok,'fact_matches':scores,'reason':'Each option must partially fit; exactly one meets the stated count. Factual source review remains separate.'}
    groups=[k for k,v in catalog['groups'].items() if set(task['options'])<=set(v['objects'])]
    exception=catalog['exceptions'].get(task['id'])
    if exception:
        unchanged=set(task['options'])==set(exception['options'])
        intentional=task['id'] in ('biology_32','body_29')
        return {'id':task['id'],'score':None,'weak':not (unchanged and intentional),'reason':exception['reason'],'reviewed_options_match':unchanged}
    return {'id':task['id'],'score':1.0 if groups else 0.0,'weak':not bool(groups),'comparison_groups':groups,
            'reason':'Reviewed topical comparison groups; not a proof of factual correctness or learning benefit.'}

def markdown(tasks,changes):
    all_tasks=[t for p in tasks for t in [p,*p.get('bonuses',[])]]
    rows=[evaluate(t) for t in all_tasks]
    document='# Antwortalternativen prüfen\n\nAktueller Prüfstand und verbleibende Warnungen: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die vollständige Prüfung umfasst Grundaufgaben **und Boni**; Einzelbewertungen werden ausschließlich nach `qa-results/distractors.json` geschrieben.\n\nDie kleine, nachvollziehbare Kategorietabelle liegt in `scripts/content/answer-categories.json`. Kategorien sind eine QA-Hilfe und erzeugen keine beliebigen falschen Antworten. Bei Merkmalsboni muss jedes falsche Bild wenigstens eine Aussage erfüllen; nur eine Option darf die geforderte Anzahl erfüllen. Die Richtigkeit der zugrunde liegenden Sachmerkmale ist eine eigene redaktionelle Prüfung.\n\n`pedagogy-base.tsv` erklärt jede neue Grundaufgabenkorrektur. Die 33 ursprünglichen Warnfälle sind als feste Regressionstest-Referenz aufgeführt; Helmaufgaben bleiben wegen fehlender alternativer Kopfbedeckungen ausdrücklich offen. Absichtliche Sicherheits-/Lebewesenkontraste sind begründete Ausnahmen. `distractor-changes.json` dokumentiert die frühere Kuratierung und ist keine Liste aller späteren Änderungen.\n\n```sh\npython3 scripts/content/generate.py\npython3 scripts/qa/distractors.py --check\npython3 scripts/qa/pedagogy.py --check\n```\n\nKeine automatische fachliche oder empirische Freigabe aus einer Kategorienübereinstimmung ableiten.\n'
    return document,rows

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks'];changes=json.loads((ROOT/'scripts/content/distractor-changes.json').read_text())
    document,rows=markdown(tasks,changes);dest=ROOT/'docs/distractor-review.md'
    if a.check:
        if not dest.exists() or dest.read_text()!=document:raise SystemExit('Distractor review is stale; regenerate it.')
    else:dest.write_text(document)
    output=ROOT/'qa-results';output.mkdir(exist_ok=True);(output/'distractors.json').write_text(json.dumps({'scope':'Heuristic screening, no educational efficacy or correctness certification','tasks':rows},ensure_ascii=False,indent=2)+'\n')
    print('Distractor audit:',len(rows),'base/bonus tasks;',sum(r['weak'] for r in rows),'review warnings; historical curations:',len(changes))
if __name__=='__main__':main()
