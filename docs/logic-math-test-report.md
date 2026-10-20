# Testbericht · Logik und Mathematik (Aufgabe 02)

Aktuell erneut geprüft: 20.10.2026 · Linux x86_64 Cloud · Godot **4.7.2.stable.official.ed1daf0bf**.
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
| `tests/learning.gd` | PASS, 559 Prüfungen, 0 Fehler |
| `tests/input.gd` | PASS, 59 Prüfungen, 0 Fehler |
| Projektstart `--headless --quit-after 60` | PASS, Exit 0 |
| `git diff --check` | PASS |
| Statische Suche nach Laufzeit-Netzwerk-APIs in core/games/content/project.godot | Keine Treffer |
| GitHub Actions (historischer Stand) | PASS: [Lauf 39313762029](https://github.com/sayac007/Kinderwelt/actions/runs/39313762029), Commit `1ed2822`; Installation, Import, die damaligen 589 Prüfungen und Start erfolgreich; neuer Push noch nicht bestätigt |

**651 Prüfungen im aktuellen lokalen Lauf bestanden (Exit 0).** Die bisherigen Modul-Tap-Assertions für Logik und
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

Das ist **kein physischer Touch- oder Android-Test**. Es beweist
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
- Physische DPI/Schrift-Fallback, realer Hörtest und Screenreader.
- Begleitete Prüfung mit Kindern: Können sie Brückenlängen, Sortieren, Vergleichen,
  Verteilen und die dreistufige Hilfe ohne Lesen verstehen?
- Leistungs-/Lernwirkungsmessungen: keine Daten, keine behaupteten Resultate.

Manuell alle 18 Level bei Hoch-/Querformat spielen, Quelle und Ziel ohne Präzision
antippen, absichtlich falsch zuordnen, rückgängig machen und wiederholen. Ton aus
und reduzierte Bewegung einschalten, während Vormachen den Hub öffnen und erneut
starten. Sichtbare Früchte und Segmentumrisse müssen ohne Farberkennung reichen.
Für alle Aufgaben sind Erwachsene optional und kein Zeitlimit vorhanden.

## Ergänzende Prüfung und Konsolidierung am 20.10.2026

Der erste Push wurde abgewiesen, weil `feat/logic-math` bereits die Umsetzung
`1ed2822` und den Bericht-Commit `5bfce74` enthielt. Diese Arbeit wurde erhalten
und als gemeinsame Basis verwendet. Die lokal parallel entstandene alternative
Implementierung wurde in einem lokalen Backup-Branch gesichert und nicht über
bestehende Remote-Arbeit geschrieben. Der unveränderte Remote-Stand bestand bei
der erneuten lokalen Ausführung alle 589 Prüfungen.

Die Ergänzung auf dieser Basis erweitert die Tests um unabhängige Endzustands-
Prüfungen der Brückenlängen, Fruchtformen und Zielmengen, vollständige Abschlüsse
beider Spiele über synthetische Touch-Ereignisse sowie Retry nach diesen
Abschlüssen. Die Figur überquert eine fertiggestellte Brücke jetzt sichtbar;
reduzierte Bewegung zeigt sofort den Endzustand. Beide Varianten sind getestet.
Beim Teilen gemischter Früchte zeigen freie Plätze neutrale Kreise. Die zuvor
verwendeten Apfelumrisse konnten fälschlich eine Sortenvorgabe nahelegen.

Aktueller Runner: **33 Fundament-, 559 Lernspiel- und 59 Eingabe-/Layoutprüfungen**,
Import und Headless-Start bestanden, keine Skript-/Parse-Fehler.
Zusätzlich wurden Brücken und gemischte Verteilung auf einem virtuellen X11-
Display mit Mesa llvmpipe/OpenGL gerendert und die Screenshots bei 900×700,
900×1000 und 360×800 visuell geprüft. Eine V-Sync-Warnung des virtuellen Treibers
betrifft die fehlende Umschaltbarkeit; keine Rendering-/Skriptfehler beobachtet.
Audio lief dort über den Dummy-Treiber, ein Hörtest fand nicht statt.

Der API-Versuch zur PR-Erstellung meldete erneut
`Post https://api.github.com/graphql: Forbidden`. Deshalb ist keine neue
PR-Erstellung durch diesen Versuch bestätigt. Manueller Erstellungslink:
https://github.com/sayac007/Kinderwelt/compare/main...feat/logic-math?expand=1

Die 651 aktuellen Prüfungen gehören zum konsolidierten Branch. Die zuvor lokal
bestandenen 684 Prüfungen der alternativen Implementierung gelten ausdrücklich
nicht als Prüfergebnis des gepushten Codes. Echte Geräte- und Kind-Usability-
Prüfungen aus der obigen Liste bleiben offen.
