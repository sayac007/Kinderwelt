#!/usr/bin/env python3
"""Offline adult audio review with hash-bound receipts, no personal fields.

Human declarations stay distinct from technical tests. This tool never grants
pedagogical effectiveness, legal clearance or publication approval.
"""
import argparse,hashlib,html,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ISSUES=['stress','word','onset','ending','number','instruction','level']
def digest(raw):return hashlib.sha256(raw).hexdigest()
def catalog(root=ROOT):
    cases=[]
    for locale in ['de','en','ru']:
        folder=root/'assets/voice/quest'/locale
        bank=json.loads((folder/'manifest.json').read_text());grouped={}
        for clip in bank['clips']:
            name=clip['file']
            if Path(name).name!=name or not name.endswith('.ogg'):raise ValueError('Invalid audio filename')
            key=locale+':'+clip['sha256']
            row={'key':key,'locale':locale,'sha256':clip['sha256'],'text_sha256':digest(clip['text'].encode()),'reference':clip['text'],'gain_db':clip.get('playback_gain_db',0),'audio':locale+'/'+name,'ids':[]}
            if key in grouped:
                if any(row[k]!=grouped[key][k] for k in ['text_sha256','gain_db']):raise ValueError('Same audio has conflicting references/gain')
            else:grouped[key]=row
            grouped[key]['ids'].append(clip['id'])
        for row in grouped.values():
            if digest((folder/Path(row['audio']).name).read_bytes())!=row['sha256']:raise ValueError('Actual recording differs from manifest')
        cases.extend(grouped.values())
    content=digest(b''.join((root/p).read_bytes() for p in ['games/quest/tasks.json','games/quest/languages.json']))
    contract=digest(json.dumps({'content':content,'cases':cases},ensure_ascii=False,sort_keys=True).encode())
    return {'schema':1,'scope':'Declared adult listening only; no personal fields or automatic human certification','contract_sha256':contract,'content_sha256':content,'cases':cases}
def verify(receipt,expected,locale=None):
    if set(receipt)!={'schema','contract_sha256','reviews'} or receipt['schema']!=1:raise ValueError('Unexpected receipt fields/schema')
    if receipt['contract_sha256']!=expected['contract_sha256']:raise ValueError('Stale audio/content contract')
    wanted={c['key']:c for c in expected['cases'] if locale is None or c['locale']==locale};known={c['key']:c for c in expected['cases']};seen={}
    for row in receipt['reviews']:
        if set(row)!={'key','sha256','text_sha256','status','issue'}:raise ValueError('Unexpected review fields; do not add personal information')
        if row['key'] not in known or row['key'] in seen:raise ValueError('Unknown or duplicate review')
        actual=known[row['key']]
        if any(row[k]!=actual[k] for k in ['sha256','text_sha256']):raise ValueError('Stale recording/reference')
        if row['status'] not in ['PASS','ISSUE'] or (row['status']=='PASS' and row['issue']!='') or (row['status']=='ISSUE' and row['issue'] not in ISSUES):raise ValueError('Invalid declared review status')
        seen[row['key']]=row
    missing=set(wanted)-set(seen);issues=[k for k in wanted if k in seen and seen[k]['status']=='ISSUE']
    status='ISSUES' if issues else 'INCOMPLETE' if missing else 'DECLARED_REVIEW_COMPLETE'
    return {'status':status,'required':len(wanted),'reviewed':len(set(wanted)&set(seen)),'open':len(missing),'issues':issues,'scope':'Hash-bound human declarations only, not an independently witnessed or empirical approval'}
def prepare(output,root=ROOT):
    if output.exists():raise ValueError('Output must be a new directory')
    data=catalog(root);output.mkdir(parents=True)
    for row in data['cases']:
        src=root/'assets/voice/quest'/row['audio']
        if digest(src.read_bytes())!=row['sha256']:raise ValueError('Audio hash mismatch: '+row['audio'])
        dst=output/row['audio'];dst.parent.mkdir(exist_ok=True);shutil.copy2(src,dst)
    for locale in ['de','en','ru']:
        for source in (root/'assets/voice/quest'/locale).glob('*.txt'):shutil.copy2(source,output/locale/source.name)
    (output/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    document='''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; media-src 'self' file:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'"><title>Kinderwelt – vollständige Hörabnahme</title><style>body{font:18px system-ui;max-width:900px;margin:2rem auto;padding:1rem;background:#fff9eb;color:#17384c}button,select,input{font:inherit;padding:.7rem;margin:.3rem}audio{width:100%}p{line-height:1.5}pre{white-space:pre-wrap}label{display:block}</style><h1>Hörabnahme durch Erwachsene</h1><p>Zuerst ohne Text bei 1× anhören. Dann Text öffnen und erneut hören: richtige Wörter, Betonung, Zahlen, Wortanfänge und -enden? Nur tatsächlich geprüfte Aufnahmen markieren. Eine Markierung ist eine eigene Erklärung, keine automatische Freigabe.</p><p>Keine Namen, Aufnahmen, Telemetrie oder automatische Speicherung. Ergebnisse bleiben bis zum freiwilligen lokalen JSON-Download im Arbeitsspeicher. Beim Schließen gehen sie verloren. Die Geräte-/Musikbalance zusätzlich in der APK prüfen.</p><select id="lang" aria-label="Sprache"><option value="de">Deutsch</option><option value="en">English</option><option value="ru">Русский</option></select><input id="search" placeholder="Aufgaben-ID suchen" aria-label="Aufgaben-ID"><p id="progress" role="status"></p><p id="ids"></p><audio id="audio" controls preload="none"></audio><details id="details"><summary>Erwarteten Text zeigen</summary><pre id="reference"></pre></details><label><input id="ack" type="checkbox">Ich habe die ganze Aufnahme gehört und mit dem Text verglichen.</label><button id="pass" disabled>Verständlich / Betonung passt</button><select id="issue" aria-label="Auffälligkeit"><option value="stress">Betonung</option><option value="word">Wort unverständlich</option><option value="onset">Wortanfang</option><option value="ending">Wortende</option><option value="number">Zahl / Rechenzeichen</option><option value="instruction">Anweisung</option><option value="level">Lautstärke</option></select><button id="fail" disabled>Auffällig</button><p><button id="previous">Zurück</button><button id="next">Weiter / offen lassen</button><button id="export">Meine bisherigen Ergebnisse herunterladen</button></p><label>Frühere Ergebnisse fortsetzen: <input type="file" id="restore" accept="application/json,.json"></label><p id="message" role="status"></p><script type="application/json" id="data">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('data').textContent), reviews=new Map();
const el=id=>document.getElementById(id), player=el('audio');
const Context=window.AudioContext||window.webkitAudioContext, context=Context?new Context():null, gain=context?context.createGain():null;
if(context){context.createMediaElementSource(player).connect(gain);gain.connect(context.destination);}
let index=0,rows=[],ended=false;
function draw(){const c=rows[index];el('ack').checked=false;ended=false;el('pass').disabled=el('fail').disabled=true;el('details').open=false;player.pause();el('progress').textContent=(rows.length?index+1:0)+' / '+rows.length+' · markiert: '+reviews.size+' / '+data.cases.length;if(!c){player.removeAttribute('src');el('ids').textContent='Keine Treffer';el('reference').textContent='';return;}el('ids').textContent=c.locale+' · '+c.ids.join(', ');el('reference').textContent=c.reference;player.src=c.audio;if(gain)gain.gain.value=Math.pow(10,c.gain_db/20);}
function filter(){index=0;rows=data.cases.filter(c=>c.locale===el('lang').value&&c.ids.some(id=>id.includes(el('search').value.trim())));draw();}
player.addEventListener('play',()=>{if(context)context.resume();});player.addEventListener('ended',()=>{ended=true;});
el('ack').addEventListener('change',()=>{el('pass').disabled=el('fail').disabled=!(ended&&el('ack').checked);});
function mark(status){const c=rows[index];if(!c||!ended||!el('ack').checked)return;reviews.set(c.key,{key:c.key,sha256:c.sha256,text_sha256:c.text_sha256,status,issue:status==='ISSUE'?el('issue').value:''});index=Math.min(index+1,rows.length-1);draw();}
el('pass').onclick=()=>mark('PASS');el('fail').onclick=()=>mark('ISSUE');el('next').onclick=()=>{index=Math.min(index+1,rows.length-1);draw();};el('previous').onclick=()=>{index=Math.max(0,index-1);draw();};el('lang').onchange=filter;el('search').oninput=filter;
el('restore').onchange=async()=>{try{const r=JSON.parse(await el('restore').files[0].text());if(r.schema!==1||r.contract_sha256!==data.contract_sha256||!Array.isArray(r.reviews))throw Error('Anderer Inhaltsstand oder ungültiges Format');const known=new Map(data.cases.map(c=>[c.key,c]));const restored=new Map();for(const row of r.reviews){const c=known.get(row.key);if(!c||row.sha256!==c.sha256||row.text_sha256!==c.text_sha256||restored.has(row.key)||!['PASS','ISSUE'].includes(row.status))throw Error('Unbekannte oder veraltete Aufnahme');if((row.status==='PASS'&&row.issue!=='')||(row.status==='ISSUE'&&!['stress','word','onset','ending','number','instruction','level'].includes(row.issue)))throw Error('Ungültige Kategorie');restored.set(row.key,{key:row.key,sha256:row.sha256,text_sha256:row.text_sha256,status:row.status,issue:row.issue});}for(const [key,row] of restored)reviews.set(key,row);el('message').textContent='Frühere Markierungen übernommen; keine neue Hörprüfung behauptet.';draw();}catch(error){el('message').textContent='Import abgelehnt: '+error.message;}};
el('export').onclick=()=>{const result={schema:1,contract_sha256:data.contract_sha256,reviews:[...reviews.values()]};const url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='kinderwelt-listening-review.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};filter();
</script></html>'''.replace('PAYLOAD',payload)
    (output/'index.html').write_text(document)
    return {'cases':len(data['cases']),'bindings':sum(len(c['ids']) for c in data['cases']),'output':str(output),'human_review':'OPEN'}
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    build=sub.add_parser('prepare');build.add_argument('--output',required=True,type=Path)
    check=sub.add_parser('verify');check.add_argument('--receipt',required=True,type=Path);check.add_argument('--locale',choices=['de','en','ru'])
    a=p.parse_args()
    if a.action=='prepare':result=prepare(a.output)
    else:result=verify(json.loads(a.receipt.read_text()),catalog(),a.locale)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if a.action=='verify' and result['status']!='DECLARED_REVIEW_COMPLETE':raise SystemExit(2)
if __name__=='__main__':main()
