# Weibliche Stimmen und Hörprüfung — 0.9.1

Deutsch und Russisch verwenden **dieselbe weibliche Modellstimme Serena** aus Qwen3-TTS-12Hz-0.6B-CustomVoice. Der Anbieter beschreibt sie als „warm, gentle young female voice“. Die bisherigen männlichen Thorsten-/Denis-Aufnahmen werden vollständig ersetzt. Englisch verwendet weiterhin die bevorzugte weibliche LJSpeech-Stimme; nur die undeutliche Geografie-Ansage wird neu erzeugt. Die Stimmen sollen ähnlich weich wirken; eine identische wahrgenommene Stimmidentität über alle drei Sprachen wird nicht behauptet.

Es handelt sich um eine echte weibliche Modellstimme, keine bloß hochgesetzte Männerstimme. Keine Schauspielerin, Familienaufnahme oder andere menschliche Referenz wird geklont. Der Android-Client enthält ausschließlich fertige lokale Vorbisdateien. Modelle, Python, neuronale Sprachengine, Mikrofon und Netzwerk kommen nicht in die App.

## Herkunft

| Sprache | Modell / Sprecherin | Lizenzangabe des Anbieters |
|---|---|---|
| DE, RU | Qwen3-TTS 0.6B CustomVoice / Serena | Modell Apache-2.0; Trainingsdaten nicht separat ausgewiesen |
| EN | Piper LJSpeech medium | Datensatz Public Domain |

Offizielles Qwen-Modell: Revision `85e237c12c027371202489a0ec509ded67b5e4b5`. Alle zwölf Modelldateien einschließlich Tokenizer und Konfiguration sind per SHA256 in `scripts/qa/qwen-source.json` festgehalten. Originale Modellkarten und der vollständige Apache-Lizenztext werden mitgeliefert. Die konkrete Herkunft und die unveränderten Lizenztexte werden geprüft.

`python3 scripts/qa/voice_models.py` prüft die ausgelieferten Modellkarten, Sprecherinnen, Lizenztexte und Provenienz. Optional werden die tatsächlich lokal vorliegenden Gewichte mit `--qwen-model /pfad/qwen` und `--models /pfad/piper` abgeglichen.

## Erzeugung und Messgrenzen

Der Generator verwendet vollständige Sätze, native Sprachsteuerung für Deutsch/Russisch, CPU-BFloat16/SDPA und deterministisch gesetzte Seeds. Aufnahmen werden nach Text dedupliziert. Das Manifest enthält pro Aufnahme die tatsächlich verwendeten Parameter und die gesamte Textgruppe; die zuerst geprüften gültigen Greedy-Aufnahmen bleiben erhalten, weitere Aufnahmen entstehen mit Seed-gesteuertem Sampling. Eine unabhängige Dauergrenze verwirft auffällige Wiederholungen oder Ausgaben am Tokenlimit, statt sie still abzuschneiden. Bis zu vier dokumentierte Einzelversuche mit eigenen Seeds und begrenztem Tokenbudget können eine fehlerhafte Gruppenausgabe ersetzen. Auch danach auffällige Ausgaben werden verweigert. Checkpoints erlauben die Wiederaufnahme.

Die vollständige Decoder-Wellenform bleibt erhalten. Es werden keine Wörter beschnitten, kein Pitch-/Formant-Filter und kein Stimmenkonverter angewendet. Vorne werden 200 ms und hinten 400 ms Stille ergänzt; die abschließende Vorbis-Decodierung kontrolliert Dauer, Pegel und stille Ränder. Modellseitige Rohsamplezahl und Hash werden getrennt erfasst. Die bisherige echte Vorbis-Pegelreserve bleibt erhalten. Zusätzlich wird aus dem tatsächlich decodierten Peak pro neuer Aufnahme ein konstanter Wiedergabepegel berechnet: Ziel 0,70, mit maximal +20 dB und mindestens −6 dB. Der Godot-Player wendet ihn zusammen mit dem Lautstärkeregler an. So bleiben die teilweise rund 14 dB leiseren weiblichen Rohaufnahmen ähnlich laut wie Englisch, ohne Re-Encoding, Kompression oder Änderung der Tonhöhe. Die Python-Prüfung kontrolliert die resultierende Reserve für jede Datei; der echte Godot-Mixer wird ebenfalls gemessen. Die Offline-Hörseite verwendet dieselbe Kalibrierung über Web Audio.

Qwen stellt keine Wortgrenzen wie die vorherige Piper-VITS-Instrumentierung bereit. Die alten phonetischen Zeitstempel werden deshalb nicht auf neue Aufnahmen übertragen oder erfunden. An ihre Stelle treten vollständige Wellenform-/Dauerprüfungen und eine unabhängige Erkennung der tatsächlichen kurzen Ansagen sowie ganzer Beispielsätze. Der Testbericht nennt die tatsächlich geprüften Stichproben und deren Grenzen. ASR-Zeichenabweichungen sind keine menschliche Hörfreigabe; unterschiedliche Zahlenschreibungen oder „Geografie/Geographie“ zählen dabei ebenfalls als Abweichung.

Die reguläre Suite decodiert jede ausgelieferte Aufnahme und prüft die realen Godot-Wiedergabefolgen, Absenkung der Musik, Unterbrechung und Rückkehr. Kurze Fächeransagen müssen zusätzlich zum tatsächlichen Dateihash passende unabhängige Erkennungsdaten besitzen. Ein Austausch der Audios ohne neue Messung lässt diese Prüfung scheitern.

## Reproduzieren

Entwicklung: CPU-Torch 2.6.0, torchaudio 2.6.0, qwen-tts 0.1.1, Transformers 4.57.3, Accelerate 1.12.0, NumPy 1.26.4, SoundFile und FFmpeg. Piper 1.4.2/ONNX Runtime bleiben nur für Englisch nötig. Der auf POSIX-Dateisperren gestützte Generator läuft unter Linux. Bereits gemessene gültige Aufnahmen können bei einem unterbrochenen Lauf wiederverwendet werden; Threadzahl und ursprüngliche Erzeugungsparameter bleiben in den einzelnen Aufnahmen beziehungsweise Prüfprotokollen dokumentiert. Alle Entwicklungswerkzeuge laufen außerhalb der Android-App; die normale CI benötigt keine TTS-Gewichte.

Das offizielle Modell mit der oben angegebenen Revision lokal herunterladen und den unveränderten Apache-Lizenztext aus `QwenLM/Qwen3-TTS`, Code-Revision `022e286b98fbec7e1e916cb940cdf532cd9f488e`, als `LICENSE.txt` daneben ablegen. Der Generator verweigert abweichende Gewichte, Konfigurationen oder Lizenztexte. Die vorläufige Prüfausgabe zunächst unter `build/` erzeugen:

```sh
python3 scripts/generate-multilingual-voice.py --locale de --model /pfad/qwen --output build/voice-review
python3 scripts/generate-multilingual-voice.py --locale ru --model /pfad/qwen --output build/voice-review
python3 scripts/qa/speech_recognition.py --model /pfad/sherpa-onnx-whisper-small \
  --voices build/voice-review --locales de ru --output build/voice-review-asr.json
python3 scripts/qa/voice_models.py --qwen-model /pfad/qwen --models /pfad/piper
GODOT=/pfad/Godot bash tests/run.sh
```

`generate-quest-voice.py --locale de|ru --model /pfad/qwen` verwendet ebenfalls diese weibliche Engine. Ein altes männliches ONNX-Modell wird dafür abgelehnt. `--locale en` bleibt beim ursprünglichen Piper-Modell. Erst geprüfte, vollständige Banken nach `assets/voice/quest/de` beziehungsweise `ru` übernehmen; keine Audios verschiedener Modellstände vermischen.

## Manuell offen

Muttersprachliche Erwachsene prüfen ohne eingeblendeten Text besonders Wortanfänge, Endungen, Verneinungen, Zahlen und Fachwörter. Danach mit Text vergleichen. In der APK mit Musik und mit Handy-Lautsprecher beziehungsweise Kopfhörern testen; den Höreindruck „weich und ähnlich wie Englisch“ ausdrücklich mitbewerten. Keine Kinderstimmen aufnehmen, keine personenbezogenen Daten sammeln. Das Actions-Artefakt enthält `kinderwelt-listening.html` mit echten Offline-Aufnahmen. Bluetooth, Android-Audiofokus und Geräteunterbrechungen benötigen weiterhin reale Gerätetests.
