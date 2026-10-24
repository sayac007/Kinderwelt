# Aufgaben redigieren und reproduzieren

`games/quest/tasks.json` und `games/quest/languages.json` sind **generierte Ausgaben**, keine alleinigen Redaktionsquellen. Einstieg: `scripts/content/generate.py`.

1. `foundation-tasks.json`, die Fach-TSVs, `german-words.tsv` und `languages-source.json` bilden Ausgangsaufgaben und Begriffe.
2. `distractor-changes.json` enthält bewusst geprüfte Antwortoptionsänderungen; `science-answer-fixtures.json` sichert stabile Sachantworten. Kategorien sind eine Review-Hilfe, kein Generator beliebiger falscher Antworten.
3. `advanced.py` erneuert die Grundaufgaben mit `advanced-*.tsv` und `advanced-words.tsv`.
4. `experience.py` ergänzt native Sprachvarianten, Kontextbilder aus `riddle-cues.json` und Boni. Sachboni kompiliert `pedagogy.science_bonuses()` aus `science-properties.tsv` und den konkreten Modellen/Bezeichnungen in `science-models.json`. `reasoning-bank.tsv` bleibt eine ausdrücklich inaktive Altquelle.
5. `pedagogy.apply()` übernimmt die geprüften Grundaufgaben aus `pedagogy-base.tsv`, Denkhinweise und `science-hints.tsv`. `spoken-prompts.json` hält geprüfte, ausschließlich gesprochene Alternativen fest. Die Vergleichskategorien aus `answer-categories.json` sind ausschließlich eine QA-Hilfe mit begründeten Ausnahmen; sie erzeugen keine Antwortoptionen.
6. Der Generator vergibt stabile IDs/Antwortpositionen und aktualisiert die aktuellen Nachher-Texte im langfristigen Redaktionsnachweis `localization-changes.json`; ursprüngliche Vorher-Werte bleiben erhalten. `localization.py` und `distractors.py` reproduzieren kompakte Anleitungen; ihre ausführlichen Laufzeitbefunde landen in `qa-results/`.

```sh
python3 scripts/content/generate.py
python3 scripts/qa/localization.py --check
python3 scripts/qa/distractors.py --check
python3 scripts/qa/pedagogy.py --check
python3 -m unittest discover -s tests/android -v
```

Anschließend die vollständige Suite aus [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) ausführen. Änderungen müssen im Generator oder seinen Quellen stehen; ein zweiter Generatorlauf darf keinen weiteren Diff erzeugen. Anzahl, stabile IDs, eindeutige Antworten, Übersetzungen und freiwillige 50-/100-Punkte-Boni erhalten.

Sachboni prüfen drei beziehungsweise vier kurze Aussagen: Genau zwei beziehungsweise drei müssen für die gewählte Option stimmen. Jede falsche Option erfüllt mindestens eine Aussage, aber nicht die geforderte Anzahl. Die unabhängig von der Generierungslogik formulierten 30 redaktionellen Gegenbeispiele in `tests/fixtures/pedagogy/science-counterexamples.json` sichern wichtige fachliche Abgrenzungen ab; sie ersetzen keine externe Fachprüfung. Kappe und Wollmütze haben originale KI-Bildnachweise in `art/public/headgear.json`; neue Bild-IDs müssen Renderer, Lokalisierung und Android-Ressourcenprüfung erreichen. Die Faktenmatrix beschreibt ausdrücklich die genannten Unterrichtsmodelle, keine universellen Behauptungen. Jede Station verwendet einen eigenen Merkmalssatz; die deterministische Auswahl ersetzt kein fachliches Review der Quelldaten. `tests/qa/content_layout.gd` misst alle Überschriften in beiden Textgrößen und beiden Orientierungen mit der tatsächlich ausgelieferten Schrift.

## Sprache und Auslieferung

`narration_texts()` in `scripts/generate-quest-voice.py` bestimmt die gesprochenen Texte einschließlich Hinweisen. Nach Inhaltsänderungen jede Locale gegen `assets/voice/quest/<locale>/manifest.json` vergleichen. Geänderte Texte benötigen neue, mit der bestehenden Engine erzeugte Clips, passende Hashes und tatsächliche Decodier-/Wiedergabeprüfungen. Alte Aufnahmen dürfen nicht durch bloßes Umetikettieren als aktuell gelten. [Erzeugung und manuelle Hörprüfung](voice.md).

Qwen-Locales auf dieser 32-GiB-Umgebung nacheinander erzeugen. Der Textbatch ist standardmäßig 48, höchstens 64; der Waveform-Decoder verarbeitet unabhängig davon höchstens vier ähnlich lange Ausgaben zusammen. Größere Textbatches sind keine Erhöhung des festen RAM-Limits. Fertige Checkpoints können wiederverwendet werden. Mit `--ids` erzeugte Teilbanken niemals unmittelbar ausliefern; vor der Installation müssen alle aktuellen Text-/ID-Zuordnungen und tatsächlichen Dateihashes vollständig stimmen.

## Native Worträtsel

Je Sprache 50 eigene Wörter. Sichtbares `prompt` und `tip` enthalten das Lösungswort nicht; `spoken_prompt` nennt es als Hörhinweis. `display` nutzt `_` für fehlende Buchstaben; `missing_positions` und `option_displays` halten die Kandidaten an genau diesen Wortpositionen. Die Antwortwerte bleiben kompakte Buchstabenfolgen. Ein gemeinsamer Renderer zeichnet gleich breite Zellen, drei breite Antwortzeilen ersetzen die engen Kreise. `test_clear_literacy.py` kontrolliert Rekonstruktion und kyrillische RU-Zeichen; `tests/qa/letter_layout.gd` prüft alle 1.800 tatsächlichen Wortansichten in vier Displayprofilen.

## Pädagogisches Review

Alle 400 Grundaufgaben und 800 Boni in allen drei Sprachen berücksichtigen: Hinweise fördern einen Denkschritt, Optionsgruppen sind plausibel und fachlich eindeutig, alternierende Regeln sind tatsächlich verschieden, Bonuskonzepte wiederholen sich nicht stationsübergreifend. Formelhafte Rechenanweisungen mit unterschiedlichen Zahlen sind nicht automatisch Duplikate. Fachwörter kurz erklären, statt sie pauschal zu entfernen. Heuristiken und Schwierigkeitsindikatoren markieren Review-Bedarf; sie sind keine empirische Lern- oder Altersfreigabe.

Aktuelle Befunde, begründete Ausnahmen und Testergebnisse werden ausschließlich im [zentralen Überblick](QUALITY_ASSURANCE.md) gepflegt. Neue Rohberichte gehören nach `qa-results/`, nicht nach `docs/qa/`.
