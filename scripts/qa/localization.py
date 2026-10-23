#!/usr/bin/env python3
"""Render the localization review; structural guards cannot certify semantics."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def markdown():
    return '# Sprache und Lokalisierung prüfen\n\nAktueller Status und Einschränkungen: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Alle 400 Grundaufgaben und 800 Boni haben DE-/EN-/RU-Fassungen. Native Sprachaufgaben verwenden die jeweilige Sprache; russische Lerntexte bleiben kyrillisch.\n\nHinweise nennen keine vollständigen Antworten oder fehlenden Buchstabenlisten. Neue Fachwörter werden im Kontext erläutert; „Hebel“ wird mit der vertrauten Wippe verknüpft, der Drehpunkt als Stelle der Bewegung erklärt. Das lange deutsche Lernwort „Schildkrötenei“ ist durch das geläufigere „Entenei“ ersetzt. Die ursprünglichen Werte und aktuellen Grundtexte sind als langfristige Redaktionsreferenz in `scripts/content/localization-changes.json` nachvollziehbar, nicht als neuer Bericht pro Testlauf.\n\nDeutsch und Russisch nutzen dieselbe weibliche Serena-Modellstimme, Englisch LJSpeech. Keine identische Stimmidentität aller drei Sprachen behauptet. Geänderte Textfelder müssen mit den tatsächlich gelieferten Audio-Manifesten und Hashes übereinstimmen. [Audioverfahren und Hörfreigabe](voice.md).\n\n```sh\npython3 scripts/content/generate.py\npython3 scripts/qa/localization.py --check\n```\n\nMuttersprachliche Hör-/Textfreigabe, natürliches Sprachgefühl und kindliches Verstehen bleiben manuell zu prüfen. Technische Zeichen-/Dauerprüfungen und ASR belegen keine Lernwirkung.\n'

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=ROOT/'docs/localization-review.md';value=markdown()
    if a.check:
        if not path.exists() or path.read_text()!=value:raise SystemExit('Localization review is stale')
    else:path.write_text(value)
    print('Localization review: 400 base tasks + 800 bonuses, 3 locales; authored changes documented; human review OPEN')
if __name__=='__main__':main()
