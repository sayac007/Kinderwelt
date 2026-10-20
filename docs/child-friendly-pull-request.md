## Kinderwelt 0.2 — Child-Friendly Experience

Die auf dem Smartphone installierte 0.1 zeigte kleine Desktop-Pixel, abstrakte Symbole und dauerhaft platzraubende Elternhinweise. Diese Änderung führt ein helles gemeinsames Design, Android-Dichteskalierung, große illustrierte Auswahlkarten und beschriftete konsistente Spielaktionen in allen fünf Bereichen ein. Wasserweg/Obst/Brücken/Geschichten/Wünsche werden anschaulicher dargestellt; die 36 Aufgaben und reinen Spielmodelle bleiben erhalten.

Fünf tatsächlich erzeugte eigene Retro-WAV-Stücke sind integriert. Gemeinsamer Manager mit Überblendung, Hintergrundpause, vollständigen Loops, getrennten Musik-/Effektlautstärken und globalem Mute; lokale Einstellungen einschließlich Großschriftmodus bewahren bisherige Spielstände. Keine fremden Aufnahmen, Release-Schlüssel oder Play-Uploads.

## Tatsächliche Validierung

- Alle 1236 bestehenden Checks PASS; bestehende GUT-Qualität 6 Tests / 13001 Assertions und 144 Aufgaben-/Viewport-Fälle PASS. Bestehende Tests wurden nicht entfernt.
- Neue Experience-Suite 6 Tests / 22891 Assertions PASS, einschließlich Text, Layout, Kontrast, großer Schrift über alle Aufgaben, Musik, lokalen Einstellungen und optionalen Elternhinweisen.
- 19 Android-/Diagnose-/Musikasset-Python-Tests, 16 QA-Python-Tests sowie die GUT-Upstream-Auswahl 13 Tests / 62 Assertions PASS.
- 146 echte Screenshot-Frames aller 36 Aufgaben an zwei Größen und 44 repräsentative UI-Renderings an vier Profilen, darunter eine hochauflösende Dichtesimulation. Elf PNG-Beispiele im Repository.
- Neue Debug-APK **0.2.0 / Code 2** und unsigniertes AAB tatsächlich erzeugt; Manifest, Signaturen, 16-KB-Ausrichtung, Berechtigungen sowie alle Musik-Payloads geprüft. Lokaler Ordner `build/android-0.2-release-check/`. SHA256 und tatsächliche Belege in `docs/child-friendly-test-report.md` / `docs/child-friendly-evidence.json`.

## Offene Prüfungen

Kein tatsächlicher 0.2-Geräte-/Emulatortest, keine bestätigte Bedienbarkeit für Siebenjährige, keine nachgewiesene Lernwirkung. Geräte-DPI, Safe Areas, Rotation, Accessibility, Lautheit und Lifecycle/Performance sind anhand der beigefügten Checkliste zu prüfen. Godot meldet bei hartem Headless-Dummy-Audio-Exit zwei noch gehaltene Audioobjekte; nicht unterdrückt und dokumentiert. Die Musik ist ein hörbarer Retro-Prototyp, keine professionelle/orchestrale Produktion. Screenshotprüfungen sind reproduzierbare Layout-/Bildbelege, kein pixelidentischer Golden-Test. Der GitHub-Actions-Lauf bleibt mangels API-Zugriff unbestätigt.

Reproduzierbare Befehle, Musikherkunft, Architektur und kurze freiwillige Smartphone-Checkliste mit Kind sind dokumentiert. Sämtliche Google-Play-Freigaben bleiben offen.
