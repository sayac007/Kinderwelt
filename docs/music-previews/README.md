# Musikvorschauen

Die vollständigen 20 Aufnahmen liegen unter [assets/music](../../assets/music/manifest.json), Quellen und Lizenzhinweise unter [NOTICES.txt](../../assets/music/NOTICES.txt). Keine doppelten MP3- oder ZIP-Dateien im Repository.

30-Sekunden-Vorschauen samt Hinweisen lokal erzeugen:

```sh
python3 scripts/qa/previews.py music --output build/music-previews
```

FFmpeg ist erforderlich. Die erzeugten Dateien liegen im ignorierten Build-Verzeichnis.
