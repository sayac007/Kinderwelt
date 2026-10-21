# Stimme, Herkunft und Hörprüfung

Deutsch verwendet bereits **Piper Thorsten high, CC0, 22.050 Hz**. Die frühere Angabe „Kerstin low“ beschreibt einen abgelösten Stand. Empfohlen und beibehalten wird Thorsten high; kein Modellwechsel und keine neue Lizenzbehauptung. Die Audios der Inhaltsphasen wurden mit diesem vorhandenen Modell erzeugt. Es gibt keine nachgebildete Schauspielerstimme.

| Geprüfte deutsche Alternative | Qualität laut Modellkonfiguration | Abtastrate | Datensatzlizenz | Entscheidung |
|---|---|---:|---|---|
| Thorsten medium | medium | 22.050 Hz | CC0 | klare alternative Herkunft; kein Hörvergleich dieser Lieferung, nicht ausgewählt |
| Thorsten high | high | 22.050 Hz | CC0 | vorhandenes Modell beibehalten |

Modellarchive: [medium](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-medium.tar.bz2), [high](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-high.tar.bz2). Datensatz: [Thorsten-Voice](https://github.com/thorstenMueller/Thorsten-Voice). Modell- und Kartenhashes sowie Quellen stehen in [voice-models.json](../scripts/qa/voice-models.json). Die Prüfung bezieht sich auf die tatsächlich lokal vorliegenden Modelle/Karten, nicht auf einen vollständigen aktuellen Onlinekatalog.

Die originale High-Modellkarte nennt im Titel „high“, im Qualitäts-Stichpunkt jedoch „medium“. Sie bleibt unverändert beigefügt. Die ONNX-Konfiguration nennt `audio.quality=high`; beide Varianten haben 22.050 Hz. Abtastrate allein unterscheidet keine Modellqualität. Diese Inkonsistenz ist dokumentiert und wird nicht durch Bearbeitung des Lizenznachweises verdeckt.

Englisch bleibt LJSpeech medium (Public Domain), Russisch Denis medium (CC0). Alle drei originalen Modellkarten sind im App-Paket enthalten. Der Android-Client spielt ausschließlich lokale Vorbisdateien; kein Modell, Mikrofon oder Sprachdienst ist eingebaut.

## Tatsächliche technische Prüfung

- 663 Clip-Zuordnungen pro Sprache; 587 deutsche, 523 englische und 523 russische unterschiedliche Dateien (gesamt 1.633).
- Vollständige Decodierung prüft Hash, Dauer, Pegel und stille Ränder. Modellseitig gemessene phonetische Dauer ist von hinzugefügter Stille getrennt; sie ist keine menschlich bestätigte Wortgrenze.
- Deutsche Generierung: Dauerfaktor 1,6, feste Lautdauern, normalisierte unterstützte IPA-Zeichen, vollständige Satzgrenzen. „Chemie“ hat eine explizite Aussprachezuordnung und bleibt ein Punkt für die Hörabnahme.
- Die Godot-Prüfung erfasst den tatsächlichen Audiobus: vollständige Frage, danach Lob, Musikabsenkung und Wiederherstellung, drei Sprachen. Eine schnelle Antwort darf die Frage nicht abschneiden.
- Unabhängiges ASR-Screening: multilingual Whisper small/int8, sherpa-onnx 1.13.8, keine Referenzvorgabe. 31 feste Beispiele je Sprache. Zeichenfehlerquote: **DE 4,189 %, EN 3,617 %, RU 7,464 %**. Rohtexte, Dateihashes und ASR-Modellhashes: [phase4-asr.json](qa/phase4-asr.json). Fehlerwerte sind nicht mit Lernwirkung oder kindlicher Hörverständlichkeit gleichzusetzen.

## Offen: Hören am Gerät

Kurze Fächeransagen (besonders Chemie), Zahlen, zusammengesetzte Wörter und deutsche Lernwörter mit/ohne Musik prüfen. EN/RU-Erklärung und anschließende deutsche Aufnahme gemeinsam hören. Muttersprachliche Erwachsene sollen jedes verstandene Wort ohne eingeblendeten Text vergleichen und undeutliche Stellen markieren. Danach freiwillige kurze Verständlichkeitsaufgaben mit Kindern; keine Aufnahme von Kinderstimmen und keine personenbezogenen Daten. Handy-Lautsprecher, Bluetooth, Unterbrechung/Aufwecken und Android-Audiofokus sind noch manuell zu prüfen.

ASR-Abweichungen umfassen weiterhin einzelne Fachnamen, deutsche Wortgrenzen und russische Auswahlwörter. Sie sind als offene Befunde enthalten, nicht als bestandene Hörabnahme ausgegeben.

## Reproduzieren

```sh
python3 scripts/qa/voice_models.py
python3 scripts/qa/voice_models.py --models /pfad/voice
python3 scripts/generate-quest-voice.py --locale de --model /pfad/de_DE-thorsten-high.onnx
python3 scripts/qa/speech_recognition.py --model /pfad/sherpa-onnx-whisper-small --output build/reports/speech-asr.json
GODOT=/pfad/Godot bash tests/run.sh
```

Entwicklungswerkzeuge: Piper 1.4.2, ONNX Runtime 1.31.0, ONNX 1.23.2, NumPy 2.5.4, FFmpeg. Generierung lädt keine Modelle selbst nach. Das ASR-Screening ist optional und offline; die reguläre Suite benötigt keine Modelle.
