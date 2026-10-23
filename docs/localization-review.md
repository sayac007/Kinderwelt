# Sprache und Lokalisierung prüfen

Aktueller Status und Einschränkungen: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Alle 400 Grundaufgaben und 800 Boni haben DE-/EN-/RU-Fassungen. Native Sprachaufgaben verwenden die jeweilige Sprache; russische Lerntexte bleiben kyrillisch.

Hinweise nennen keine vollständigen Antworten oder fehlenden Buchstabenlisten. Neue Fachwörter werden im Kontext erläutert; „Hebel“ wird mit der vertrauten Wippe verknüpft, der Drehpunkt als Stelle der Bewegung erklärt. Das lange deutsche Lernwort „Schildkrötenei“ ist durch das geläufigere „Entenei“ ersetzt. Die ursprünglichen Werte und aktuellen Grundtexte sind als langfristige Redaktionsreferenz in `scripts/content/localization-changes.json` nachvollziehbar, nicht als neuer Bericht pro Testlauf.

Deutsch und Russisch nutzen dieselbe weibliche Serena-Modellstimme, Englisch LJSpeech. Keine identische Stimmidentität aller drei Sprachen behauptet. Geänderte Textfelder müssen mit den tatsächlich gelieferten Audio-Manifesten und Hashes übereinstimmen. [Audioverfahren und Hörfreigabe](voice.md).

```sh
python3 scripts/content/generate.py
python3 scripts/qa/localization.py --check
```

Muttersprachliche Hör-/Textfreigabe, natürliches Sprachgefühl und kindliches Verstehen bleiben manuell zu prüfen. Technische Zeichen-/Dauerprüfungen und ASR belegen keine Lernwirkung.
