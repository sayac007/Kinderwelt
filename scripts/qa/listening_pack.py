#!/usr/bin/env python3
"""Create a single offline listening page from the actual shipped recordings.

No network, recording, storage, telemetry or participant information. German
learning samples play the same localized/native sequence as the application.
"""
import argparse,base64,hashlib,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
IDS=['area_'+s for s in ['math','german','logic','physics','biology','chemistry','body','geography']]+['math_count','german_sun','german_robot_hint','physics_05_hint','chemistry_20','praise_1']
STYLE='body{font:18px system-ui;max-width:980px;margin:2rem auto;padding:0 1rem;color:#17384c;background:#fff9eb}h1{font-size:1.8rem}button,select{font:inherit;padding:.65rem;margin:.3rem;border-radius:1rem;border:2px solid #407087;background:#fff}button:focus{outline:3px solid #d68d1c}article{border-top:1px solid #bdc6c9;padding:1rem 0}audio{width:100%;position:sticky;top:0;background:#fff9eb}summary{cursor:pointer}small{overflow-wrap:anywhere}p{line-height:1.5}'
SCRIPT=r'''
const clips=JSON.parse(document.getElementById('data').textContent);
const player=document.getElementById('player'),status=document.getElementById('status');
let remaining=[],active=null;
function next(){
 if(!remaining.length){status.textContent='Vollständig abgespielt.';return;}
 const item=remaining.shift();player.src=item.audio;player.playbackRate=Number(document.getElementById('speed').value);
 status.textContent=active.locale+' / '+active.id+' — '+item.locale;
 player.play().catch(()=>{status.textContent='Bitte Wiedergabe am Audioplayer starten.';});
}
player.addEventListener('ended',next);
player.addEventListener('error',()=>{status.textContent='Wiedergabe fehlgeschlagen. Bitte einen aktuellen Browser mit Ogg-Unterstützung verwenden.';remaining=[];});
document.getElementById('speed').addEventListener('change',e=>{player.playbackRate=Number(e.target.value);});
for(const button of document.querySelectorAll('[data-index]'))button.addEventListener('click',()=>{
 player.pause();active=clips[Number(button.dataset.index)];remaining=active.sequence.slice();next();
});
'''
def generate(output):
    models={};catalogs={}
    for locale in ['de','en','ru']:
        folder=ROOT/'assets/voice/quest'/locale;m=json.loads((folder/'manifest.json').read_text());catalogs[locale]={c['id']:c for c in m['clips']}
        models[locale]={'model':m['model'],'license':m['dataset_license'],'card':(folder/'MODEL_CARD.txt').read_text()}
    items=[];rows=[]
    for locale in ['de','en','ru']:
        for id in IDS:
            refs=[(locale,id)]
            if locale!='de' and id.startswith('german_'):refs.append(('de',id))
            sequence=[]
            for lang,key in refs:
                c=catalogs[lang][key];raw=(ROOT/'assets/voice/quest'/lang/c['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['sha256']
                sequence.append({'locale':lang,'reference':c['text'],'sha256':c['sha256'],'audio':'data:audio/ogg;base64,'+base64.b64encode(raw).decode()})
            index=len(items);items.append({'locale':locale,'id':id,'sequence':sequence})
            reference='<br>'.join(html.escape(s['locale']+': '+s['reference']) for s in sequence)
            rows.append(f'<article><strong>{locale.upper()} · {html.escape(id)}</strong> <button data-index="{index}">Anhören</button><details><summary>Erwarteten Text zeigen</summary><p>{reference}</p></details></article>')
    cards=''.join('<details><summary>'+html.escape(l+': '+m['model']+' · '+m['license'])+'</summary><pre>'+html.escape(m['card'])+'</pre></details>' for l,m in models.items())
    # Keep literal </script and other HTML delimiters out of embedded JSON.
    data=json.dumps(items,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    version=json.loads((ROOT/'scripts/android/app-config.json').read_text())['version_name']
    document='<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; media-src data:; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'"><title>Kinderwelt Hörprobe '+html.escape(version)+'</title><style>'+STYLE+'</style><h1>Kinderwelt '+html.escape(version)+' · Hörprobe</h1><p>Für die Hörprüfung durch Erwachsene: zuerst ohne Text anhören, dann den erwarteten Text öffnen. Besonders auf Wortanfänge, Wortenden, Verneinungen und Antwortoptionen achten. Die Seite speichert oder übermittelt nichts und nimmt keinen Ton auf. Ohne Musik; die Balance mit Musik bitte in der APK prüfen.</p><p>Deutsch-Lernproben spielen in EN/RU zuerst die lokalisierte Erklärung und danach die deutsche Aufnahme. Standardtempo 1× entspricht der App.</p><audio id="player" controls preload="none"></audio><p id="status" role="status">Eine Probe wählen.</p><label>Tempo <select id="speed"><option value="1">1× · App-Tempo</option><option value="0.85">0,85× · nur zur Prüfung</option></select></label>'+''.join(rows)+'<h2>Modellnachweise</h2>'+cards+'<script type="application/json" id="data">'+data+'</script><script>'+SCRIPT+'</script></html>'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(document)
    print('Created',len(items),'offline listening sequences:',output)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();generate(a.output)
