# Kinderwelt

Ein **offline spielbares Lernabenteuer für Klasse 1–2**, derzeit mit anspruchsvolleren Inhalten für die zweite Klasse. Kinder bewegen eine Figur durch sieben wählbare Welten, lösen Aufgaben und sammeln dauerhaft lokal gespeicherte Punkte. Keine Konten, Werbung, Käufe, Ranglisten oder Zeitlimits.

**Inhalte:** acht Fächer mit je 40 Grundaufgaben: Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch und Geografie. Zu jeder Grundaufgabe gehören zwei freiwillige Boni: insgesamt 320 + 640 Aufgabenplätze. Deutsch, Englisch und Russisch haben eigene Sprachlernaufgaben. Sieben Figuren, fünf Looks, 20 klassische Klavierwiedergaben und lokale Sprachclips ergänzen das Spiel. Familien- und neutrale Variante verwenden dieselbe Spiellogik; Familiengrafiken bleiben separat privat.

**Hier beginnen:** [Qualität, Architektur, Prüfstand und Grenzen](docs/QUALITY_ASSURANCE.md). Dort sind technische Testerfolge, offene fachliche Prüfungen und nicht nachgewiesene Lernwirkungen getrennt. [Bedienung](docs/experience.md) · [Inhaltsquellen und Redaktion](docs/CONTENT_AUTHORING.md) · [Android](docs/android.md) · [Sprachprüfung](docs/voice.md).

## Entwickeln und prüfen

Benötigt: **Godot 4.7.2**, Python 3 und FFmpeg; für grafische Prüfungen eine Anzeige oder `xvfb-run`. Die neutrale Variante benötigt keine Familien-Assets oder Tokens.

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Für wiederholte Bildprüfungen ein neues Ausgabeverzeichnis wählen.

App-Einstieg: `core/quest/main.tscn`; erzeugte Inhalte: `games/quest/tasks.json`. Ältere Nachweise bleiben vollständig im [versionsfesten QA-Archiv](docs/qa/README.md). Neue Laufberichte gehören in CI-Artefakte, nicht als Einzeldateien ins Git.
