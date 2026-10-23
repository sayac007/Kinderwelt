# Sprachvorschauen

Die aktuellen Sprachdateien und Zuordnungen liegen einmal unter [assets/voice/quest](../../assets/voice/quest/de/manifest.json). Modellnachweise und offene Hörprüfungen: [Stimme](../voice.md).

Aktuelle Beispiele in drei Sprachen lokal erzeugen:

```sh
python3 scripts/qa/previews.py voice --output build/voice-previews
```

FFmpeg ist erforderlich. Enthalten sind Physik, Frage, Hinweis und Lob; die originalen Modellkarten liegen bei.
