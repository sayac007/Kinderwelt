#!/usr/bin/env python3
"""Render the localization review; structural guards cannot certify semantics."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def markdown():
    log=json.loads((ROOT/'scripts/content/localization-changes.json').read_text())
    lines=['# Lokalisierungsabgleich','','Verglichen: alle 320 Fragen und Hinweise in Deutsch, Englisch und Russisch (960 Sprachfassungen). Die 200 Sachfragen wurden inhaltlich auf Objekte, Bedingungen, Mengen, Verneinungen und Sicherheitshinweise abgeglichen; außerdem alle 120 Mathe-, Deutsch- und Logikaufgaben. Dies ist eine redaktionelle Prüfung, keine unabhängige muttersprachliche Freigabe.','',f"{len(log['changes'])} Textfelder in {len({c['id'] for c in log['changes']})} Aufgaben geändert; Ausgangscommit `{log['baseline_commit']}`. Richtige Antworten, Zuordnung, Bilder und Mechanik bleiben erhalten. Die ursprünglichen 24 deutschen Aufgabentexte bleiben wortgleich.",'','## Abgleich und Grenzen','','- Mengenaufgaben nennen die Gegenstände, wenn die deutsche Fassung sie nennt. Ursprüngliche Zahlenfolgen und konkrete Hinweise sind in EN/RU vollständig.','- Deutsche Lernwörter, einzelne Buchstaben und Klatsch-Silben stehen auch in EN/RU auf dem Bildschirm. Die Erklärung wird lokal gesprochen, anschließend folgen Wort und Hinweis aus der deutschen Aufnahme. Fremdsprachige Modelle sprechen keine deutschen Lernwörter vor.','- Sachfragen behalten Einschränkungen wie „meist“, „nicht alle“, „bei Raumtemperatur“, „unsichtbar“, konkrete Materialien und Hilfe durch Erwachsene. Ergänzt wurden unter anderem Kraftwirkung, dicht beieinander stehende Bäume, abgestorbene Blätter, langer Fluss und die Unterscheidung Sinn/Körperteil.','- Keine automatische Behauptung vollständiger Bedeutungsäquivalenz. Tests schützen ausgewählte konkrete Informationsverluste und die Reproduzierbarkeit.','','## Noch durch Muttersprachler / Fachpersonen prüfen','','- EN/RU: natürliches Sprechtempo und Verständnis bei Kindern der ersten und zweiten Klasse; alle 320 Aufgaben im Kontext der Bilder.','- RU: technische Begriffe „блок“ (Seilrolle), „качели-доска“, „ось“, „вкусовые почки“ und Schulkontext der Fremdsprachensilben. Verständlichkeit gezielt beobachten; keine ungeprüften Fachbegriffe ersetzen.','- EN: „food pipe“, „forewings/hindwings“, „precipitation“ und „physiology“ auf altersgerechtes Verständnis prüfen.','- Deutsche Rechtschreibung versus gehörte Anlaute (z. B. Sonne): die Fragen prüfen den Anfangsbuchstaben; keine Lautschrift oder Übersetzung des Lernworts lehren.','- Mehrsprachige Bildschirmtexte und deutsche Folgeaufnahme gemeinsam hören; ASR allein kann diese Lernsequenzen nicht freigeben.','','## Vollständiges Änderungsprotokoll','','| Aufgabe | Sprache | Feld | Vorher | Jetzt |','|---|---|---|---|---|']
    for c in log['changes']:
        cells=[c['id'],c['locale'],c['field'],c['before'],c['after']]
        lines.append('| '+' | '.join(v.replace('|','\\|') for v in cells)+' |')
    return '\n'.join(lines)+'\n'
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=ROOT/'docs/localization-review.md';value=markdown()
    if a.check:
        if not path.exists() or path.read_text()!=value:raise SystemExit('Localization review is stale')
    else:path.write_text(value)
    print('Localization review: 320 tasks, 3 locales; authored changes documented; human review OPEN')
if __name__=='__main__':main()
