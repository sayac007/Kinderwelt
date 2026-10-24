# Stimmen, Betonung und Hörprüfung — 0.9.2

Die bisherigen weiblichen Stimmen bleiben auf Wunsch erhalten: **Serena** aus Qwen3-TTS-12Hz-0.6B-CustomVoice für Deutsch und Russisch, **LJSpeech** für Englisch. Kein Pitch-/Formant-Filter, keine Schauspielerimitation und keine Familienaufnahme als Stimmvorlage. Die App enthält ausschließlich fertige lokale Vorbisclips; keine Sprachmodelle, Python, Mikrofon- oder Netzwerkanbindung.

## Herkunft

| Sprache | Modell / Sprecherin | Lizenzangabe des Anbieters |
|---|---|---|
| DE, RU | Qwen3-TTS 0.6B CustomVoice / Serena | Modell Apache-2.0; Trainingsdaten nicht separat ausgewiesen |
| EN | Piper LJSpeech medium | Datensatz Public Domain |

Qwen-Modellrevision `85e237c12c027371202489a0ec509ded67b5e4b5`: alle zwölf Dateien einschließlich Tokenizer und Konfiguration sind in `scripts/qa/qwen-source.json` mit SHA-256 gepinnt. Originale Modellkarten und Lizenztexte bleiben unverändert. `python3 scripts/qa/voice_models.py` kontrolliert die ausgelieferten Angaben, optional auch lokale Gewichte mit `--qwen-model /pfad/qwen --models /pfad/piper`.

## Wortbetonung: geprüftes Textwissen und tatsächliches Hören trennen

`scripts/voice/pronunciations.json` erfasst das vollständige aktuelle ausgeschriebene Vokabular. Quellen, Revisionen, Dateihashes und Original-Lizenztexte liegen in `scripts/voice/sources.json` und `scripts/voice/licenses/`:

- Russisch: NSU-AI `russian_g2p`, MIT; Wörterbuchformen plus redaktionelle Entscheidungen für den konkreten Spielkontext. `russian-context.tsv` und `russian-contexts.json` unterscheiden etwa **ру́ки / руки́**, **о́блака / облака́**, **о́рганы**, **оси́**, **четыре ноги́** gegenüber **вырастают но́ги** sowie **два/оба бе́рега** gegenüber der freien Mehrzahl **берега́**. `ё` bleibt erhalten.
- Englisch: CMUdict, BSD-Lizenz, zusammen mit der vorhandenen eSpeak-NG-Phonemisierung. Eindeutig passende mehrsilbige Einträge mit einer abweichenden Hauptbetonung erhalten die lexikalische Hauptbetonung im Piper-Phonemeingang. Schwache Satzbetonung, insbesondere einsilbiger Funktionswörter, wird erhalten. Phonemfolge und Nebenbetonung bleiben erhalten; mehrdeutige oder nicht passende Formen behalten ihre native kontextabhängige Aussprache.
- Deutsch: eSpeak NG aus der vorhandenen Piper-Entwicklungsumgebung liefert regel-/wörterbuchbasierte IPA-Referenzen. Das ist keine unabhängige muttersprachliche Freigabe jedes Wortes.

**Serena besitzt in dieser Engine keine Lautschrift-/Betonungsschnittstelle.** `instruct` wird beim 0.6B-Modell ignoriert. Flächendeckende Akzent-, Großbuchstaben- und Pluszeichenversuche verschlechterten die unabhängige Erkennung oder erzeugten Wiederholungen und wurden verworfen. `controls.json` begrenzt schriftliche Hinweise auf geprüfte Fachwörter und russische kontextabhängige Formen; alle übrigen Wörter behalten die natürliche Schreibweise. Für RU werden ausgewählte Akzente als zuvor separat geprüfter Apostroph nach dem betonten Vokal übergeben. Das bleibt eine **indirekte Hilfe**, keine garantierte Phonemanweisung. Sichtbare Texte enthalten diese Steuerzeichen nicht.

Ziffern und Rechenzeichen werden durch die jeweilige Engine verbalisiert. Das Wortregister zertifiziert diese internen Zahlwortformen nicht; Zahlwörter, Kasusformen und Betonung bleiben zusätzlich zu hören.

Jede neue Aufnahme enthält einen prüfbaren Nachweis des verwendeten Texts und der Wortreferenzen. Qwen-Batchregister bewahren den tatsächlich übergebenen Synthesetext. Unbekannte Wörter und veraltete Zuordnungen lassen `scripts/qa/pronunciation.py` scheitern. **Wörterbuchdeckung und ASR beweisen nicht die hörbare Betonung jeder Silbe.** Dafür bleibt eine muttersprachliche Hörprüfung erforderlich.

## Erzeugung und technische Prüfungen

Alle Sprachen werden nach tatsächlichem gesprochenem Text dedupliziert. Wortaufgaben trennen sichtbare Frage und `spoken_prompt`: Das Wort wird als Hörhinweis genannt, aber im Bild nicht vollständig geschrieben. Gesprochene Alternativen dürfen nur die Formulierung verbessern, nicht Fakten oder Antwort ändern.

Qwen verwendet CPU-BFloat16/SDPA und dokumentierte Seeds, Samplingparameter, Rohsamplezahlen und Wellenformhashes. Textbatches standardmäßig 48, maximal 64; der Waveform-Decoder verarbeitet unabhängig davon höchstens vier ähnlich lange Ausgaben. DE und RU auf dieser festen 32-GiB-Umgebung seriell erzeugen. Auffällige Tokenlimit-/Dauerausgaben werden vor dem Decodieren verworfen und höchstens viermal einzeln mit dokumentiertem Seed versucht. Kein stilles Abschneiden; vollständige Decoder-Wellenform und 200/400 ms Stille vorne/hinten bleiben erhalten. Checkpoints erlauben Wiederaufnahme, ohne alte Aufnahmen nur umzubenennen. Optional kann `--reuse-bank assets/voice/quest/de` (beziehungsweise `ru`) unveränderte Aufnahmen übernehmen: Modell/Sprecherin/Tokenizer müssen passen, der nach Hash geprüfte ursprüngliche Batch muss exakt den aktuellen Synthesetext enthalten und der Audiohash muss stimmen. Originalparameter, Seed und Wellenformhash bleiben erhalten; ein gesonderter Nachweis kennzeichnet die spätere lexikalische Prüfung ausdrücklich als nicht neu erzeugt. Geänderte Texte oder tatsächliche Betonungszeichen schließen diese Wiederverwendung aus.

Die Vorbis-Decodierung prüft Dauer, stille Ränder und Peak. Qwen-Wiedergabe wird pro Aufnahme aus dem tatsächlich decodierten Peak auf 0,70 kalibriert, begrenzt auf −6 bis +20 dB. Englisch behält seinen Piper-Pegel und die aus dem VITS-Modell abgeleiteten phonetischen Dauern. Für Qwen werden keine Wortzeitstempel erfunden. Bei sechs englischen Lernwörtern bleiben besser erkannte Originalaufnahmen erhalten: Modellhash, vollständige tatsächliche Phonemfolge und Syntheseeinstellungen wurden mit dem neuen Eingang abgeglichen. Die alten Erzeugungsmetadaten bleiben unverändert, der spätere Prüfstand wird getrennt dokumentiert. Die Auswahl nutzt ASR und ist deshalb kein davon unabhängiger nachträglicher Verständlichkeitstest. `tests/run.sh` decodiert jede ausgelieferte Datei und kontrolliert reale Godot-Wiedergabefolgen, Absenkung der Musik und Abbruch bei Navigation. Die Fächeransagen brauchen unabhängige Erkennungsdaten mit exakt dem ausgelieferten Dateihash.

## Reproduzieren

Entwicklungswerkzeuge: CPU-Torch 2.6.0, torchaudio 2.6.0, qwen-tts 0.1.1, Transformers 4.57.3, Accelerate 1.12.0, NumPy 1.26.4, SoundFile, FFmpeg; Piper 1.4.2/ONNX Runtime für EN und Wörterbuchkompilierung. Die normale CI benötigt keine TTS-Gewichte.

Offizielle Gewichte und gepinnte Wörterbuchdateien lokal bereitstellen. Qwen benötigt den unveränderten Apache-Lizenztext aus `QwenLM/Qwen3-TTS`, Code-Revision `022e286b98fbec7e1e916cb940cdf532cd9f488e`, als `LICENSE.txt` neben den Gewichten. Abweichende Dateien werden abgelehnt.

```sh
python3 scripts/voice/compile_pronunciation.py --russian /pfad/Accents_new.zip --cmu /pfad/cmudict.dict
python3 scripts/generate-quest-voice.py --locale en --model /pfad/en_US-ljspeech-medium.onnx --output build/voice-review
python3 scripts/generate-multilingual-voice.py --locale de --model /pfad/qwen --output build/voice-review
python3 scripts/generate-multilingual-voice.py --locale ru --model /pfad/qwen --output build/voice-review
python3 scripts/qa/pronunciation.py --voices build/voice-review
python3 scripts/qa/speech_recognition.py --model /pfad/sherpa-onnx-whisper-small \
  --voices build/voice-review --locales de en ru --output build/voice-review-asr.json
```

Erst vollständige, geprüfte Banken nach `assets/voice/quest/<locale>` übernehmen und die vollständige Suite aus [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) ausführen. `--ids` erzeugt nur eine Teilbank; diese niemals direkt ausliefern. Die Nachweise der tatsächlich ausgeführten Läufe und die Grenzen stehen zentral im Qualitätsüberblick, neue Rohlogs unter `qa-results/`.

Die tatsächlichen 24 Fächeransagen, neun Aufgabenbeispiele und 150 nativen Wortfragen sind als notwendige [Regressionsreferenz](../tests/fixtures/voice/subject-recognition.json) mit Audiohash, erwartetem Text und Erkennung erhalten. Auch nicht wiedergewonnene Zielschreibweisen bleiben dort sichtbar. Das ist kein neuer Einzelbericht pro Lauf.

## Manuell offen

Muttersprachliche Erwachsene hören ohne eingeblendeten Text, dann mit Referenz: Wortbetonung, Wortanfänge/-enden, Verneinungen, Zahlen, Fachwörter und alle neuen Lernwörter. Insbesondere die russischen kontextabhängigen Formen prüfen. Auf Handy-Lautsprecher und Kopfhörer, mit/ohne Musik testen. ASR-Abweichungen können Modellfehler oder tatsächliche Ausspracheprobleme sein; sie dürfen nicht pauschal als bestanden gelten. Das Actions-Artefakt enthält `kinderwelt-listening.html` mit echten Offline-Aufnahmen. Bluetooth, Android-Audiofokus und Geräteunterbrechungen brauchen reale Geräteprüfungen. Keine Kinderstimmen oder personenbezogenen Testdaten erheben.
