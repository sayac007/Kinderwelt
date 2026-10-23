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

**Entwicklungsstand, noch keine vollständige neue Freigabe.** Die neue Gesamtprüfung und Android-Auslieferung werden nach Abschluss der DE-/RU-Vertonung eingetragen. Der zuvor vollständig verifizierte 0.9.1-Stand ist unten versionsfest verlinkt; seine Ergebnisse werden nicht auf neue Aufnahmen übertragen.

| Dimension | Neue Prüfung / verbleibende Grenze |
|---|---|
| Inhalte | 400 Grundaufgaben + 800 Boni, 50 je Fach und drei Sprachen. Bestehende 320 Grund- und 640 Bonus-IDs sowie Belohnungsrevision erhalten. Typisierte Inhalts-, Faktenmatrix-, Hinweis- und Duplikatprüfungen; keine unabhängige fachliche oder empirische Freigabe. |
| Wortaufgaben | Sichtbare Frage ohne Lösungswort, einfache `_`-Lücken, Kandidaten in ihren Wortpositionen. Gesprochener Wort-Hörhinweis separat. **99.756 Prüfungen über 1.800 echte Wortansichten** in vier Displayprofilen bestanden; 48er-Berührungsflächen und Abstand zu Steuerungselementen geprüft. |
| Punkte | Erweiterung auf 64.000 aktuelle Punkte, mit allen alten Belohnungen maximal 67.200. **1.231 Punkteprüfungen** bestanden. Neustart aus einem separaten Prozess stellt 3.470 Testpunkte einschließlich neuer Stationen wieder her, ohne doppelte Belohnung. |
| Audio | Wortregister: DE 1.490, EN 1.228, RU 1.743 unterschiedliche Wörter. Erzeugung neuer Banken läuft. Je 50 ganze Wortfragen in DE/EN unabhängig erkannt: 35/50 bzw. 25/50 Zielschreibweisen exakt wiedergewonnen (ohne Leerzeichen; zusammengesetzte Wörter, Eigennamen-/Schreibvarianten und mögliche Aussprachefehler offen). Eine niedrige Zeichenfehlerrate über die ganze wiederholte Frage darf diese Zielwortabweichungen nicht verdecken. Tatsächliche Syntheseeingaben werden geprüft. Akustische Betonung jedes Wortes bleibt mangels Lautschriftsteuerung und muttersprachlicher Hörfreigabe offen. |
| Darstellung / Android | **673 echte Renderbilder** in vier Displayprofilen bestanden; Wortansichten in DE/RU auch manuell angesehen. Android-Builds aus sauberem Commit stehen noch aus. Kein Release-Schlüssel; vorläufige Testpaketkennung bleibt. |

Neue Ergebnisse ersetzen diesen Entwicklungsstatus erst nach tatsächlichem Abschluss. Rohlogs bleiben in `qa-results/` und `build/`.

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
