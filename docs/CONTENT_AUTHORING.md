# Aufgaben redigieren und reproduzieren

`games/quest/tasks.json` und `games/quest/languages.json` sind **generierte Ausgaben**, keine alleinigen Redaktionsquellen. Einstieg: `scripts/content/generate.py`.

1. `foundation-tasks.json`, die Fach-TSVs, `german-words.tsv` und `languages-source.json` bilden Ausgangsaufgaben und Begriffe.
2. `distractor-changes.json` enthält bewusst geprüfte Antwortoptionsänderungen; `science-answer-fixtures.json` sichert stabile Sachantworten. Kategorien sind eine Review-Hilfe, kein Generator beliebiger falscher Antworten.
3. `advanced.py` erneuert die Grundaufgaben mit `advanced-*.tsv` und `advanced-words.tsv`.
4. `experience.py` ergänzt native Sprachvarianten, Kontextbilder aus `riddle-cues.json` und Boni; `reasoning-bank.tsv` ist die bisherige Sachbonusquelle.
5. Der Generator vergibt stabile IDs/Antwortpositionen und erzeugt außerdem das nachvollziehbare `localization-changes.json`. `localization.py` und `distractors.py` reproduzieren die zugehörigen Review-Dokumente.

```sh
python3 scripts/content/generate.py
python3 scripts/qa/localization.py --check
python3 scripts/qa/distractors.py --check
python3 -m unittest discover -s tests/android -v
```

Anschließend die vollständige Suite aus [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) ausführen. Änderungen müssen im Generator oder seinen Quellen stehen; ein zweiter Generatorlauf darf keinen weiteren Diff erzeugen. Anzahl, stabile IDs, eindeutige Antworten, Übersetzungen und freiwillige 50-/100-Punkte-Boni erhalten.

## Sprache und Auslieferung

`narration_texts()` in `scripts/generate-quest-voice.py` bestimmt die gesprochenen Texte einschließlich Hinweisen. Nach Inhaltsänderungen jede Locale gegen `assets/voice/quest/<locale>/manifest.json` vergleichen. Geänderte Texte benötigen neue, mit der bestehenden Engine erzeugte Clips, passende Hashes und tatsächliche Decodier-/Wiedergabeprüfungen. Alte Aufnahmen dürfen nicht durch bloßes Umetikettieren als aktuell gelten. [Erzeugung und manuelle Hörprüfung](voice.md).

## Pädagogisches Review

Alle 320 Grundaufgaben und 640 Boni in allen drei Sprachen berücksichtigen: Hinweise fördern einen Denkschritt, Optionsgruppen sind plausibel und fachlich eindeutig, alternierende Regeln sind tatsächlich verschieden, Bonuskonzepte wiederholen sich nicht stationsübergreifend. Formelhafte Rechenanweisungen mit unterschiedlichen Zahlen sind nicht automatisch Duplikate. Fachwörter kurz erklären, statt sie pauschal zu entfernen. Heuristiken und Schwierigkeitsindikatoren markieren Review-Bedarf; sie sind keine empirische Lern- oder Altersfreigabe.

Aktuelle Befunde, begründete Ausnahmen und Testergebnisse werden ausschließlich im [zentralen Überblick](QUALITY_ASSURANCE.md) gepflegt. Neue Rohberichte gehören nach `qa-results/`, nicht nach `docs/qa/`.
