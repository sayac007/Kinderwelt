#!/usr/bin/env python3
"""Render the localization review; structural guards cannot certify semantics."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def markdown():
    log=json.loads((ROOT/'scripts/content/localization-changes.json').read_text())
    lines=['# Lokalisierungsabgleich', '',
        '0.9.0 enthält 320 Grundaufgaben und 640 freiwillige Bonusaufgaben in jeweils drei Sprachen. Die Strukturprüfung deckt Übersetzungsfelder, Antwortoptionen, native Lernwörter und kyrillische russische Inhalte ab. Sie ersetzt keine muttersprachliche oder fachliche Freigabe.', '',
        f"{len(log['changes'])} geänderte Grundaufgaben-Textfelder seit Ausgangscommit `{log['baseline_commit']}` sind unten protokolliert. Bonusinhalte stehen vollständig in `tasks.json` und den versionierten Inhaltsquellen.", '',
        '## Aktuelle Regeln', '',
        '- Deutsch vermittelt deutsche, English englische und Русский russische Lernwörter, Anfangsbuchstaben und Silben. Keine automatische deutsche Folgeaufnahme in EN/RU.',
        '- Russische sichtbare Texte, Namen, Musikbeschriftungen und alle 1947 gesprochenen Einträge sind ohne lateinische Buchstaben. Interne stabile IDs und Quellen-/Lizenzdateien sind keine Lerninhalte.',
        '- Die zweite Runde ersetzt alle 320 Fragen. Neue native Wörter haben zwei Buchstabenlücken, freiwillige Boni drei oder vier. Rechtschreibung ist von Lautschrift zu unterscheiden.',
        '- 200 Sachfragen verwenden Kontextzeichnungen statt Kopien der richtigen Antwort. Kurze Hinweiswörter ergänzen die gesprochene Frage. Auswahlbilder und freigegebene Grundantworten bleiben erhalten.',
        '- Pro Grundaufgabe zwei unabhängig wählbare, überspringbare Herausforderungen mit 50/100 Punkten. Die Sachbonusfragen verwenden wiederkehrende Konzepte; 640 Bonusplätze bedeuten nicht 640 einzigartige redaktionelle Fragestellungen.', '',
        '## Offene Prüfung', '',
        '- Muttersprachler: Aussprache, natürliche Formulierungen, Silbenzählung und vollständige russische UI am Android-Gerät.',
        '- Fachpersonen: eindeutige Ablenker, Kontextbilder und höhere Schwierigkeit der Bonusaufgaben; Kinder mit unterschiedlichen Vorkenntnissen.',
        '- Hörprobe ohne eingeblendeten Text, danach im Spiel mit Musik. Technische Dauermessung und ASR sind keine Hörfreigabe.',
        '- Eine identische weibliche Stimme in allen Sprachen ist noch nicht erreicht. Die getestete Umwandlung verschlechterte deutsche Aussprache und wurde nicht ausgeliefert.', '',
        '## Änderungsprotokoll der Grundaufgaben', '',
        '| Aufgabe | Sprache | Feld | Vorher | Jetzt |', '|---|---|---|---|---|']
    for c in log['changes']:
        cells=[c['id'],c['locale'],c['field'],c['before'],c['after']]
        lines.append('| '+' | '.join(v.replace('|','\\|') for v in cells)+' |')
    return '\n'.join(lines)+'\n'
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=ROOT/'docs/localization-review.md';value=markdown()
    if a.check:
        if not path.exists() or path.read_text()!=value:raise SystemExit('Localization review is stale')
    else:path.write_text(value)
    print('Localization review: 320 base tasks + 640 bonuses, 3 locales; authored changes documented; human review OPEN')
if __name__=='__main__':main()
