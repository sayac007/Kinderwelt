# Audio 0.4: tatsächliche Quellen und offene Hörprüfung

Alle neuen Musiknoten, Texte und synthetischen Signale sind eigene Inhalte. Es wurden
keine Nintendo-Melodien, fremden Audioaufnahmen oder geschützten Sprecheraufnahmen verwendet.
Die fünf älteren Weltmusiken bleiben für Kompatibilität erhalten; die normale Musikauswahl
verwendet die bessere elektronische Richtung aus 0.3 und acht neue Stücke.

| Titel | BPM | Datei |
|---|---:|---|
| Funkenflug | 132 | `assets/music/adventure/workshop.wav` |
| Sternensprung | 146 | `assets/music/adventure/stars.wav` |
| Wiesenwind | 116 | `assets/music/modern/meadow.ogg` |
| Zahnrad-Tanz | 138 | `assets/music/modern/gears.ogg` |
| Markttag | 128 | `assets/music/modern/market.ogg` |
| Wolkenbuch | 104 | `assets/music/modern/stories.ogg` |
| Gartensprung | 122 | `assets/music/modern/garden.ogg` |
| Hand in Hand | 134 | `assets/music/modern/together.ogg` |
| Regentropfen | 110 | `assets/music/modern/rain.ogg` |
| Geschafft! | 154 | `assets/music/modern/victory.ogg` |

Die Miniaturen dauern jeweils über 20 Sekunden, mit Melodie, Bass, Akkorden, Rhythmus
und weiteren Ebenen. Acht neue Notenfolgen und decodierte Audios sind nachweislich
unterschiedlich; dazu kommen die beiden eigenen Originale aus 0.3. Klangästhetik und
Abwechslung wurden nicht von Menschen bewertet. Es wird keine Konsolenproduktion behauptet.

Generatoren: `scripts/compose-adventure.py` und `scripts/compose-modern.py`. Die neuen
Stücke werden mit FFmpeg als mono Ogg Vorbis, Qualität 5, 22050 Hz gespeichert. Die zwei
bestehenden WAVs verwendet Godot weiterhin mit QOA-Import. Kurze Randblenden verhindern
Sample-Sprünge; es bleibt eine manuelle Prüfung auf hörbare Loopstellen erforderlich.
Metadaten, Tempi, Noten und SHA-256: `assets/music/modern/manifest.json` und das bestehende
Adventure-Manifest. Zehn bloß umbenannte Kopien werden durch die Prüfungen nicht akzeptiert.

Ein neu synthetisiertes, deterministisches WAV von „Gartensprung“ wurde mit dem gelieferten
Vorbis-Decode verglichen: **694033 Frames auf beiden Seiten**, normalisierte Korrelation
**0,99913**, Signal-zu-Fehler-Abstand **27,57 dB**, kein Clipping. Das ist ein objektiver
Codecvergleich eines Titels, **kein menschlicher Hörtest** und keine Zertifizierung aller
zehn Mischungen. Die PCM-/Pegel-/Längenprüfungen erfassen alle acht neuen Dateien; bestehende
Tests prüfen die bisherigen WAVs weiter.

## Deutsche Prototypstimme

[Auftrag anhören: Die Pflanze hat Durst](../assets/voice/water_0.ogg).

18 tatsächliche Vorbis-Sprachclips enthalten eigene deutsche Orts-/Menüansagen,
Figurennamen und die drei Aufträge, Hilfe und Erfolg der Pflanzenmission. Die Stimme ist
**eSpeak NG 1.52.0, Deutsch, 145 Wörter/Minute, Pitch 48**: technisch funktionierend,
aber robotisch und ausdrücklich kein natürlich klingendes Veröffentlichungsmaterial.
Die Anzeige in den Einstellungen kennzeichnet sie als synthetischen Prototyp.

`scripts/generate-voice.py` erzeugt die Aufnahmen offline und komprimiert mit Vorbis q4.
Texte, Clip-Hashes und Checksummen der zur Erzeugung benutzten Debian-Pakete stehen in
`assets/voice/manifest.json`. eSpeak NG ist ein GPLv3-Erzeugungswerkzeug; weder dessen
Executable noch Wörterbücher oder Bibliotheken werden in die App gepackt. Die eigenen
Texte und erzeugten Inhalte folgen der Repository-Lizenz. Die Android-Buildpipeline
benötigt kein eSpeak und keine Cloud-TTS, weil die fertigen Dateien versioniert sind.

Erneut erzeugen bei vorbereiteten lokalen Tools:

```bash
python3 scripts/compose-modern.py
python3 scripts/generate-voice.py --tools /workspace/tools/voice
python3 -m unittest discover -s tests/android -v
```

Die ersten beiden Befehle sind Erzeugungswerkzeuge, keine App-Laufzeitbefehle. FFmpeg
wird für Erzeugung und Decoderprüfungen benötigt; GitHub Actions installiert den Decoder
explizit. Fertige Ogg-Dateien und ihre Hashes sind die gelieferten Artefakte. Vorbis-
Container und Builds sind nicht als über alle Encoderstände byteidentisch zugesichert.

## Vor einer hochwertigen Veröffentlichung noch nötig

Natürliche deutsche Aufnahmen aller neuen Sätze, Aussprache- und Verständlichkeitstest,
Lautstärkeabgleich und echte Telefonlautsprecher-/Kopfhörerprüfung fehlen. Auch die
musikalische Motivation, subjektive Vielfalt und der Übergang zu gesprochener Anleitung
benötigen menschliches Hören. Automatisiert geprüft wurden echtes Laden/Abspielen,
Wiederholen, Automatik aus, Stumm, getrennte Regler, Ducking, natürliche Clip-Ende-Signale
und Pause/Wiederaufnahme. Das Desktop-Audiogerät war Dummy, keine reale Audioausgabe.
