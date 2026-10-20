# Musik in Kinderwelt 0.2

Die fünf WAV-Dateien sind tatsächlich erzeugte, integrierte und offline ladbare
Mono-PCM-Aufnahmen mit 22.050 Hz und 16 Bit. Keine moderne Aufnahme, kein Soundfont,
kein fremdes Arrangement und kein Mario-/Nintendo-Motiv wurde übernommen.
`scripts/compose-music.py` synthetisiert die Stimmen aus Sinus-Obertönen mit
weichen Hüllkurven und eigenen Begleitungen. Das ist ein hörbarer Retro-Prototyp,
keine Behauptung einer professionellen Musikproduktion oder originalgetreuen
Notenausgabe. Musikalische Wiedererkennbarkeit und angenehme Wirkung benötigen
noch eine menschliche Hörprüfung.

| Welt / Datei in assets/music | Kompositorische Inspiration | Länge / Tempo |
|---|---|---|
| logic.wav | Liszt, Liebesträume Nr. 3 | 22,86 s / 84 BPM |
| math.wav | Liszt, Ungarische Rhapsodie Nr. 2 | 17,78 s / 108 BPM |
| language.wav | Puccini, O mio babbino caro | 24,62 s / 78 BPM |
| autonomy.wav | Liszt, La Campanella | 18,46 s / 104 BPM |
| social.wav | Puccini, Nessun dorma | 23,41 s / 82 BPM |

Die neu gesetzten/transponierten kurzen Motivreihen, Bassfolgen und Tempi stehen
in der Synthesequelle sowie `assets/music/manifest.json`. Sie sind eigene
Miniaturstudien mit diesen Ausgangspunkten, keine aus einer überprüften kritischen
Partitur übertragene Edition. Liszt starb 1886, Puccini 1924; die zugrunde gelegten
Kompositionen sind im deutschen/EU-Kontext gemeinfrei. Schutzrechte moderner
Notenausgaben, Aufnahmen und Bearbeitungen sind davon getrennt. Keine solche
Aufnahme/Edition wird mitgeliefert. Die eigene Synthese und erzeugten Aufnahmen
stehen wie der Projektcode unter MIT. Vor einer Distribution in weiteren
Rechtsräumen ist deren Rechtslage passend zu prüfen; es werden keine weltweiten
Rechte pauschal zugesichert. Es gibt keinen Gesang oder abgedruckte Operntexte.

Reproduktion: `python3 scripts/compose-music.py` im Repository. Anschließend Godot
importieren. Das Manifest enthält SHA256, Notenreihen, Frequenzbasis und Peakwerte.
Die Tests prüfen echte Dateien auf passenden Hash, Länge, Signalenergie, stille
Randwerte und Abstand zur Übersteuerung. Beispielmessung logic.wav mit FFmpeg:
Mittel -22,5 dBFS, Peak -14,2 dBFS vor dem einstellbaren Wiedergabepegel.
Das ist kein Lautheitsnachweis auf Telefonlautsprechern.

`core/music.gd` nutzt zwei AudioStreamPlayer und 0,7-s-Überblendungen, vollständige
Loop-Grenzen auch nach Godots komprimiertem Import, Pausieren/Fortsetzen und eine
zentrale Bankzuordnung. Standard-Musikpegel 0,35, Spielklänge 0,6; beide regelbar
bis null und gemeinsam stummschaltbar. Einstellungen bleiben lokal. Ruhige eigene
Hinweistöne und ein kurzer harmonischer Erfolgsklang stammen aus `cues.gd`.

## Nächster musikalischer Produktionsschritt

Ein Musiker prüft die Motive anhand geeigneter gemeinfreier Quellen, präzisiert
Phrasierung, Register und Loop-Anschluss und hört sie auf einem Telefon bei leiser
Lautstärke ab. Keine dauernde Dramatik, keine erschreckenden Spitzen. Danach mit
Kind prüfen, ob Musik Konzentration stört; Abschalten bleibt gleichwertig möglich.

Für eine optionale orchestrale Variante dieselben MIDI-Themen/Bassereignisse
verwenden, Instrumentierung und Dynamik separat produzieren und ausschließlich
geeignet lizenzierte/eigene Instrumentaufnahmen einsetzen. Erst nach Hörprüfung
als zusätzliche Bank registrieren. Momentan gibt es **nur die echte Retro-Bank**;
keine orchestrale Auswahl mit identischem Ersatzklang und keine Fake-Dateien.
