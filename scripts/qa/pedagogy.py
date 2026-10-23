#!/usr/bin/env python3
"""Offline editorial regression and review diagnostics, not a learning-effect test."""
import argparse,collections,hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOCALES=('de','en','ru')
def normalized(text):return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',text).casefold()))
def flatten(tasks):return [t for p in tasks for t in [p,*p.get('bonuses',[])]]
def properties(root=ROOT):
    result={}
    for line in (root/'scripts/content/science-properties.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        subject,key,members,*texts=line.split('|')
        result.setdefault(subject,{})[key]={'members':set(members.split()),'texts':dict(zip(LOCALES,texts))}
    return result

def logic_errors(task):
    errors=[];rule=task.get('logic_rule',{})
    if rule.get('operation')=='sum-next-two':
        seq=rule['given'];differences=[b-a for a,b in zip(seq,seq[1:])]
        if [int(n) for n in re.findall(r'\d+',task['display'])]!=seq:errors.append('visible-sequence-drift')
        if len(differences)<3 or differences[0]==differences[1] or any(d!=differences[i%2] for i,d in enumerate(differences)):
            errors.append('alternating-steps');return errors
        first=seq[-1]+differences[(len(seq)-1)%2];second=first+differences[len(seq)%2]
        if rule['continuation']!=[first,second] or task['answer']!=first+second:errors.append('continuation-answer')
        if rule['steps']!=differences[:2]:errors.append('rule-metadata')
    elif rule.get('operation')=='inverse-function':
        (x1,y1),(x2,y2)=rule['examples'];answer=task['answer']
        if [int(n) for n in re.findall(r'\d+',task['display'])]!=[x1,y1,x2,y2,rule['output']]:errors.append('visible-example-drift')
        if x2==x1 or y2-y1!=2*(x2-x1) or rule['multiply']!=2:errors.append('inverse-rule')
        if 2*answer+(y1-2*x1)!=rule['output'] or y1-2*x1!=rule['add']:errors.append('inverse-answer')
    else:errors.append('missing-logic-rule')
    return errors

def inspect(tasks,root=ROOT):
    failures=[];warnings=[];all_tasks=flatten(tasks);facts=properties(root)
    languages=json.loads((root/'games/quest/languages.json').read_text())
    categories=json.loads((root/'scripts/content/answer-categories.json').read_text())
    expected=set(json.loads((root/'games/quest/legacy-rewards.json').read_text())['rewards'])
    if {t['id'] for t in tasks}!=expected or len(tasks)!=320:failures.append('Base IDs/count changed')
    expected_all=expected|{p+'_bonus_'+str(n) for p in expected for n in (1,2)}
    if {t['id'] for t in all_tasks}!=expected_all or len(all_tasks)!=960:failures.append('Bonus IDs/count changed')
    prompt_groups=collections.defaultdict(list);option_groups=collections.defaultdict(list);type_counts=collections.Counter()
    owners={b['id']:p['id'] for p in tasks for b in p.get('bonuses',[])}
    for t in all_tasks:
        id=t['id'];parent=t.get('parent_id',id);subject=t['subject'];type_counts[(subject,t['kind'])]+=1
        if 'parent_id' in t:
            p=next((x for x in tasks if x['id']==parent),None)
            if not p or p['subject']!=subject or owners.get(id)!=parent or id not in (parent+'_bonus_1',parent+'_bonus_2') or t.get('optional') is not True or t['points']!=(50 if id.endswith('_1') else 100):failures.append(id+': inconsistent parent/reward')
        for locale in LOCALES:
            v=t if locale=='de' else {**t,**t.get('variants',{}).get(locale,{})}
            options=v['options'];answer=v['answer'];text=t['texts'][locale];hint=text['tip']
            if len(options)!=3 or options.count(answer)!=1 or len(options)!=len(set(map(str,options))):failures.append(id+': duplicate/missing answer '+locale)
            if re.search(r'gesucht ist|the answer is|ответ\s*:|die lücke[n]? brauch|the missing letters are|на месте пропуска|в пропусках\s*:',hint,re.I):failures.append(id+': solution-prefix '+locale)
            if subject=='german':
                # Match spelling sequences, not incidental words such as "a".
                listed=r'(?<!\w)'+r'\s*\.\s*'.join(re.escape(c) for c in str(answer))+r'\s*\.'
                if re.search(listed,hint,re.I):failures.append(id+': missing-letter-list '+locale)
                if str(v['word']).casefold() in hint.casefold():failures.append(id+': complete-word-in-hint '+locale)
            if t['kind']=='discovery':
                labels=[languages['objects'][str(answer)][locale],v.get('option_labels',{}).get(str(answer),'')]
                for label in set(labels)-{''}:
                    suffix=r'\w*' if locale=='de' and len(label)>=4 and ' ' not in label else r'(?!\w)'
                    if re.search(r'(?<!\w)'+re.escape(label)+suffix,hint,re.I):failures.append(id+': named-science-answer '+locale)
            result_prefix=r'(?:zuletzt|finally|в конце|(?:das\s+)?(?:endergebnis|ergebnis|lösung)\s*(?:ist|lautet|:|=)|(?:final\s+)?(?:answer|result)\s*(?:is|:|=)|(?:итог|ответ|результат)\s*(?:равен|:|=)?)'
            if subject=='math' and re.search(result_prefix+r'\s*'+re.escape(str(answer))+r'\b',hint,re.I):failures.append(id+': final-result '+locale)
            if locale=='ru' and re.search('[A-Za-z]',text['prompt']+hint):failures.append(id+': Latin learning text')
            prompt_groups[(subject,t['kind'],locale,normalized(text['prompt']))].append((id,parent,t.get('display','')))
            option_groups[(subject,t['kind'],locale,str(answer),tuple(sorted(map(str,options))))].append(id)
        if t['subject']=='logic' and 'parent_id' in t:
            failures.extend(id+': '+err for err in logic_errors(t))
            rule=t['logic_rule']
            numbers=rule.get('given') or [n for pair in rule.get('examples',[]) for n in pair]+[rule.get('output')]
            hint_parameter=rule['steps'][0] if 'steps' in rule else rule['add']
            for locale in LOCALES:
                if [int(n) for n in re.findall(r'\d+',t['texts'][locale]['prompt'])]!=numbers:failures.append(id+': spoken-rule-data-drift '+locale)
                if not re.search(r'\b'+str(hint_parameter)+r'\b',t['texts'][locale]['tip']):failures.append(id+': hint-rule-parameter-drift '+locale)
        if t['kind']=='discovery' and 'comparison' not in t:
            common=[k for k,v in categories['groups'].items() if set(t['options'])<=set(v['objects'])]
            exception=categories['exceptions'].get(id)
            if exception and set(t['options'])!=set(exception['options']):failures.append(id+': unreviewed exception options')
            if not common and not exception:failures.append(id+': unrelated comparison categories')
            if exception:warnings.append({'id':id,'dimension':'distractors','reason':exception['reason'],'open_image_gap':id in ('physics_09','body_16')})
        if 'comparison' in t:
            c=t['comparison']
            if c.get('model')!=subject or len(set(c['property_ids']))!=len(c['property_ids']) or any(k not in facts[subject] for k in c['property_ids']):
                failures.append(id+': invalid property source reference');continue
            selected=[facts[subject][key] for key in c['property_ids']];scores={o:sum(o in f['members'] for f in selected) for o in t['options']}
            valid=[o for o,n in scores.items() if n==c['required_matches']]
            if valid!=[t['answer']]:failures.append(id+': scientific comparison has missing/ambiguous answer')
            if any(n==0 for n in scores.values()):failures.append(id+': wholly unrelated distractor')
            if any(not 0<sum(o in f['members'] for o in t['options'])<3 for f in selected):failures.append(id+': irrelevant or non-discriminating fact')
            if len(selected)!=(3 if t['points']==50 else 4) or c['required_matches']!=len(selected)-1:failures.append(id+': comparison complexity')
            for locale in LOCALES:
                if not all(f['texts'][locale] in t['texts'][locale]['prompt'] for f in selected):failures.append(id+': source/content reference drift')
            warnings.append({'id':id,'dimension':'difficulty','indicator':len(selected)*3,'reason':'Possible factual judgements plus exact-count/negative constraint. Editorial progression, not empirical difficulty evidence.'})
    difficulty=[]
    for parent in tasks:
        for bonus in parent['bonuses']:
            subject=parent['subject'];indicator={};easier=False
            if subject=='math':
                base_ops=len(re.findall(r'[+−-]',parent['display']))
                bonus_ops=len(re.findall(r'[+−-]',bonus['display']))
                indicator={'base_operations':base_ops,'bonus_operations':bonus_ops,'inverse':bonus['points']==100}
                easier=bonus_ops<=base_ops
            elif subject=='german':
                base_gaps=len(parent['answer']);bonus_gaps=len(bonus['answer'])
                indicator={'base_gaps':base_gaps,'bonus_gaps':bonus_gaps};easier=bonus_gaps<=base_gaps
            elif subject=='logic':indicator={'bonus_rule':bonus['logic_rule']['operation'],'additional_process':'continue twice and add, or infer rule and reverse it'}
            else:indicator={'possible_factual_judgements':len(bonus['comparison']['property_ids'])*3,'exact_count':bonus['comparison']['required_matches'],'professional_transfer_review':'OPEN'}
            if easier:failures.append(bonus['id']+': likely easier without an additional process')
            difficulty.append({'id':bonus['id'],'parent_id':parent['id'],'probably_easier_structurally':easier,'indicator':indicator,'scope':'Review indicator only; no empirical age/difficulty claim'})
    duplicates=[]
    for (subject,kind,locale,prompt),records in prompt_groups.items():
        if len(records)<2:continue
        cross=len({r[1] for r in records})>1
        bonus=[r for r in records if '_bonus_' in r[0]]
        row={'subject':subject,'kind':kind,'locale':locale,'ids':[r[0] for r in records],'cross_station':cross,'mathematical_template_exception':subject=='math' and len({r[2] for r in records})==len(records)}
        duplicates.append(row)
        if cross and len({r[1] for r in bonus})>1 and subject!='math':failures.append('Duplicate non-math bonuses: '+','.join(r[0] for r in bonus))
        if subject=='math':
            displayed=collections.defaultdict(list)
            for record in bonus:displayed[re.sub(r'\s+','',record[2].replace('−','-'))].append(record)
            for same in displayed.values():
                if len({r[1] for r in same})>1:failures.append('Duplicate identical math bonuses: '+','.join(r[0] for r in same))
    baseline=json.loads((root/'tests/fixtures/pedagogy/baseline-cases.json').read_text())
    by_id={t['id']:t for t in tasks}
    rechecks=[{'id':id,'current_options':by_id[id]['options'],'review':by_id[id].get('pedagogical_review',''),'remaining_image_warning':id in ('physics_09','body_16')} for id in baseline['weak_base_ids'] if id in by_id]
    return {'failures':sorted(set(failures)),'status':'FAIL' if failures else 'PASS','scope':'Offline consistency and editorial diagnostics; no professional, child-usability or learning-effect certification',
        'base_tasks':len(tasks),'bonus_tasks':len(all_tasks)-len(tasks),'typed_counts':[{'subject':s,'kind':k,'count':n} for (s,k),n in sorted(type_counts.items())],
        'text_repetitions':duplicates,'repeated_answer_option_sets':[{'subject':s,'kind':k,'locale':l,'ids':ids} for (s,k,l,answer,opts),ids in option_groups.items() if len(ids)>1],
        'baseline_33_rechecks':rechecks,'difficulty_review':difficulty,'review_warnings':warnings,'limitations':['A mathematically possible intermediate result or operand equal to the final answer is not itself a hint leak. Explicit final-result wording is rejected.', 'An English article such as a is not treated as a spelled missing-letter answer. Short German Ei must not match Eine or Eigenschaft; longer names include compounds such as Eisenstueck.', 'Same-word bonuses inside one station are allowed when the gaps differ. Across-station duplicate non-math prompts are rejected.', 'Science facts describe the stated models; professional review, pronunciation and empirical difficulty remain open.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--output',type=Path,default=ROOT/'qa-results/pedagogy.json');a=p.parse_args()
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks'];r=inspect(tasks);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('Pedagogy:',r['status'],';',r['base_tasks'],'base +',r['bonus_tasks'],'bonuses;',len(r['failures']),'regressions; professional/empirical review OPEN')
    for f in r['failures']:print(f)
    raise SystemExit(1 if r['failures'] else 0)
if __name__=='__main__':main()
