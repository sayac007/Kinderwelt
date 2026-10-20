Implementiert ausschließlich `02_logic_math.yaml` auf Basis des zusammengeführten Fundaments.

- Brückenwerkstatt: neun datenbasierte Level in drei Stufen, kombinierbare Stücke, alternative Lösungen, sichtbare Restlücken und reversible Entscheidungen.
- Marktstand: neun Level für Mengenabgleich, Vergleich, Sortieren und gleiches Verteilen mit sichtbaren Früchten im Bereich 1–10.
- Gemeinsame Levelwahl, Rückgängig, Wiederholung und Hilfefolge Zeigen → Teilschritt → abbrechbares Vormachen; lokale Fortschritte und transparente adaptive Vorschläge ohne Fehlerstrafen.
- Tatsächliche Fenstergröße und Fokus-Scrolling; synthetische Touch- und Tastaturtests, auch nach Größenwechsel.

Validierung mit Godot 4.7.2: Import, 33 Fundament-Regressionen, 559 Lernspiel-Prüfungen, 59 Eingabe-/Layoutprüfungen und Headless-Projektstart erfolgreich (651 Prüfungen). Alle 18 Level werden über Modelle und UI gelöst. Details: `docs/test-report.md`.

Zusätzlich auf virtuellem X11-Display gerendert und Screenshots bei 900×700, 900×1000 und 360×800 visuell geprüft. Neutrale Mengenplätze für gemischte Verteilung und animierte Brückenüberquerung (mit Variante für reduzierte Bewegung) ergänzt. Keine physischen Geräte-, Hör- oder Kind-Usability-Tests; keine Sprachausgabe oder behauptete Lernwirkung. Aufgaben 03–05 und alle YAML-Spezifikationen bleiben unverändert. Die drei übrigen Hub-Eingänge bleiben Fundament-Demos.

Historischer GitHub-Actions-Nachweis: [Lauf 39313762029](https://github.com/sayac007/Kinderwelt/actions/runs/39313762029) auf Commit `1ed2822`, einschließlich der checksum-geprüften Installation und der damaligen 589 Prüfungen. Das Remote-CI-Ergebnis des aktuellen Pushs ist noch nicht bestätigt.
