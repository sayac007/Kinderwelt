# Kinderwelt: Qualität und Prüfstand

**Klasse 1–2:** Ein lokal spielbares Godot-Lernabenteuer mit 400 Grundaufgaben und 800 freiwilligen Boni. Kinder bewegen eine Figur durch sieben wählbare Kulissen und sammeln dauerhaft gespeicherte Punkte. Keine Konten, Werbung, Käufe, Mikrofonaufnahmen oder Telemetrie integriert. Technische Prüfergebnisse sind kein Nachweis pädagogischer Wirksamkeit oder einer Google-Play-Freigabe.

## Orientierung

| Bereich | Inhalt / zuständige Komponenten |
|---|---|
| Lernen | Je **50 Stationen** in Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch und Geografie; DE/EN/RU mit eigenem nativem Sprachwortschatz. Jede Station: zehn Punkte und freiwillige Boni mit 50/100 Punkten. |
| App | `core/quest/main.tscn`, `core/quest/` und `games/quest/`: Oberfläche, Weltbewegung, Aufgaben, Audio und lokaler Spielstand. Sieben Figuren, fünf Looks, sieben Kulissen, 20 klassische Klavierwiedergaben. |
| Redaktion | `scripts/content/generate.py` kompiliert TSV-/JSON-Quellen mit `advanced.py`, `experience.py` und `pedagogy.py`. [Quellen, Regeln und Ablauf](CONTENT_AUTHORING.md). |
| Sprache | Fertige Vorbisclips: weibliche Serena DE/RU und LJSpeech EN. Lexikalische Betonungsreferenzen, Syntheseprovenienz und ASR-Regressionsdaten. [Verfahren und Hörgrenzen](voice.md). |
| Medien / Android | [Musik](music.md), [Figurenherkunft](character-origins.md), [Build und Paketprüfung](android.md). Familien- und neutrale Variante mit gleicher Spiellogik; private Figuren separat. |
| Menschliche Abnahme | [Hörpaket, Geräteprotokolle, Fachprüfung und Evaluation](ACCEPTANCE.md). [Offene Play-Entscheidungen und Entwürfe](PLAY_READINESS.md). |

## Ausführen

Dieselben Befehle wie im [README](../README.md); Godot 4.7.2, Python 3 und FFmpeg erforderlich:

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Für Bildprüfungen ein neues Ausgabeverzeichnis wählen. CI führt beide Suiten aus und erzeugt separat `kinderwelt-full-listening-review`. Laufzeitberichte liegen unter `qa-results/`, Pakete unter `build/`; CI-Artefakte laufen nach sieben Tagen ab. Tests und Hörpaket benötigen keine privaten Familien-Assets, Tokens oder Sprachmodelle.

## Aktueller Prüfstand — 0.9.3 / Code 16

**24.10.2026. Verifizierter Anwendungscommit: `bace67364a334a592c8fe74f4953f1c5074027ca`.** Die lokalen Android-Builds bestätigen diesen sauberen Commit (`source_dirty: false`). Spätere Änderungen dieses Überblicks betreffen die Anwendung nicht. GitHub baut separat; Status und Downloads im jeweiligen [Actionslauf](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml). Ein lokaler Erfolg beweist keinen erfolgreichen Remote-Lauf.

| Dimension | Tatsächlich verifiziert / verbleibende Grenze |
|---|---|
| Vollständige Suite | **135 Python-Tests bestanden**; die vollständige `tests/run.sh`-Suite wurde nach der Fixturekorrektur nochmals erfolgreich ausgeführt. 12.750 Aufgaben-, 4.168 Welten- und 1.231 Punkteprüfungen bestanden. Generator reproduziert Inhaltsdateien ohne Diff. Alle 1.200 Aufgaben-IDs, richtigen Antwortwerte und Belohnungen gegenüber `main` erhalten. |
| Inhaltskorrekturen | Beide Helm-Bildlücken geschlossen: Fahrradhelm versus original KI-generierte Kappe/Wollmütze; sichtbare echte Bilder und lokalisierte Namen. Herkunft/Hashes in `art/public/headgear.json`. 30 separat formulierte Sachgegenbeispiele sichern u.a. Achsen, Pilze, Puppenstadien, Stoffeigenschaften und Organe ab. Kategorienprüfung meldet keine offenen Bildwarnungen; unabhängige Sach-/Altersprüfung bleibt erforderlich. |
| Oberfläche | **681 tatsächliche Renderbilder** in vier Displayprofilen; 99.756 Prüfungen über 1.800 Wortansichten und 14.400 Schriftmessungen ohne Überlauf bestanden. Neue Helmaufgabe auf kleinem Display manuell angesehen. Kein vollständiger manueller Bild-/Gerätetest. |
| Punkte / Start | 64.000 aktuelle Punkte, mit alten Belohnungen maximal 67.200. Separater Neustart stellt **3.470 Testpunkte** wieder her, ohne doppelte Belohnung. Frischer Import/Start aus ausgelieferten Dateien und isolierter Familienstart mit 60 echten Frames bestanden. |
| Unterbrechung | Konkreter Fehler behoben: Belohnungstöne pausieren jetzt wie Sprache/Musik beim Hintergrundwechsel. Neuer Test mit **66 echten Godot-Prüfungen**: Pause/Fortsetzung, ausstehendes Lob, gehaltene Geste, gespeicherte Punkte/Kulisse und fünf Drehungen einer offenen Aufgabe. Desktop-Notifications/Resize, keine Android-Hardware- oder Audiofokus-Zertifizierung. |
| Audio / Technik | **Alle 3.803 tatsächlichen Ogg-Dateien decodiert**, 7.281 aktuelle Text-/ID-Bindungen und Dateihashes geprüft. 36 Wiedergabe-, 75 Sequenz- und 38 Weltsprachprüfungen bestanden. Alle 44 geänderten Aufnahmen zusätzlich mit gepinntem CI-FFmpeg decodiert; Dauer/Pegel bestanden. Vollständige Wellenformen und Randstille, Modell-/Lizenznachweise erhalten. |
| Aussprache | Dieselben Frauenstimmen; 44 Aufnahmen gezielt überarbeitet: vier DE- und zehn EN-Stationen einschließlich Boni, zwei RU-Grundfragen. Bei allen 50 nativen Wortfragen je Sprache gewinnt ASR **39/50 DE, 41/50 EN, 44/50 RU** Zielschreibweisen zurück (vorher 35/31/42). Alle 28 geänderten DE-/EN-Bonusfragen vollständig erkannt. Originale Probeparameter und genaue Eingänge bleiben nachgewiesen. ASR-gestützte Auswahl ist kein unabhängiger menschlicher Verständlichkeits- oder Betonungsnachweis; nicht erkannte Wörter bleiben sichtbar. |
| Vollständige Hörabnahme | Offlinepaket mit allen **3.803 unterschiedlichen Aufnahmen / 7.281 Verwendungen** tatsächlich erzeugt; aktuelle Hashes geprüft und JavaScript-Syntax validiert. Prüferklärungen können lokal exportiert/fortgesetzt werden; stale, doppelte oder um persönliche Felder erweiterte Belege werden abgelehnt. Ein leerer Beleg führt tatsächlich zu `INCOMPLETE` / Exit 2. **Keine menschlichen Freigaben eingeholt**, keine vollständige Browser-/Hörabnahme behauptet. |
| Android | **Beide APKs und beide unsignierten AABs tatsächlich gebaut und technisch bestanden.** Familie 7.801, neutral 7.791 geprüfte Ressourcen. Paket/Version, API 24–36, `arm64-v8a`/`x86_64`, ZIP-/ELF-16-KB-Ausrichtung, Launcherbilder und Inhaltsintegrität geprüft. APKs mit bestehender Entwicklungsidentität (v2), AABs unsigniert; Play weiterhin gesperrt. |
| Datenschutz / Herkunft | Begrenzter Quell-/Konfigurationsaudit: keine Netzwerk-/Konten-/Werbeintegration, keine Android-Berechtigungen, Backup deaktiviert. Private Figurenquellen und Android-/Qwen-Workflows unverändert. Quality-Workflow veröffentlicht nur ein separates Hörpaket ohne Familienbilder oder Zugangsdaten. Keine personenbezogenen Testdaten erhoben; keine umfassende Sicherheits-/Rechtszertifizierung. |
| Dokumentation | Alle lokalen Dokumentationsziele und CI-Dateireferenzen geprüft; Details im Laufprotokoll. Alle drei Workflow-YAMLs syntaktisch geparst. `docs/qa/` unverändert zwei Referenzdateien / 78.669 Bytes; 139 historische Originaldateien weiterhin verifiziert. Allgemeine externe HTTP-Erreichbarkeit wird nicht pauschal zertifiziert. |

Die vollständige Suite fand zunächst eine veraltete positive Android-Testfixture: Sie führte die neuen Mützenressourcen noch nicht auf. Die Fixture wurde um Import- **und** Texturdateien ergänzt; die strengere Paketprüfung bleibt erhalten. Ihre 17 Prüfungen bestanden anschließend; die vollständige Suite wurde danach mit allen 135 Python-Tests und sämtlichen Godot-/Qualitätsgates erfolgreich wiederholt.

Lokale Nachweise: `qa-results/qa-v093-full-suite-final.log`, `qa-results/visual-v093-acceptance/`, `qa-results/qa-lifecycle-before.log`/`qa-lifecycle-after.log`, `qa-results/qa-final-native-words.json`, `qa-results/qa-final-native-ru.json`, `qa-results/qa-bonus-clarity-*.json`, `qa-results/qa-documentation-final.log`, `build/listening-acceptance-v093/` und `build/android-v093-acceptance/delivery.json` samt Varianten-Provenienz/Verifikation. Die notwendigen [Worterkennungsreferenzen](../tests/fixtures/voice/subject-recognition.json) und [Bonusreferenzen](../tests/fixtures/voice/carrier-recognition.json) bewahren gemessene Transkripte und Audiohashes im Git. Keine neuen Rohlogs eingecheckt.

### Tatsächlich erzeugte lokale Dateien

APK-Zertifikat wie beim lokalen 0.9.2-Vorgänger: SHA-256 `3444a17df292f9c04a47059082669d28e67bb16014c81bdfa0910d01f0389c15`. Stabile Testpakete `.preview.family.v090` / `.preview.neutral.v090` bleiben erhalten. Das ist eine technische Updatevoraussetzung; ein echtes Android-Update wurde hier nicht ausgeführt. Bei Zertifikatsabweichung nicht deinstallieren, wenn Punkte erhalten bleiben sollen.

Unter `build/android-v093-acceptance/`:

| Datei | Bytes | SHA-256 |
|---|---:|---|
| `kinderwelt-debug-family.apk` | 323,910,788 | `af98141960b91713ddebfae24ae03ac784d3ce8e0b6d4fde63a45cbb7c345296` |
| `kinderwelt-unsigned-family.aab` | 309,995,434 | `257ea05aa2c4644285440eb73d2a9459ae678c6479463866681e41c68cb64c7d` |
| `kinderwelt-debug-neutral.apk` | 319,039,837 | `0398d35fabc7113d4e97898218d13a53fdf097f1b70a3eabbcb430d0b7afbf6e` |
| `kinderwelt-unsigned-neutral.aab` | 305,132,045 | `44dfd3fdd81daa8574e091e54b907c0f9b117973aa143eabec1e4d19aafbcedb` |


Das kompakte `kinderwelt-listening.html` mit 262 echten Hörfolgen liegt der Android-Ausgabe bei. Das vollständige Hörpaket wird separat in Quality-Actions veröffentlicht; ZIP entpacken, `index.html` öffnen. Beide Pakete sind Prüfhilfen, keine erfolgte Hörfreigabe.

## Noch erforderliche menschliche Freigaben

- **Muttersprachliches Hören:** alle Aufnahmen, insbesondere verbleibende Wortfragen, Betonung, interne Zahlwortverbalisation und Fachbegriffe; reale Lautsprecher/Kopfhörer und Musikbalance.
- **Android-Geräte:** Rotation, Touch, Audiofokus, Unterbrechungen, Prozessneustart und echtes Update mit gespeichertem Spielstand. Hier kein nutzbares angeschlossenes Android-Gerät oder eingerichteter Emulator; `/dev/kvm` fehlt. ADB konnte in dieser Sandbox sein unveränderliches Standard-Konfigurationsverzeichnis nicht anlegen. Keine Geräteprüfung als ausgeführt markiert.
- **Unabhängige fachpädagogische Prüfung und Kinderbeobachtung:** konkrete Unterrichtsmodelle, Mehrdeutigkeiten, Lesebelastung und Schwierigkeitsniveau. Entwicklerdurchsicht, Merkmalszählung und konsistente Antworten beweisen keine Lernwirkung. Mehrere externe Fachquellen waren mit HTTP 403 gesperrt; kein erfolgter Quellenabgleich behauptet.
- **Betreiber / Play:** endgültige Paketkennung, Herausgeber/Kontakt, Datenschutzerklärung, Zielgruppen-/Altersangaben, Medienrechte, Store-Eintrag, Release-Signierung und aktuelle Console-Vorgaben. Entscheidungsvorlagen und sichere Einrichtungshinweise vorbereitet; keine Schlüssel erzeugt oder Freigaben geändert.

[Praktische Protokolle und wissenschaftlicher Evaluationsplan](ACCEPTANCE.md) · [Play-Voraussetzungen und Entwürfe](PLAY_READINESS.md). Personenbezogene Kinder-/Forschungsdaten erst nach gesonderter Entscheidung und Schutzkonzept erheben. Aktuell keine Kinderaufnahmen oder Telemetrie; empirische Lernwirkungen nicht nachgewiesen.

## Historische Nachweise und Dokumentationsregeln

Die [vollständige 0.9.2-Prüfübersicht](https://github.com/sayac007/Kinderwelt/blob/4e81e4b34817f4f609ab11c0a73e1824911b3f5b/docs/QUALITY_ASSURANCE.md) enthält die damaligen APK-/AAB-Hashes, 129 Python-Tests und sämtliche Decoder-/Aussprachebefunde. Diese Angaben sind historisch, keine neuen Builds.

[Archiv und Inventar](qa/README.md): **139 unveränderte Originaldateien / 7.383.943 Bytes** bleiben im geprüften Git-Archiv unter Tag `qa-evidence/2026-10-23-v091`, Commit `a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`, dauerhaft erhalten. `docs/qa/` weiterhin zwei Referenzdateien / 78.669 Bytes. Keine historischen QA-Dokumente gelöscht oder privaten Assets veröffentlicht.

Im Git nur aktuellen Überblick, Anleitungen, bekannte Grenzen und notwendige langfristige Referenzen pflegen. **Keine neuen Einzelberichte je Testlauf.** Neue Logs/JSONs nach `qa-results/` oder `build/`. Langfristige Freigaben brauchen verifizierte Ablage mit Commit, Datum, Dateinamen und Hashes; Originale erst nach verifizierter Ersatzablage entfernen. CI-Artefakte laufen ab und sind kein dauerhaftes Freigabearchiv. `documentation.py` prüft lokale Links, Archivindex und CI-Dateireferenzen; README und Überblick nennen dieselben Testkommandos.
