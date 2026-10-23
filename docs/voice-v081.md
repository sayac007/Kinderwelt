# Englische Stimme für Deutsch und Russisch – tatsächlicher Befund

> Historischer Versionsbericht. Aktuelle Funktionen, Tests und offene Freigaben: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die folgenden Ergebnisse gelten ausschließlich für den genannten früheren Stand.

Die gewünschte gemeinsame Stimmidentität ist in diesem Stand **noch nicht umgesetzt**. Die vorhandene klare englische LJSpeech-Aufnahme bleibt erhalten; deutsche und russische Aufnahmen wurden nicht durch einen schlechteren Versuch ersetzt.

## Tatsächlich ausgeführter Versuch

Das vorhandene englische Piper-LJSpeech-Modell wurde mit deutscher beziehungsweise russischer eSpeak-Lautung statt englischer Lautung angesprochen. Dieselbe unterstützte IPA-Normalisierung und vollständige Satzsynthese wie im bestehenden Generator wurden verwendet. Je Sprache wurden sieben echte WAV-Aufnahmen erzeugt: Physik, Chemie, Lob, Apfelzählaufgabe, Sonne/Anfangsbuchstabe, Magnet-Hinweis und Stadthinweis. Modell und Texte stammen aus dem aktuellen App-Stand.

Die unabhängige Erkennung mit multilingual Whisper small/int8 erhielt **keine Referenztexte**. Ergebnis: **DE 45,02 %**, **RU 62,91 %** Zeichenabweichung. Bereits „Physik“ wurde als „Fesik“ erkannt; längere deutsche und russische Sätze verloren erhebliche Wortteile. Dieser Versuch wurde verworfen. Einzelne Begriffe sind keine vollständige Verständlichkeitsmessung, aber der Versuch rechtfertigt gerade keinen Austausch der vorhandenen Aufnahmen.

Rohtexte, Dauer und Hashes: [v081-rejected-english-crosslang.json](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/v081-rejected-english-crosslang.json). Reproduzierbare Erzeugung unter `scripts/qa/try_english_voice.py`; sie schreibt ausschließlich in ein neues Entwicklungsverzeichnis und verändert keine App-Aufnahme.

## Echte sprachübergreifende Klangübertragung

OpenVoice V2 wurde als möglicher Konverter untersucht. Die öffentliche Dokumentation und der Konverter-Code konnten gelesen werden. Die notwendigen Modellgewichte von Hugging Face und dem offiziellen S3-Link wurden jedoch mit **HTTP 403 Forbidden** blockiert. Daher wurde **keine** OpenVoice-Konvertierung ausgeführt und keine Klangähnlichkeit oder Qualität behauptet. Weitere angefragte Hosts lieferten ebenfalls keine verwendbaren Gewichte. [Abrufbefund](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/v081-voice-model-access.json).

Ein nächster Versuch benötigt ein lokal verfügbares, hinsichtlich Herkunft und Nutzungsbedingungen geprüftes mehrsprachiges Konverter-/Sprachmodell. Als Referenz wären ausschließlich die bestehenden synthetischen LJSpeech-Clips vorgesehen. Vor einem Austausch sind die feste DE/EN/RU-Stichprobe, vollständige Decodierung, Pegel, Wort-/Satzdauer sowie eine menschliche Hörprüfung erforderlich. Ein bloßer Wechsel des Modellnamens, englische Lautung für fremdsprachige Texte oder simples Hochsetzen der Tonhöhe würde diese Anforderung nicht erfüllen.

Englisch, Deutsch und Russisch bleiben in der App vollständig offline; keine Modelle oder Dienste werden zur Laufzeit eingebaut. Dieser Stand enthält keinen Stimmenklon einer Schauspielerin.
