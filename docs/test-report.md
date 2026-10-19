# Testbericht · Fundament

Stand: 19.10.2026. Linux x86_64 Cloud-Umgebung. Nur Aufgabe 01 umgesetzt.
Vorher waren keine Tests, kein Godot-Projekt und keine CI vorhanden.

| Prüfung | Ergebnis |
| --- | --- |
| Offizieller Latest-Release-Redirect | 4.7.2-stable |
| `bash scripts/install-godot.sh` | PASS; SHA-512 der offiziellen Release-Liste stimmt, wiederholbar installiert |
| Godot-Version | 4.7.2.stable.official.ed1daf0bf |
| `GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh` | PASS; alle drei folgenden Schritte Exit 0 |
| Headless Editor-Import | PASS, ohne ERROR-/Parse-Fehler |
| `--headless --path . --script tests/smoke.gd` | PASS: 47 Prüfungen, 0 Fehler |
| `--headless --path . --quit-after 60` | PASS, Projektstart ohne Fehler |
| `git diff --check` | PASS |
| Laufzeit-Netzwerk-API-Suche in core/games/content/project.godot | Keine Treffer für HTTPRequest, HTTPClient, WebSocket, ENet, JavaScriptBridge, OS.execute oder HTTP-URLs |
| GitHub Actions | Konfiguriert; Remote-Ausführung nicht bestätigt |
| Visuelle Darstellung, tatsächliche Touch- und Tastatureingaben | NICHT AUSGEFÜHRT; kein Display/physisches Gerät verfügbar |
| Hörtest, Kind-Usability und Verständlichkeit ohne Lesen | NICHT AUSGEFÜHRT |
| Android-Export, Installation, Berechtigungen auf Gerät | NICHT AUSGEFÜHRT; Aufgabe 05 zurückgestellt |

Die 47 Assertions prüfen fünf registrierte Hub-Buttons; für jede Demo valide
Leveldaten, Start, Hinweisfokus, Abschluss über Button-Signal, idempotenten
Abschluss, Wiederholung und Hub-Rückkehr; außerdem Save/Load aller fünf Module,
ein-/zweispaltigen Hub bei 360×800 und 1024×600, Reset-Bestätigung, persistierten
Reset, beschädigtes JSON, unbekanntes Schema, Stummschaltung und Escape-Rückkehr.
Dies sind native Godot-Integrationstests ohne zusätzliches Testframework.
Signalaufrufe und Layoutzustandsprüfungen sind keine echten Touch-/Bildtests.
Der Runner isoliert Benutzerdaten und wertet zusätzlich zum Exitcode Godot-Fehler
im Log aus, da Godot Skriptfehler nicht immer als Prozessfehler meldet.

Initiale Einrichtungsfehler: Sandbox verhinderte Schreiben nach ~/.local,
~/.config und ~/.cache. Behoben mit beschreibbaren XDG-Verzeichnissen.
Ein früherer Testlauf meldete einen JSON-Parse-Fehler trotz 45 bestandenen
Assertions; Save-Parser fängt beschädigte Daten jetzt geräuschlos ab.
Audio-Ressourcenwarnungen durch schnelles Ersetzen von Streams wurden durch
Stoppen vor Streamwechsel und vor Freigabe behoben. Finaler Lauf: keine dieser
Fehler oder Ressourcenwarnungen. Vorläufige 4.6.3-Tests gelten nicht als finaler
Versionsnachweis; die finale Suite lief vollständig auf 4.7.2.

## Manuelle Abnahme noch offen

- Auf kleinem Telefon und Tablet Hoch-/Querformat wechseln; kein abgeschnittener Eingang.
- Alle fünf Bilder mit Touch starten; Hinweise, Wiederholung und Haus ohne Lesen nutzen.
- Mit Tab/Pfeiltasten und Enter/Leertaste navigieren; Fokus sichtbar und erreichbar.
- Ton anhören, stummschalten, erneut starten; reduzierte Bewegung überprüfen.
- Zurück-Taste auf Android prüfen; Abbruch des Resets erhält den Spielstand.
- Begleitete Beobachtung: Wird das Tippen und der Abschluss ohne Erklärung verstanden?

Es gibt keine behaupteten Lernwirkungen oder gemessenen Geräteleistungswerte.
