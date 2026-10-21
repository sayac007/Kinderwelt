# Tatsächliche Prüfungen Kinderwelt 0.7.1

Stand: 21. Oktober 2026. **Alle abschließenden lokalen technischen Prüfungen bestanden.** Keine physische Android-Geräteprüfung und keine menschliche Hörabnahme werden behauptet.

## Ausgeführt und bestanden

- **6.083 Godot-Spiel-/Layoutprüfungen:** weiterhin 320 Aufgaben, ursprüngliche 24 Aufgaben, lokale Spielstände, sieben Figuren/35 Looks, drei Sprachen, wechselnde Kulissen, Fortschritt, Drehungen derselben offenen Aufgabe und Bedienbarkeit.
- **30 Prüfungen tatsächlicher Audiowiedergabe:** Godots Audiobus wurde für „Physik“ und eine Aufgabe mit anschließendem Lob in allen drei Sprachen abgegriffen. Samplezahl, Peak, Zeit und Clipfolge geprüft. Eine sofort richtige Antwort kürzt den gesprochenen Auftrag nicht. [Messwerte](qa-evidence/v071/speech-playback.json).
- **36 Python-Tests**, einschließlich Android-Manifest-/Paket-/Signatur-/Ressourcen-Verifier, echten Audiodekodierungen und phonetischer Wortdauern.
- **343 echte OpenGL-Renderings** auf 360×800, 320×568, 800×360 und 1080×2400 mit simulierten 420 DPI, einschließlich acht zusätzlicher Bilder mit maximaler Punktzahl in Welt/Aufgabe. Godot 4.7.2, Mesa llvmpipe; Desktop-Simulation. Ausgewählte Bilder manuell betrachtet, keine vollständige Einzelabnahme aller 343 Bilder.
- Regulärer und cachefreier Start mit jeweils 60 Frames; alle **1.621** Sprachdateien und **20** Musikstücke vollständig dekodiert und auf Hash, Dauer und Pegel geprüft. Der begrenzte lokale Audit fand keine aktivierten Android-Berechtigungen oder Laufzeit-Netzwerkzugriffe.

Der Fehler mit dem Punktezähler war reproduzierbar: „Eichhörnchen“ vergrößerte die linke Schaltfläche auf 129 statt der geplanten 83 Pixel. Jetzt werden lange Namen begrenzt. Tatsächliche Rechtecke aller sieben Figuren × drei Sprachen × fünf Bildschirmprofile werden mit 3.200 Punkten auf Überschneidungen geprüft; zusätzliche echte Touchtests erreichen Figuren-/Menüschaltfläche. Aufgaben prüfen Schließen, Wiederholung und Frage neben/unter dem Zähler. [Kleines Display mit maximaler Punktzahl](screenshots/small-header-max-points.png), [Querformat-Aufgabe](screenshots/landscape-header-max-points-task.png).

## Sprachklarheit: gemessen und weiterhin zu beurteilen

Die gesamte deutsche Sammlung verwendet nach der Entscheidung des Nutzers eine unabhängige männliche **Thorsten-high-Stimme (CC0)**. Kein Stimmenklon. Die alte Physik-Aufnahme ließ nach Abzug eingefügter Stille etwa 0,304 Sekunden für die erzeugte Sprache; die neue enthält rund 0,789 Sekunden modellseitig zugeordnete phonetische Wortdauer. Das ist keine menschlich validierte Einzelwortausrichtung. Für alle neu erzeugten Aufnahmen werden VITS-Dauersumme und tatsächlich erzeugte Samplezahl abgeglichen. [Verfahren](speech-clarity-v071.md), [neue und alte Hörproben](voice-previews/README.md).

Unabhängiges Screening ohne Referenztext-Prompt: **31 feste Stichproben je Sprache**, multilingual Whisper small int8, sherpa-onnx 1.13.8. Dateihashes und Rohtranskripte sind gespeichert. Normalisierte Zeichenfehlerquote (keine Wortfehler-/Hörverständnisquote):

| Sprache | Vorher | Nachher |
|---|---:|---:|
| de | 20.98 % | 4.08 % |
| en | 1.08 % | 2.02 % |
| ru | 8.45 % | 7.63 % |

Mehrere Fachansagen und deutsche Auswahlformulierungen haben sich geändert. Die volle Tabelle isoliert daher keinen reinen Stimmeffekt. Für **18 exakt gleiche deutsche Referenztexte** sinkt die Zeichenfehlerquote von **13.09 % auf 5.82 %**. [Kontrollierter Textvergleich](qa-evidence/v071/speech-comparison.json).

Die Befunde bleiben ausdrücklich offen: „Chemie“ wird trotz korrekter Lautzuordnung noch abweichend erkannt; außerdem einzelne deutsche zusammengesetzte Wörter und englische/russische Fachnamen wie „Geography“/„География“. Englisch zeigt im Gesamtscreening keine Verbesserung. Ein ASR-Fehler beweist weder unverständliches Audio noch seine Verständlichkeit. Keine Freigabeaussage „jedes Wort klar“. Muttersprachler und Kinder müssen die tatsächlichen Aufnahmen hören, insbesondere die auffälligen Beispiele, mit/ohne Musik und auf dem Handy. [Vollständige neue Transkripte](qa-evidence/v071/speech-after.json).

## Tatsächlich erzeugte Android-Dateien

Beide Varianten stammen aus dem sauberen Quellcommit `cf3deb080c3f4be565b64fb1e7231d17846ff24c`. Die nachfolgende Dokumentation ändert keine App-Dateien. Beide Allowlist-Quellhashes wurden nach den Builds erneut gegen die aktuellen Quelldateien geprüft.

| Variante | Lokale Datei | Bytes | Signatur |
|---|---|---:|---|
| standard | `build/android-v071/kinderwelt-debug.apk` | 204,115,006 | temporärer Entwicklungsschlüssel; APK-Signatur geprüft |
| standard | `build/android-v071/kinderwelt-unsigned.aab` | 192,712,182 | UNSIGNIERT |
| preview | `build/android-v071-test/kinderwelt-debug.apk` | 204,115,062 | temporärer Entwicklungsschlüssel; APK-Signatur geprüft |
| preview | `build/android-v071-test/kinderwelt-unsigned.aab` | 192,712,310 | UNSIGNIERT |

Version **0.7.1 / Code 8**. Standardkennung `org.example.kinderwelt`, Testkennung `org.example.kinderwelt.preview.v071`, Name **Kinderwelt 0.7.1 Test**. Die separate Test-App kann neben der bisherigen App installiert werden; sie hat einen eigenen lokalen Spielstand. Temporäre Entwicklungsschlüssel sind keine dauerhafte Update-Identität. Die bestehende App nicht unbedacht deinstallieren.

Bei allen vier Dateien bestanden: Format/Paket/Version, API 24–36, `fullUser`-Rotation, keine Berechtigungen, kein Backup, arm64-v8a und x86_64, 16-KB-ELF-Ausrichtung, vollständige App-/Grafik-/Audio-/Lizenzressourcen, 3.413 geprüfte App-Einträge. Beide APKs bestanden Signatur- und 16-KB-ZIP-Ausrichtungsprüfung, beide AABs Bundletool-Validierung. Keine Release-Schlüssel verwendet; AABs bleiben unsigniert.

SHA-256:

```text
8516fa9e742a08114695a669a97e836fcb49da16e7bd122dbe8f70da0ae25978  build/android-v071/kinderwelt-debug.apk
5be881985819d79dc9cac5b264a62a29048526c98883a9c96004416a301cf3dd  build/android-v071/kinderwelt-unsigned.aab
794da418be3aa555dacb76b19a54746b558b786dbfad718f2de5207a4c7fd28d  build/android-v071-test/kinderwelt-debug.apk
957a8a14983a833c8439bebac7f2ee748538c9c25fea54f4928df2f28c69c3a4  build/android-v071-test/kinderwelt-unsigned.aab
```

Die APKs sind rund 204,1 MB, die AABs rund 192,7 MB groß. Archivgrößen sind keine gemessenen Geräte-Downloadgrößen oder installierten Speicherwerte. Dateien unter `build/` sind lokale Downloads und werden nicht ins Repository eingecheckt. Nach einem erfolgreichen Remote-Build liegen dessen Standard-Artefakte in GitHub Actions; der Remote-Lauf wurde hier nicht beobachtet.

## Rohprotokolle und Wiederholung

[Testsuite](qa-evidence/v071/tests.log), [Renderings](qa-evidence/v071/renderings.log), [343 Bildhashes](qa-evidence/v071/renderings.json), [Audit](qa-evidence/v071/audit.json), [Standard-Build](qa-evidence/v071/android-standard.log), [Preview-Build](qa-evidence/v071/android-preview.log), [Standard-Verifikation](qa-evidence/v071/standard-verification.json), [Preview-Verifikation](qa-evidence/v071/preview-verification.json). Provenienz, Manifest-, Signatur- und Größenberichte liegen im selben Nachweisordner. [Maschinenlesbare Gesamtübersicht](test-evidence.json).

```sh
KINDERWELT_SPEECH_REPORT=/tmp/wiedergabe.json GODOT=/pfad/Godot bash tests/run.sh
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 GODOT=/pfad/Godot bash tests/qa/quest-render.sh /tmp/neue-bilder
python scripts/qa/speech_recognition.py --model /pfad/sherpa-onnx-whisper-small --output /tmp/asr.json
python3 scripts/android/build.py --output build/neuer-standard
python3 scripts/android/build.py --preview --output build/neuer-test
```

Neue Ausgabeverzeichnisse verwenden; Renderer benötigt X11/OpenGL, ASR lokale Entwicklungsmodelle und sherpa-onnx. [Werkzeuge und Verfahren](speech-clarity-v071.md), [Android-Einrichtung](android.md).

Offen bleiben physische Installation/Bedienung, echte Safe-Areas, Audiofokus/Bluetooth/Lautsprecher, Leistung und Speicher auf Android, menschliche Ausspracheabnahme, fachliche/pädagogische und empirische Evaluation, dauerhafte Release-Signatur und alle Play-Freigaben. Keine nachgewiesene Lernwirkung oder Uploadbereitschaft.
