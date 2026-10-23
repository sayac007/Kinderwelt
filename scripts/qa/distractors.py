#!/usr/bin/env python3
"""Deterministic topical screening; not an answer or learning-effect oracle."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FINE={
 'mechanisms':'wheel gear lever pulley'.split(),
 'tools':'hammer screwdriver scissors magnet'.split(),
 'electrics':'battery bulb gear magnet'.split(),
 'materials':'wood metal glass paper fabric salt sand oil soap water ice steam'.split(),
 'water_states':'water ice steam'.split(),
 'garden':'leaf roots seed tree flower apple mushroom'.split(),
 'animals':'bird bee butterfly frog fish cat turtle worm mouse'.split(),
 'senses':'eye ear nose tongue hand'.split(),
 'internal':'heart lungs brain stomach bone tooth'.split(),
 'limbs':'hand foot'.split(),
 'navigation':'map globe compass'.split(),
 'landscapes':'mountain river sea island forest desert'.split(),
 'sky_weather':'sun moon star cloud rain snow'.split()}
BROAD={
 'technology':'wheel gear lever pulley bridge hammer screwdriver scissors magnet battery bulb helmet'.split(),
 'body':'eye ear nose tongue hand foot heart lungs brain stomach bone tooth'.split(),
 'nature':'sun moon star cloud rain snow mountain river sea island forest desert tree water ice steam sand'.split()}
EXEMPT={'biology_32':'Absichtlicher Kontrast Lebewesen/unbelebt; semantische Entfernung ist hier sinnvoll.',
        'body_29':'Absichtliche Unterscheidung Lebensmittel/gefährlicher Nicht-Lebensmittel; keine weiteren Lebensmittel als falsche Antwort einsetzen.'}
REQUIRES_IMAGES={
 'physics_09':'Andere Kopfbedeckungen und ein klares Sturzschutz-Szenario.',
 'physics_11':'Wippe, Drehpunkt und vergleichbare Bewegungsbilder; die allgemeine Drehpunktfrage nicht mit ebenfalls drehenden Geräten verschärfen.',
 'physics_16':'Bauplan-Vorlagen auf konkreten Trägermaterialien; auf vielen Oberflächen kann grundsätzlich gezeichnet werden.',
 'physics_18':'Hand in verschiedenen Aktionen; auch Fuß oder Werkzeug können einen Ball anschubsen.',
 'physics_32':'Verschiedene Brücken-/Stützenbilder und ein engeres Bauziel; auch Häuser benötigen tragfähige Teile.',
 'physics_34':'Solarzelle mit direkt unterschiedlichen Beleuchtungen; auch Mond-/Kunstlicht kann Solarzellen schwach versorgen.',
 'physics_35':'Sattel und Lenker; Zahnrad wäre ebenfalls eine sich drehende Fahrradkomponente.',
 'physics_38':'Seil, feste Befestigung und Rad einer konkreten Seilrolle.',
 'physics_40':'Unmagnetisierte Vergleichskörper mit klarer Materialkennzeichnung; Kompass und Erdkugel sind wegen Polen keine sicheren Ablenker.',
 'biology_02':'Unterschiedliche konkrete Brutplätze; ein Baum kann gleichzeitig Standort eines Nestes sein.',
 'biology_06':'Pflanze unter klar unterschiedlichen Beleuchtungen statt unpräzise Lichtquellen-Gegenstände.',
 'biology_18':'Gekennzeichnete Getränke; das tägliche Trinken nicht mit ebenso notwendigen Ressourcen verwechseln.',
 'biology_30':'Konkrete Entwicklungsschritte; Früchte enthalten Samen und auch andere Pflanzenteile ermöglichen Vermehrung.',
 'biology_33':'Konkrete Beobachtungshandlungen am Nest; Eier wären ebenfalls in Ruhe zu lassen.',
 'biology_36':'Konkrete Gartenmaßnahmen; Wasser, Bäume oder Samen können Bienen ebenfalls helfen.',
 'biology_37':'Konkrete Nahrung/Gänge-Aktionen; Würmer können verschiedene abgestorbene Pflanzenteile einziehen.',
 'biology_39':'Eichen-/andere Sämlinge; keine biologisch mehrdeutigen Pflanzenteile als falsche Antwort einsetzen.',
 'body_16':'Verschiedene Kopfbedeckungen in einem klaren Fahrrad-Sturzschutz-Szenario.',
 'body_40':'Verschiedene konkrete Greifhandlungen; ein Fuß darf wegen möglicher alternativer Körpernutzung nicht pauschal falsch sein.',
 'geography_14':'Konkrete Verkehrswege; Fähre/Steg können ebenfalls Ufer verbinden und brauchen eine präzisere Frage.',
 'geography_23':'Regen-/Verdunstungs-Pfeile; Schnee oder Hagel wären ebenfalls gültiger Niederschlag.',
 'geography_24':'Konkrete Quellbilder in unterschiedlicher Höhenlage statt überlappender Landschaftsbegriffe.',
 'geography_28':'Konkrete Waldschichten; Blumen und Pilze gehören ebenfalls zu einem Wald.',
 'geography_31':'Klarer Himmel/Wolkendecke; Mond wäre bei Sonnenfinsternis ebenfalls richtig.',
 'geography_32':'Konkrete Temperatur-/Schmelzszenen statt weiterer möglicher Wärmequellen.',
 'geography_35':'Ein Süßwassersee; generisches Wasser ist nicht automatisch eine falsche Alternative zum Meer.'}
SORTING=[
 ('physics_17','Geografie','Frage prüft Orientierung; Physik wäre bei Fokus Magnetnadel ebenfalls begründbar.'),
 ('physics_29','Geografie','Zeichnung von Straßen und Wegen ist hier Kartenlesen.'),
 ('physics_23','Mensch oder explizit Schallphysik','Aktuell wird das Sinnesorgan abgefragt; der Hinweis nennt zusätzlich Schwingungen.'),
 ('physics_30','Mensch','Direkte Sinnesorgan-Zuordnung einer Fahrradklingel.'),
 ('chemistry_09','Physik oder Stofftrennung beibehalten','Magnetkraft ist physikalisch; Gemischtrennung kann im Stoffkunde-Bereich bleiben.'),
 ('chemistry_32','Physik oder Stofftrennung beibehalten','Gleiche Abwägung Magnetwirkung versus Trennverfahren.'),
 ('chemistry_23','Physik','Sonnenwärme und Schmelzen; Schwerpunkt Wärmequelle.'),
 ('chemistry_24','Geografie/Sachkunde oder Wasserzustände beibehalten','Wolkenbildung; Fachziel ausdrücklich entscheiden.'),
 ('chemistry_25','Geografie/Sachkunde oder Stoffkunde beibehalten','Zusammensetzung von Regentropfen ist auch Stoffkunde.'),
 ('chemistry_26','Geografie/Sachkunde oder Stoffkunde beibehalten','Eiskristalle/Schnee ist fachübergreifend.')]

def tags(value,groups):return {key for key,items in groups.items() if value in items}
def proximity(task,value):
    answer=task['answer'];cue=task.get('object')
    if tags(value,FINE)&tags(answer,FINE):return 1.0
    if tags(value,FINE)&tags(cue,FINE):return .75
    if tags(value,BROAD)&(tags(answer,BROAD)|tags(cue,BROAD)):return .5
    return 0.0

def evaluate(task):
    if task['kind']!='discovery':
        return {'id':task['id'],'score':None,'weak':False,'reason':'Zahl-/Sprach-/Muster-/Formaufgabe: semantische Kategorien sind kein gültiger Maßstab.'}
    if task['id'] in EXEMPT:return {'id':task['id'],'score':None,'weak':False,'reason':EXEMPT[task['id']]}
    wrong=[v for v in task['options'] if v!=task['answer']]
    scores=[proximity(task,v) for v in wrong]
    score=sum(scores)/max(1,len(scores))
    return {'id':task['id'],'score':score,'weak':score<=.5,'distractors':dict(zip(wrong,scores)),
            'reason':'Nur Kategorien-Heuristik: 1 fein verwandt, 0.75 Cue-Bezug, 0.5 breites Thema, 0 fremd; keine Prüfung der richtigen Antwort.'}

def markdown(tasks,changes):
    results=[evaluate(t) for t in tasks];by_id={t['id']:t for t in tasks};weak=sorted([r for r in results if r['weak']],key=lambda r:(r['score'],r['id']))
    lines=['# Review der Antwortalternativen','','Alle 320 Aufgaben werden geprüft. Für Zahlen, Anlaute, Silben, Muster und Formen wird die Semantik-Heuristik ausdrücklich nicht angewendet. Für Sachfragen bewertet sie Kategorien der vorhandenen Bildobjekte: 1 feines Themenfeld, 0,75 Kontextbild, 0,5 breites Themenfeld, 0 themenfremd. Mittelwerte bis 0,5 markieren Prüfbedarf.','',f'**{len(changes)} Aufgaben kuratiert; keine richtige Antwort und kein Fach geändert. {len(weak)} Sachfragen bleiben heuristisch schwach.** Die Heuristik beurteilt weder fachliche Richtigkeit noch Eindeutigkeit oder pädagogische Wirksamkeit. Enge Kategorien können ebenfalls mehrdeutige Antworten erzeugen.','','## Tatsächliche Änderungen','','| Aufgabe | Bisherige Auswahl | Neue Auswahl | Begründung |','|---|---|---|---|']
    for c in changes:
        note=c['reason']
        if c['question_before']!=c['question_after']:note+=' Frage in allen drei Sprachen präzisiert.'
        lines.append('| '+c['id']+' | '+', '.join(c['options_before'])+' | '+', '.join(c['options_after'])+' | '+note+' |')
    lines+=['','Besonders relevant: `biology_32` enthielt eine Blume als angeblich falsche Alternative zu „Lebewesen“. Diese war ebenfalls lebendig. Sie wurde durch das in der Frage genannte Glas ersetzt; die Maus bleibt richtig. Fragen zu warmem Regen, Achsenmaterial und allgemeinem Helfen/Schützen wurden eingegrenzt, bevor nähere Ablenker eingesetzt wurden.','','## Weiterhin auffällige Aufgaben','','| Aufgabe | Wert | Frage | Ablenker |','|---|---:|---|---|']
    for r in weak:
        t=by_id[r['id']];lines.append(f"| {r['id']} | {r['score']:.2f} | {t['prompt']} | "+', '.join(f'{k}: {v:g}' for k,v in r['distractors'].items())+' |')
    lines+=['','## Fehlende Bilder und bewusst unveränderte Aufgaben','','Die folgenden Aufgaben wurden **nicht geändert**. Für einen fachlich sicheren Umbau wären neue konkrete Bilder/Szenen oder eine gesondert geprüfte Aufgabenfassung nötig. Vorhandene Gegenstände wurden nicht bloß wegen ähnlicher Kategorien als falsche Antworten eingesetzt.','','| Aufgabe | Bedarf / Risiko |','|---|---|']
    for id,reason in REQUIRES_IMAGES.items():lines.append(f'| {id} | {reason} |')
    lines+=['','## Fachzuordnung: Vorschläge, keine Umsortierung','','Die Bereiche sind für frühe Sachkunde fachübergreifend. Zustandsänderungen sind keine chemischen Reaktionen; ihre Behandlung als Stoffkunde ist trotzdem möglich. Die folgende Liste schlägt Schwerpunktentscheidungen vor. **Keine Aufgabe wurde verschoben.**','','| Aufgabe | Möglicher Schwerpunkt | Begründung |','|---|---|---|']
    for id,target,why in SORTING:lines.append(f'| {id} | {target} | {why} |')
    lines+=['','## Reproduzieren','','```sh','python3 scripts/content/generate.py','python3 scripts/qa/distractors.py','python3 scripts/qa/distractors.py --check','```','','Änderungen liegen in den TSV-Quellen; `distractor-changes.json` protokolliert die Kuratierung. `science-answer-fixtures.json` sichert die zuvor freigegebenen Antworten/Fächer unabhängig von der Generierung. Ein Prüfbericht in `qa-results/distractors.json` enthält alle 320 Einzelbewertungen. Muttersprachliche und fachliche Abnahme bleiben offen.','']
    return '\n'.join(lines),results

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks'];changes=json.loads((ROOT/'scripts/content/distractor-changes.json').read_text())
    document,rows=markdown(tasks,changes);dest=ROOT/'docs/distractor-review.md'
    if a.check:
        if not dest.exists() or dest.read_text()!=document:raise SystemExit('Distractor review is stale; regenerate it.')
    else:dest.write_text(document)
    output=ROOT/'qa-results';output.mkdir(exist_ok=True);(output/'distractors.json').write_text(json.dumps({'scope':'Heuristic screening, no educational efficacy or correctness certification','tasks':rows},ensure_ascii=False,indent=2)+'\n')
    print('Distractor audit:',len(rows),'tasks;',sum(r['weak'] for r in rows),'flagged;',len(changes),'curated; answers unchanged.')
if __name__=='__main__':main()
