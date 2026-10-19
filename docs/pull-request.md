Implementiert ausschließlich `02_logic_math.yaml` auf Basis des zusammengeführten Fundaments.

- Brückenwerkstatt: neun datenbasierte Level in drei Stufen, kombinierbare Stücke, alternative Lösungen, sichtbare Restlücken und reversible Entscheidungen.
- Marktstand: neun Level für Mengenabgleich, Vergleich, Sortieren und gleiches Verteilen mit sichtbaren Früchten im Bereich 1–10.
- Gemeinsame Levelwahl, Rückgängig, Wiederholung und Hilfefolge Zeigen → Teilschritt → abbrechbares Vormachen; lokale Fortschritte und transparente adaptive Vorschläge ohne Fehlerstrafen.
- Tatsächliche Fenstergröße und Fokus-Scrolling; synthetische Touch- und Tastaturtests, auch nach Größenwechsel.

Validierung mit Godot 4.7.2: Import, 33 Fundament-Regressionen, 507 Lernspiel-Prüfungen, 49 Eingabe-/Layoutprüfungen und Headless-Projektstart erfolgreich (589 Prüfungen). Alle 18 Level werden über Modelle und UI gelöst. Details: `docs/test-report.md`.

Keine physischen Geräte-, Hör-, Screenshot- oder Kind-Usability-Tests; keine Sprachausgabe oder behauptete Lernwirkung. Aufgaben 03–05 und alle YAML-Spezifikationen bleiben unverändert. Die drei übrigen Hub-Eingänge bleiben Fundament-Demos.

GitHub Actions ist ebenfalls erfolgreich: [Lauf 39313762029](https://github.com/sayac007/Kinderwelt/actions/runs/39313762029) auf Commit `1ed2822`, einschließlich der checksum-geprüften Installation und aller 589 Prüfungen.
