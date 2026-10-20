# Kinderwelt

Ein offline spielbares Lernabenteuer für die erste und zweite Klasse. **Wanja und vier weitere Familienfiguren** laufen durch die Spielwelt und lösen **320 eigene Aufgaben: je 40 in Mathe, Deutsch, Logik, Physik, Biologie, Chemie, Mensch und Geografie**. Jede erstmals gelöste Aufgabe gibt einen Stern und zehn Punkte. Es gibt keine Zeitlimits, Werbung, Käufe, Konten oder Ranglisten.

Die Figuren im 3D-Comicstil haben farbige Lichtkränze, Klickreaktionen, kleine Blitze sowie Lauf- und Jubelanimationen. Die App verwendet deutsche, englische und russische Menütexte und neuronale Sprachclips sowie vier auswählbare klassische Klavierwiedergaben. Sämtliche Wiedergabe funktioniert offline.

Dieser Projektstand enthält ausschließlich die neue App. Einstieg: `core/quest/main.tscn`. Aufgaben: `games/quest/tasks.json`.

## Entwickeln und prüfen

Godot **4.7.2** ist verbindlich. Python 3 und FFmpeg werden für die technischen Prüfungen benötigt.

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/quest-render.sh /tmp/kinderwelt-bilder
```

Android-Builds und Installationshinweise: [docs/android.md](docs/android.md). Aktuelle Ergebnisse: [docs/test-report.md](docs/test-report.md). Bedienung, Inhalte und Quellen: [docs/subjects-family-v06.md](docs/subjects-family-v06.md).

Die technische Prüfung ersetzt keinen Test mit Kindern oder auf echten Android-Geräten. Lernwirkung und Google-Play-Freigabe sind nicht nachgewiesen.
