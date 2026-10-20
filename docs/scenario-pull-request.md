Die drei bisherigen Fundament-Demos für Sprache, Selbstständigkeit und soziales Lernen werden durch je sechs spielbare Szenarien ersetzt. Basis ist das aktuelle `main` einschließlich PR #2; Brückenwerkstatt und Marktstand bleiben erhalten.

- Bildergeschichte: sechs Bild-/Klanggeschichten mit 3–5 frei anordenbaren Karten, Replay, selbstbestimmtem Blättern und erlaubten Reihenfolgen in editierbaren Daten.
- Entdeckerwerkstatt: sechs reversible Versuche zu Kugelbahn, Licht, Wasser, Wind, Waage und Garten; mehrere passende Einstellungen, kein Zeitdruck.
- Gemeinsames Dorf: sechs Situationen mit zwei unterschiedlichen Bedürfnissen, bebilderten Ideen und sichtbaren Folgen. Keine Moralpunkte oder Beschämung; freiwillige Gesprächsimpulse blockieren das Spiel nicht.
- Gemeinsame Hinweise, lokale Abschlussmarkierungen ohne neue Rangstufen, zentrale deutsche Textschlüssel und dokumentierte Narrations-Slots. Keine Sprachausgabe oder externen Audio-/Netzwerkdienste.

Validierung mit Godot 4.7.2: **1.236 Prüfungen bestanden** (33 Fundament, 559 Logik/Mathematik, 59 bisherige Eingaben, 585 neue Szenarienprüfungen), außerdem Import und Headless-Start. Neue Tests schließen alle 18 Szenarien solo ab, enumerieren Experimentzustände und prüfen Hinweise, Rückgängig, Speicherung, optionale Elternansicht, Touch-Abschlüsse, Tastatur-Undo und Größenwechsel. Alle drei Module wurden zusätzlich auf virtuellem Display gerendert und beispielhafte Screenshots visuell geprüft.

Offen bleiben physische Geräte, Hörtest, komplette Tastaturnavigation und Verständlichkeit ohne Lesen mit Kindern. Details und Datenvertrag: `docs/scenario-test-report.md` und `docs/scenario-authoring.md`. Alle YAML-Dateien sowie Aufgaben 04 und 05 bleiben unverändert.
