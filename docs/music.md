# Musik: 20 Klavierwiedergaben

Kuratierte Auswahl bekannter klassischer Stücke, keine objektive Rangliste der „besten aller Zeiten“. Rund 50 Minuten eigene Klavierwiedergaben aus benannten Noten-/MIDI-Ausgaben. Eigene instrumentale Wiedergaben. Wiener Blut und O mio babbino caro sind ausdrücklich Themenauszüge.

| Komponist | Stück / Fassung | Tatsächliche Dauer | Notenlizenz |
| --- | --- | ---: | --- |
| Johann Strauss II | Wiener Blut · Walzerauszug | 35.0 s | CC-BY-SA-4.0 |
| Giacomo Puccini | O mio babbino caro · Thema | 73.72 s | MIT (MIDI arrangement); public domain composition |
| P. I. Tschaikowski | Altes französisches Lied | 58.29 s | Public Domain |
| Franz Liszt | Consolation Nr. 1 | 103.0 s | CC-BY-3.0 |
| Ludwig van Beethoven | Für Elise | 133.83 s | Public Domain |
| Johann Sebastian Bach | Präludium C-Dur · BWV 846 | 143.0 s | Public Domain |
| Erik Satie | Gymnopédie Nr. 1 | 144.0 s | Public Domain |
| Claude Debussy | Clair de lune | 327.0 s | Public Domain |
| Frédéric Chopin | Nocturne · Op. 9 Nr. 2 | 205.27 s | CC-BY-SA-3.0 |
| Robert Schumann | Träumerei · Op. 15 Nr. 7 | 113.68 s | Public Domain |
| Wolfgang Amadeus Mozart | Sonata facile · Allegro | 135.72 s | CC-BY-SA-3.0 |
| Claude Debussy | Arabesque Nr. 1 | 180.5 s | Public Domain |
| Johannes Brahms | Walzer · Op. 39 Nr. 15 | 71.27 s | Public Domain |
| Johann Pachelbel | Kanon in D | 179.0 s | CC-BY-3.0 |
| Franz Schubert | Impromptu · D 899 Nr. 3 | 357.35 s | Public Domain |
| Johann Sebastian Bach | Invention Nr. 1 · BWV 772 | 69.0 s | CC-BY-SA-3.0 |
| Frédéric Chopin | Prélude e-Moll · Op. 28 Nr. 4 | 111.21 s | Public Domain |
| Christian Petzold | Menuett G-Dur · BWV Anh. 114 | 46.64 s | Public Domain |
| Wolfgang Amadeus Mozart | Rondo alla turca | 259.0 s | Public Domain |
| Ludwig van Beethoven | Mondscheinsonate · Adagio sostenuto | 279.0 s | CC-BY-SA-2.5 |

Die genauen Quellen, Upstream-Commits, Bearbeiter und SHA256 stehen in [catalog.json](../scripts/music/catalog.json), die erzeugten Audiodateien in [manifest.json](../assets/music/manifest.json). Vollständige Namensnennung, Links und Bearbeitungshinweise werden unter `assets/music/NOTICES.txt` mit der App ausgeliefert und unter „Für Erwachsene → Musik & Quellen“ angezeigt. Die Lizenztexte liegen unter `assets/music/licenses/` bei. Christian Petzolds Menuett wird in der alten Vorlage noch Bach zugeschrieben; die App nennt die heutige Zuschreibung und dokumentiert die Abweichung.

## Recording notices in the app

For all five CC-BY-SA-derived tracks, the app recording explicitly retains the
same CC-BY-SA version and licence URL as its source arrangement. This is stated
in `NOTICES.txt` and in the parent-only music credits in German, English and
Russian. Original author names, legal licence identifiers and pinned source
URLs remain visible in every locale; URLs are plain text and are not opened by
the app. This corrects the previous Russian view, which omitted those credits.
Other source licence assertions remain unchanged. The general asset scope is
documented in [ASSETS_LICENSE](../ASSETS_LICENSE.md).

Reproduce only the notice metadata, without rendering/transcoding any audio:

```sh
python3 scripts/music/notices.py
python3 scripts/music/notices.py --check
```

The full renderer also applies these notices on both newly rendered and cached
tracks. Android checks both presets' include/exclude filters and the actual bytes
of bundled source/model/font/software notices, including install-time assets.

## Erzeugung

Eigener Grand-Piano-Klang: GeneralUser GS 2.0.3 von S. Christian Collins, erlaubte Musikproduktion gemäß beigefügter Lizenz. SoundFont-SHA256 und tatsächlich verwendete Toolversionen stehen im Audiomanifest. SoundFont und Synthesizer werden nicht in die App eingebaut.

```sh
/workspace/tools/piper-env/bin/python scripts/music/render.py \
  --lilypond-root /workspace/tools/classical/lilypond-2.24.4 \
  --soundfont /workspace/tools/classical/generaluser/GeneralUser-GS.sf2
```

Werkzeuge: LilyPond 2.24.4, libfluidsynth 2.4.4, pyfluidsynth 1.4.0, mido 1.3.3 und FFmpeg. Der Generator prüft die Noten- und Abhängigkeitshashes, modernisiert ältere LilyPond-Syntax, überträgt veraltete Oktavangaben in `ottava` und entfernt obsolete reine Balken-Gravureinstellungen. Ein inaktiver `old-relative`-Kommentar wird vor `convert-ly` entfernt. Originalvorlagen bleiben bytegetreu erhalten. Eine validierte Zwischenspeicherung ermöglicht Wiederaufnahme; `manifest.complete` wird erst bei allen 20 Titeln gesetzt.

Nach jedem Stück folgt das nächste. Zufall und Wiederholung sind optional; Fach- und Kulissenwechsel starten die Musik nicht neu. Vorlesen senkt die Musik ab. Die Audio-Prüfungen dekodieren alle 20 Stücke und kontrollieren Dauer, Pegel und Hashes. Musikalische Abnahme und Balance auf Geräten bleiben offen.

[Hörproben lokal erzeugen](music-previews/README.md); im Repository liegen die vollständigen Audiodateien jeweils einmal unter `assets/music/`.
