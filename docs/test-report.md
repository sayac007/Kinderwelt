# Testbericht · Logik und Mathematik (Aufgabe 02)

19.10.2026 · Linux x86_64 Cloud · Godot **4.7.2.stable.official.ed1daf0bf**.
Ausgangspunkt: `main`, Merge von Fundament-PR #1. Umsetzung auf
`feat/logic-math`. Aufgaben 03–05 und alle fünf YAML-Dateien bleiben unverändert.
Der ursprüngliche Fundamentbericht ist in `foundation-test-report.md` archiviert.

## Ausgeführt

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
```

| Schritt | Ergebnis |
| --- | --- |
| Godot-Headless-Editorimport | PASS, Exit 0, keine Skript-/Parse-Fehler |
| `tests/smoke.gd` | PASS, 33 Prüfungen, 0 Fehler |
| `tests/learning.gd` | PASS, 507 Prüfungen, 0 Fehler |
| `tests/input.gd` | PASS, 49 Prüfungen, 0 Fehler |
| Projektstart `--headless --quit-after 60` | PASS, Exit 0 |
| `git diff --check` | PASS |
| Statische Suche nach Laufzeit-Netzwerk-APIs in core/games/content/project.godot | Keine Treffer |
| GitHub Actions | Wird nach Push geprüft; Ergebnis hier noch nicht behauptet |

**589 Prüfungen bestanden.** Die bisherigen Modul-Tap-Assertions für Logik und
Mathematik wurden durch die umfassendere Lernspiel-Suite ersetzt. Die 33
Fundament-Regressionen prüfen weiterhin den Hub, die drei zurückgestellten Demos,
Speicherung/Reset, beschädigte Daten, Ton, Layout und Zurück-Navigation.
Es wurden keine bestehenden Framework-Tests ausgelassen: ein externes
Testframework ist in diesem Projekt nicht installiert.

### Lernspiel-Suite

Alle 18 Content-Level werden validiert, über die Modelle und separat über echte
UI-Button-Signale gelöst. Geprüft werden Schemafehler, doppelte IDs, unerreichbare
Mengen, mehrdeutige Vergleiche, ungültige Indizes, Abschluss, Rückgängig nach
Abschluss, Hilfestufen, gestenbasierter Hinweis ohne Zustandsänderung, partieller
Hinweis, vollständiges Beispiel, Wiederholung, gespeicherte Levelabschlüsse und
Hub-Rückkehr. Für jede legal platzierbare erste Brückenentscheidung wird außerdem
der Rückweg zur Lösung geprüft; alternative Aufteilungen einer Lücke und eine
konkrete Sackgasse mit Rückgängig sind enthalten.

Die Vorschlagslogik wird auf unterschiedliche unassistierte Erfolge, wiederholte
Aufgaben, assistierte Abschlüsse, Übergänge aller drei Stufen, getrennte Module,
Save/Reload und Erwachsenen-Reset geprüft. Dies belegt Softwareverhalten, keine
pädagogische Wirksamkeit oder reale Kompetenzmessung.

### Eingaben und Layout

Synthetische `InputEventScreenTouch`-Ereignisse gehen durch Godots Input-System:
Quelle auswählen und Ziel antippen in beiden Modulen, jeweils auch nach Wechsel
auf 360×800 und 1024×600. Dabei werden echte GUI-Ereignisse verarbeitet, nicht
manuell das `pressed`-Signal ausgelöst. Enter aktiviert Rückgängig über GUI-
Tastaturdispatch. Ein falscher Mengenvergleich bleibt korrigierbar. Die Tests
prüfen Fenster-/Viewportgröße, passende Mindestbreite, Spaltenwechsel und große
Hit-Targets. Ein laufendes Beispiel wird per Wiederholung und Hub abgebrochen;
alte Timer dürfen den neuen Level nicht verändern.

Das ist **kein physischer Touch-, Screenshot- oder Android-Test**. Es beweist
weder die Darstellung auf jedem Display noch die Verständlichkeit für Kinder.
Der Test-Runner verwendet temporäre XDG-Verzeichnisse statt echter Spielstände,
meldet Godot-Fehler auch bei Prozess-Exit 0 und begrenzt jeden Schritt auf 120 s.
Prozessfehler inklusive Timeout-Exitcode bleiben erhalten.

## Während der Implementierung gefundene und behobene Fehler

- GDScript konnte den Typ der dynamischen Hinweis-Flags nicht inferieren: explizite
  Bool-Typisierung; danach Module erfolgreich geladen.
- JSON lädt Stufen als Fließkommazahlen: eine zu strenge Integer-Mitgliedsprüfung
  setzte geladene Vorschläge zurück. Numerische Validierung/Normalisierung ergänzt;
  Reload-Test besteht.
- Ein Test verlangte bei Vergleichsaufgaben immer die dritte Hilfe, obwohl die
  einzelne Wahl schon durch Hilfe zwei abgeschlossen wird. Erwartung korrigiert;
  Hilfe drei wird weiterhin für alle mehrschrittigen Aufgaben geprüft.
- Der erste synthetische Touch-Test nutzte falsche Bildschirmkoordinaten. Die
  feste virtuelle Breite verhinderte außerdem echte Portrait-Anpassung. Test-
  Koordinaten werden nun mit dem Viewporttransform umgerechnet; Layout nutzt die
  tatsächliche Fenstergröße, inklusive geprüfter Eingaben nach Größenwechsel.

## Nicht ausgeführt / manuelle Abnahme

- Physische Telefon-/Tablet-Tests, echter Touch, Android-Zurück-Taste und Export.
- Sichtprüfung der Piktogramme, DPI/Schrift-Fallback, realer Hörtest und Screenreader.
- Begleitete Prüfung mit Kindern: Können sie Brückenlängen, Sortieren, Vergleichen,
  Verteilen und die dreistufige Hilfe ohne Lesen verstehen?
- Leistungs-/Lernwirkungsmessungen: keine Daten, keine behaupteten Resultate.

Manuell alle 18 Level bei Hoch-/Querformat spielen, Quelle und Ziel ohne Präzision
antippen, absichtlich falsch zuordnen, rückgängig machen und wiederholen. Ton aus
und reduzierte Bewegung einschalten, während Vormachen den Hub öffnen und erneut
starten. Sichtbare Früchte und Segmentumrisse müssen ohne Farberkennung reichen.
Für alle Aufgaben sind Erwachsene optional und kein Zeitlimit vorhanden.
