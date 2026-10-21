# Musik: Quellen, Wiedergabe und offene Wünsche

Die App enthält eigene Instrumentalwiedergaben tatsächlich notierter klassischer Kompositionen. Es sind keine Aufnahmen der verlinkten YouTube-Videos. „Wiener Blut“ und „O mio babbino caro“ sind ausdrücklich gekürzte Themenauszüge; sie werden auch in der Musikauswahl so bezeichnet.

| Stück | Dauer der erzeugten Datei | Notenvorlage und Lizenz |
| --- | --- | --- |
| Johann Strauss II: Wiener Blut, Walzerauszug | 35,00 s | Christian F. Coors / OpenRCT2 OpenMusic, CC BY-SA 4.0; neu als Klavier gerendert, Tempo 180 Viertel/min |
| Giacomo Puccini: O mio babbino caro, Themenauszug | 73,72 s | MIDI aus tnm/mbot, MIT; zugrunde liegende Komposition von 1918 gemeinfrei; Tempo um Faktor 1,65 verlangsamt |
| P. I. Tschaikowski: Altes französisches Lied, Op. 39 Nr. 16 | 58,29 s | David McNamara / Mutopia, Public Domain; neue Klavierwiedergabe |
| Franz Liszt: Consolation, S.172 Nr. 1 | 103,00 s | Ryan Prince / Mutopia, CC BY 3.0; neue Klavierwiedergabe |

Die genauen Repository-Commits, Pfade und SHA-256 der Vorlagen stehen in [catalog.json](../scripts/music/catalog.json), die tatsächlich erzeugten Audiodateien mit Dauer und SHA-256 in [manifest.json](../assets/music/manifest.json). Die jeweiligen Audio-Bearbeitungen übernehmen die dort genannten Lizenzen. Herkunft, Bearbeitungsvermerk und Lizenzlinks werden mit der App in `assets/music/NOTICES.txt` ausgeliefert und sind unter „Für Erwachsene → Musik & Quellen“ zugänglich. Diese Lizenzen beziehen sich auf die jeweiligen Musikdateien.

Der Klavierklang stammt aus GeneralUser GS 2.0.3 von S. Christian Collins. Dessen beigefügte Lizenz gestattet private und kommerzielle Musikproduktion. Die SoundFont selbst und der Synthesizer werden nicht in die App eingebaut; die App spielt nur die vorab erzeugten Vorbis-Dateien ab.

Nach jedem Stück folgt automatisch das nächste. Wahlweise sind Zufallsreihenfolge und die Wiederholung eines einzelnen Stücks möglich. Ein Wechsel des Lernbereichs unterbricht die gewählte Musik nicht. Die Musik wird beim Vorlesen abgesenkt und bei App-Unterbrechungen pausiert.

## Erzeugung

Werkzeuge des tatsächlich ausgeführten Renderings: LilyPond 2.24.4, libfluidsynth 2.4.4, pyfluidsynth 1.4.0, mido 1.3.3, FFmpeg 7.1.5. Modelle und Werkzeuge sind Entwicklungsabhängigkeiten, keine Laufzeitabhängigkeiten der Android-App.

- LilyPond-Archiv: `https://gitlab.com/lilypond/lilypond/-/releases/v2.24.4/downloads/lilypond-2.24.4-linux-x86_64.tar.gz`; SHA-256 `53bc1df875ee56dabe56ae1f0b4550237e0c9acc837b60f0ef8c42fc35a68641`.
- GeneralUser: `https://github.com/mrbumpy409/GeneralUser-GS`, Commit `684543d5e5efaef08d02be50dcda8d552478fa60`; `GeneralUser-GS.sf2`, SHA-256 `9575028c7a1f589f5770fccc8cff2734566af40cd26ed836944e9a5152688cfe`.
- Die Noten/MIDI-Vorlagen liegen bereits unter `scripts/music/scores`; der Generator prüft ihre SHA-256 vor der Synthese.

```bash
/workspace/tools/piper-env/bin/python -m pip install mido==1.3.3 pyfluidsynth==1.4.0
/workspace/tools/piper-env/bin/python scripts/music/render.py \
  --lilypond-root /workspace/tools/classical/lilypond-2.24.4 \
  --soundfont /workspace/tools/classical/generaluser/GeneralUser-GS.sf2
```

Die Audiodateien werden fertig eingecheckt. CI und Android benötigen weder SoundFont noch LilyPond. Eine erneute Synthese kann durch Synthesizer-/Encoder-Versionen in den Bytes abweichen; der erzeugte Manifest-Hash bezeichnet immer die tatsächlich ausgelieferte Datei.

## Noch offen

Beide YouTube-URLs, YouTube-oEmbed und der alternative Titelabruf waren aus der Entwicklungsumgebung mit HTTP 403 gesperrt. Die Inhalte wurden nicht heruntergeladen oder angehört. „LITTLE BIG – SKIBIDI“ wurde vom Nutzer anschließend als Referenz angesprochen. Für dessen Originalaufnahme und Komposition liegt keine Nutzungslizenz für die App vor; das Original ist nicht enthalten. Die genaue Zuordnung und der Titel des zweiten YouTube-Links sind weiterhin offen.

Ein eigener elektronischer Track mit allgemeiner, verspielter Dance-Energie wäre ein weiterer möglicher Vorschlag. Eine Kopie von Melodie, Gesang oder dem markanten Rhythmus von „SKIBIDI“ wird nicht als Eigenkomposition ausgegeben.

Automatisierte Prüfungen verifizieren tatsächliche Dekodierung, Laufzeit, Pegel, Dateihashes, Notenquellen und die Fortschaltung beim realen Audio-Ende. Hörvergleich, musikalische Abnahme und das Lautstärkeverhältnis auf Android-Geräten bleiben manuelle Prüfungen.
