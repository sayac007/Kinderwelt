# Kinderwelt: Qualität und Prüfstand

**Klasse 1–2:** Ein vollständig lokal spielbares Godot-Lernabenteuer mit 400 Grundaufgaben und 800 freiwilligen Boni. Kinder bewegen eine Figur durch sieben wählbare Kulissen und sammeln dauerhaft gespeicherte Punkte. Keine Konten, Werbung, Käufe, Mikrofonaufnahmen oder Telemetrie. Technische Prüfergebnisse sind kein Nachweis pädagogischer Wirksamkeit oder einer Google-Play-Freigabe.

## Orientierung

| Bereich | Inhalt / zuständige Komponenten |
|---|---|
| Lernen | Je **50 Stationen** in Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch und Geografie; jeweils DE/EN/RU. Sprache mit eigenem nativem Wortschatz. Jede Station: 10 Punkte und zwei freiwillige Boni mit 50/100 Punkten. |
| App | `core/quest/main.tscn`, `core/quest/` und `games/quest/`: Oberfläche, Weltbewegung, Aufgaben, Audio und lokaler Spielstand. Sieben Figuren, fünf Looks, sieben Kulissen und 20 klassische Klavierwiedergaben. |
| Redaktion | `scripts/content/generate.py` kompiliert TSV-/JSON-Quellen mit `advanced.py`, `experience.py` und `pedagogy.py`. [Quellen, Regeln und Ablauf](CONTENT_AUTHORING.md). |
| Sprache | Fertige lokale Vorbisclips: weibliche Serena DE/RU und LJSpeech EN. Vollständiges Wortregister, kontextabhängige Betonungsreferenzen, Syntheseprovenienz und unabhängige ASR-Stichproben. [Verfahren und Hörgrenzen](voice.md). |
| Medien / Android | [Musik](music.md), [Bildherkunft](character-origins.md), [Build und Paketprüfung](android.md). Familien- und neutrale Variante mit gleicher Spiellogik; private Figuren separat. |

## Ausführen

Dieselben Befehle wie im [README](../README.md); Godot 4.7.2, Python 3 und FFmpeg erforderlich:

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Für neue Bildprüfungen ein neues Ausgabeverzeichnis wählen. CI führt beide Suiten aus. Laufzeitberichte stehen unter `qa-results/`, Pakete unter `build/`; CI-Artefakte laufen nach sieben Tagen ab. Normale Tests benötigen keine privaten Familien-Assets, Tokens oder Sprachmodelle.

## Aktueller Prüfstand — 0.9.2

**23.10.2026. Verifizierte Anwendungsressourcen: `74a50c8d4599257949235a94ac789ac9a3deff27`; QA-Hörprobentool: `a097e386` bei unveränderten Anwendungsressourcen.** Die folgenden Prüfungen wurden lokal tatsächlich ausgeführt. Die Android-Pakete bestätigen den sauberen Anwendungscommit (`source_dirty: false`, keine Änderung während des Builds). Nachfolgende Dokumentationsänderungen betreffen die App nicht. GitHub baut separat; dessen Status, Prüfnachweise und Downloads stehen im jeweiligen [Actionslauf](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml).

| Dimension | Tatsächlich verifiziert / verbleibende Grenze |
|---|---|
| Automatisierung / Inhalte | **124 Python-Tests bestanden**; 12.000 Aufgaben-, 4.168 Welten- und 1.231 Punkteprüfungen bestanden. 400 Grundaufgaben + 800 Boni, je 50 Stationen pro Fach in DE/EN/RU; bestehende 320 Grund- und 640 Bonus-IDs und Belohnungsrevision erhalten. Generator reproduziert alle Inhaltsdateien ohne Diff. Fach-/Schwierigkeitsreview bleibt offen. |
| Wortaufgaben / Darstellung | Sichtbare Frage ohne Lösungswort; `_`-Lücken und positionsgetreue Buchstabenkandidaten. **99.756 Prüfungen über 1.800 echte Wortansichten**, 14.400 Schriftmessungen ohne Überlauf und **673 echte Renderbilder** in vier Displayprofilen bestanden. Große Schrift, Hoch-/Querformat, 48er-Berührungsflächen und Abstand zu Steuerungselementen geprüft. Einzelne Wortansichten DE/RU manuell angesehen; kein vollständiger manueller Geräte-/Bildtest. |
| Punkte / Start | 64.000 aktuelle Punkte, mit allen alten Belohnungen maximal 67.200. Separater Neustart stellt **3.470 Testpunkte** einschließlich neuer Stationen wieder her, ohne doppelte Belohnung. Frischer Import aus ausschließlich ausgelieferten Dateien sowie zusätzlicher Familienstart über 60 echte Frames mit Produktions-Audioshutdown bestanden. |
| Audio / Technik | **Alle 3.803 tatsächlichen Ogg-Dateien decodiert**, 7.281 aktuelle Text-/ID-Bindungen und Dateihashes geprüft; 36 Wiedergabe-, 75 Sequenz- und 38 Weltsprachprüfungen bestanden. Modellkarten, Lizenzen, vollständige Wellenformen, Ränder, Dauer und Pegel geprüft. Weibliche Serena DE/RU und LJSpeech EN bleiben erhalten. Unveränderte, besser erkannte Aufnahmen werden mit ihren ursprünglichen Erzeugungsdaten beibehalten; geänderte Eingänge neu erzeugt. |
| Betonung / Erkennung | Vollständiges ausgeschriebenes Vokabular: DE 1.490, EN 1.228, RU 1.743 unterschiedliche Wörter mit Referenzen; tatsächliche Syntheseeingaben nachgewiesen. Russische Kasusfälle unterscheiden etwa ру́ки/руки́, но́ги/четыре ноги́ und берега́/два бе́рега. **24 Fächeransagen und neun Aufgabenbeispiele** mit tatsächlichen Audiohashes abgesichert. Bei 50 nativen Wortfragen pro Sprache gewinnt ASR **35/50 DE, 31/50 EN, 42/50 RU** Zielschreibweisen exakt zurück; auch Abweichungen bleiben sichtbar. Zusammengesetzte Wörter, reduzierte Vokale, Kasus-/Schreibvarianten und mögliche Ausspracheprobleme bleiben zu hören. ASR-gestützte Auswahl ist kein unabhängiger nachträglicher Verständlichkeitstest und bestätigt keine Silbenbetonung. Interne Zahlwortverbalisation und vollständige muttersprachliche Hörfreigabe bleiben offen. |
| Android | **Beide APKs und beide unsignierten AABs erzeugt und technisch bestanden**, 0.9.2 / Code 15. Paketkennung, Konfiguration, API 24–36, zwei ABIs, ZIP-/ELF-Ausrichtung, Launcherbilder und Ressourcenintegrität geprüft: Familie 7.797, neutral 7.787 Ressourcen je Paket. APKs mit bestehendem Entwicklungsschlüssel (v2); **AABs unsigniert**, keine Release-/Play-Freigabe. Vorläufige Paketkennungen und stabiler Testkanal bleiben erhalten. |
| Datenschutz / Herkunft | Bestehender begrenzter Quell-/Konfigurationsaudit bestanden: keine Konten-/Netzwerk-/Werbeintegration, keine Android-Berechtigungen, Backup deaktiviert. Medien-/Modellherkunft und 20 Musik-Lizenzhinweise geprüft. Private Familienquellen und Android-Workflow unverändert; keine personenbezogenen Testdaten erhoben. Keine umfassende Sicherheits-/Rechtszertifizierung. |
| Dokumentation | **81 lokale Dokumentationsziele, 13 CI-Dateireferenzen und alle 139 Remote-Archivdateien** geprüft. `docs/qa/` weiterhin zwei Referenzdateien / 78.669 Bytes. Externe allgemeine HTTP-Erreichbarkeit wird nicht pauschal zertifiziert. |

Lokale Nachweise: `qa-results/fifty-full-suite.log`, `qa-results/fifty-python-final.log`, `qa-results/visual-v092-final/`, `qa-results/fifty-documentation-final.log` und `build/android-v092-fifty/delivery.json` samt beiden Variantenverzeichnissen mit Provenienz und Verifikation. Die notwendige [Erkennungsreferenz](../tests/fixtures/voice/subject-recognition.json) bewahrt tatsächlich gemessene Transkripte und Hashes dauerhaft, einschließlich der offenen Fälle. Neue Rohlogs wurden nicht ins Git aufgenommen.

Die Offline-Hörseite `build/android-v092-fifty/kinderwelt-listening.html` enthält **262 tatsächliche Hörfolgen**, darunter alle 50 Lernwörter je Sprache und kurze russische Kasus-/Betonungsbeispiele. Sie enthält keine Aufnahme- oder Übertragungsfunktion und liegt auch dem Android-Actions-Artefakt bei. Die Hörprobenseite behandelt `FUSSABDRUCK` und gesprochenes **Fußabdruck** mit derselben Normalisierung wie der Aufgabengenerator; ein vollständiger Erzeugungstest sichert alle 50 Wörter je Sprache ab.

Lokale Paketdateien unter `build/android-v092-fifty/` (GitHub-Builds haben eigene Nachweise und können andere Archivhashes besitzen):

| Datei | Bytes | SHA-256 |
|---|---:|---|
| `kinderwelt-debug-family.apk` | 321.911.510 | `95151aefac922c4f13b1f644eab6ad7661d193ec8904342139ad6f2fe7345a42` |
| `kinderwelt-debug-neutral.apk` | 317.040.567 | `4ee6f53d99b52afe8f0ba2d17c813c52dd9d0409b1cde64dfa9c79b0a565858c` |
| `kinderwelt-unsigned-family.aab` | 307.995.219 | `d3d2a4364c8a2eeadeea0402de1df6bf34bfb80806a6c960b132555bb2da74cb` |
| `kinderwelt-unsigned-neutral.aab` | 303.131.828 | `90e1de93b564d03308142c79d73aef2edfadd45bf90e74ca0bb37beed155072a` |

## Qualitätsdimensionen und Regeln

- **Inhalte:** stabile IDs, eindeutige Antworten, plausible Ablenker, Hinweise ohne Endlösung, zwei verschiedene Schritte bei alternierenden Regeln, native Alphabete und überprüfbare Vergleichsmerkmale. Bewusst eingebaute Fehler und zulässige Gegenbeispiele sind Regressionstests. Rechenschablonen mit verschiedenen Zahlen sind keine automatischen Duplikate.
- **Sprache:** aktuelle Text-/ID-Bindungen, Hashes und Modellkarten; jede Ogg-Datei tatsächlich decodieren, Ränder/Dauer/Pegel prüfen. Godot-Tests kontrollieren vollständige Sprechfolgen, Navigation, Musikabsenkung und Unterbrechung. Wörterbuch-/Phonemvorgaben und ASR sind keine menschliche Hörfreigabe.
- **Bedienbarkeit:** tatsächliche Schriftmessung bei normaler/großer Schrift, Hoch-/Querformat, 320×568 und dichteren Displays; echte Touch-Ereignisse, Punkteabstände, Rotation und lokale Neustarts. Bildprüfungen ersetzen keine Geräte- und Kinderbeobachtung.
- **Android:** isolierter Export, Quellenprovenienz, Ressourceninventar, ZIP-/ELF-Ausrichtung, Paketkennung, Version, API, ABIs und Signaturstatus. APK nur mit bestehendem Entwicklungsschlüssel; AAB unsigniert. Keine Google-Play-Uploadfreigabe.
- **Datenschutz / Herkunft:** begrenzter Quell-/Konfigurationsaudit auf Netzwerk, Berechtigungen und personenbezogene Datenerhebung, geprüfte Medienherkunft und Lizenzhinweise. Keine umfassende Sicherheits-/Rechtszertifizierung.

## Bekannte Grenzen und manuelle Freigaben

Zwei bestehende Helm-Bildlücken (`physics_09`, `body_16`); muttersprachliches Hören aller neuen Clips mit Schwerpunkt auf Wortbetonung, Verneinungen und Zahlen; unabhängiges Fachreview der Unterrichtsmodelle und Schwierigkeitsangemessenheit; Geräte-, Drehungs-, Unterbrechungs- und Update-/Spielstandprüfungen. Die Faktenmatrix gilt für die konkret genannten Beispiele, nicht für jede Tierart oder jedes Material. Mehr Merkmale/Rechenschritte sind Schwierigkeitsindikatoren und beweisen keinen Lerngewinn.

Für Untersuchungen mit Kindern sind Testprotokoll, Einwilligung und Datenschutzentscheidung vor personenbezogener Datenerhebung erforderlich. Aktuell werden keine Kinderaufnahmen oder Telemetriedaten erhoben. Empirische Lernwirkungen sind nicht nachgewiesen.

## Historische Nachweise und Dokumentationsregeln

Der [verifizierte 0.9.1-Überblick mit KW-QA-01-Korrekturen](https://github.com/sayac007/Kinderwelt/blob/ebf226b55564ffb1f27ad7006b0f57ce6b4f562b/docs/QUALITY_ASSURANCE.md) enthält den früheren vollständigen Prüfstand einschließlich Commit `2f179ce6615e0bb7130e1bad4815fd1bf882ddff`, 106 Python-Tests, 605 Renderbildern und tatsächlichem Familien-APK-/AAB-Nachweis. Diese Angaben sind historisch.

[Archiv und Inventar](qa/README.md): **139 unveränderte Originaldateien / 7.383.943 Bytes** sind im geprüften, versionierten Git-Archiv unter Tag `qa-evidence/2026-10-23-v091`, Commit `a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`, dauerhaft erhalten. `docs/qa/` behält zwei notwendige Referenzdateien / 78.669 Bytes. Keine Historie oder privaten Assets entfernt/veröffentlicht.

Im Git nur aktuelle Übersicht, Anleitungen, bekannte Grenzen und notwendige langfristige Referenzen pflegen. **Keine neuen Einzelberichte je Testlauf.** Neue Logs/JSONs gehören nach `qa-results/` oder `build/`. Dauerhafte Freigaben benötigen eine verifizierte Ablage mit Commit, Datum, Dateinamen und Hashes. Originale erst nach verifizierter Ersatzablage entfernen. `documentation.py` prüft lokale Links, Archivindex und CI-Dateireferenzen; externe HTTP-Erreichbarkeit wird getrennt ausgewiesen. README und Überblick müssen dieselben Testkommandos nennen.
