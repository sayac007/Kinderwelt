# Kinderwelt 0.7: Looks, Kulissen und klarere Bedienung

Sieben Figuren sind spielbar: Hauptheld Wanja, Mischa, Du, Mama, Katze, George und Eichhörnchen. George wurde anhand des bereitgestellten Bildes neu illustriert; die Eichhörnchenfigur ist eine eigene neue Gestaltung. Originalfotos und die beigefügte Schauspieleraufnahme werden nicht ausgeliefert.

## Kleidung und Kulissen

In der Figurenauswahl zuerst die Figur, dann unten ihren Look antippen: **Normal, Held, Alien, Astronaut, Forscher**. Jede Figur merkt sich ihre Kleidung unabhängig von den anderen. So entstehen **35 Kombinationen** einschließlich der bisherigen Outfits. Alle Looks bleiben beim Laufen und beim Jubel sichtbar. Die Auswahl ist ohne Punktehürde frei. Auf kleinen Bildschirmen stehen Wanja in der ersten Reihe und die übrigen sechs Figuren in zwei Reihen darunter.

Die neue Technik verwendet sieben Vierer-Atlanten statt 28 separater Bildladungen. Sichtbare Grenzen und eine native R8-Abtastmaske verhindern Bildreste benachbarter Outfits. Die originalen PNGs werden nicht verändert. Alle Kostüme und Tierfiguren verwenden durchgehende verformbare Netze, damit Mäntel, Umhänge und Schwänze intakt bleiben; die bisherigen normalen Menschenfiguren behalten ihre bestehende Animation. Atlas-/Maskencaches sind auf sieben Figuren und 28 Kostümrahmen begrenzt.

Drei Kulissen wechseln standardmäßig mit Fach und Wegabschnitt:

- Berge und Landschaft wie bisher.
- Zuhause mit Wandbildern, Sofa und einer schlafenden getigerten Katze.
- Schloss mit drei freundlich schwebenden Gespenstern; keine Schreckeffekte. „Weniger Bewegung“ hält die Gespenster still.

Unter **Einstellungen → Kulisse wählen** sind auch feste Kulissen möglich. Der Spielstand bleibt beim Wechsel erhalten. Kulissen und Kleidung werden ausschließlich lokal gespeichert.

## Bedienung und Punkte

Alle acht Fächer sind unten gleichzeitig antippbar: im Hochformat vier Spalten und zwei Reihen, im Querformat eine Reihe. Wischen ist nicht mehr erforderlich. Der größere helle Bereich und kleinere Piktogramme schaffen ausreichend große Trefferflächen. Die Weganzeige hat einen eigenen hellen Hintergrund, damit sie auch im Schloss und Zuhause lesbar bleibt.

Der farbige Punktezähler bleibt oben in Welt und Aufgabe sichtbar. Eine erstmals gelöste Aufgabe bringt weiterhin einen Stern und **zehn Punkte**: Zahl, Stern und „+10“ reagieren animiert. Wiederholungen erzeugen keine zusätzlichen Sterne/Punkte; ein Menüwechsel oder Neustart täuscht keinen neuen Gewinn vor. Die Option „Weniger Bewegung“ reduziert die Effekte.

Beim Drehen wird die logische Mindestgröße an der **kürzeren Bildschirmseite** ausgerichtet. Das Seitenverhältnis bleibt erhalten; vorübergehend veraltete Android-Safe-Area-Rechtecke werden verworfen und das Layout nach dem Größenwechsel erneut berechnet. Aufgaben und Antworten bleiben während der Drehung erhalten. Tests drehen dieselbe laufende Aufgabe mehrfach; echte Geräteeigenschaften bleiben separat zu prüfen.

## Sprache und Lob

Die App verwendet eigenständige synthetische Stimmen: **Deutsch Kerstin (weiblich), Englisch LJSpeech (weiblich), Russisch Denis (männlich)**. Kate Beckinsales Stimme wird nicht geklont oder imitiert. Die vom Nutzer hochgeladene Aufnahme wurde nicht als TTS-Modell verwendet und gehört nicht zum Repository oder zur App.

Die Aussprachekorrektur behebt einen tatsächlich beobachteten Fehler: Der Lautgenerator zerlegte den deutschen „ich“-Laut in `c` und ein kombinierendes Zeichen; das Modell ließ letzteres aus. Unterstützte zusammengesetzte IPA-Zeichen werden jetzt korrekt zugeordnet. Unbekannte Laute führen bei der Erzeugung zu einem Fehler, statt still auszufallen. Alle aktuellen Aufnahmen wurden so erzeugt.

Zusätzlich: Sprechdauerfaktor 1,18, echte Satzpausen von 280 ms, 180 ms Vorlauf und 350 ms Nachlauf. Jeder erzeugte Audiosatz bleibt vollständig erhalten. Eine schnelle Antwort unterbricht den noch laufenden Auftrag nicht: Lob wartet auf dessen Ende. Weitere Antwortversuche ersetzen höchstens eine vorgemerkte Rückmeldung. Lautsprecher-Wiederholung und bewusste Navigation dürfen die vorherige Wiedergabe beenden.

Sechs Lobvarianten wechseln ohne direkte Wiederholung, unter anderem „Wunderbar!“, „Sehr klug entschieden!“ und „Super cool, das gefällt mir!“. Lob wird angezeigt und gesprochen; es gibt keine Strafe für Fehler. Die Varianten sind in allen drei Sprachen vorhanden.

Je Sprache sind **663 Clip-Zuordnungen** vorhanden: 320 Aufgaben, 320 Hilfen, acht Fächer, fünf Looks, sechs Lobvarianten und vier allgemeine Hinweise. Gleiche Texte teilen sich Dateien. Tatsächlich ausgeliefert werden **1.621 unterschiedliche Sprachdateien** (Deutsch 583, Englisch 519, Russisch 519). Die Aufnahmen und Modelle enthalten keine Laufzeit-Netzwerk- oder Mikrofonfunktion. [Sprachproben anhören](voice-previews/README.md).

## Musik und bestehende Inhalte

Die 320 Aufgaben in acht Fächern sowie Deutsch/Englisch/Russisch bleiben erhalten. Die ursprünglichen 24 Aufgaben und gespeicherten Lösungen werden unverändert übernommen. Inhaltliche Einordnung und offene fachliche Prüfung: [Beschreibung 0.6](subjects-family-v06.md).

Die Musikauswahl enthält jetzt **20 eigene Klavierwiedergaben** bekannter klassischer Notenquellen, rund 50 Minuten insgesamt. Eine kuratierte Auswahl, keine objektive Rangliste. Die Musik wechselt automatisch; Auswahl, Zufall und Wiederholung bleiben möglich. Zwei Titel sind ausdrücklich Themenauszüge. [Titel, Quellen und Lizenzen](music.md), [20 Hörproben](music-previews/README.md).

## Reproduzieren und Grenzen

```sh
python3 scripts/content/generate.py
# Metadaten aus vorhandenen, unveränderten PNG-Atlanten; nur Entwicklung:
# Voraussetzungen: Pillow, NumPy, SciPy
python3 scripts/graphics/compile_wardrobe.py
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/quest-render.sh /tmp/kinderwelt-bilder
```

Technische Tests belegen nicht automatisch, dass jedes Wort von Kindern verstanden wird. Hörabnahme durch Muttersprachler, Geräteinstallation, Drehung mit echten Safe-Areas, Bedienung durch Kinder und fachliche/pädagogische Evaluation bleiben offen. Es werden keine nachgewiesene Lernwirkung oder Google-Play-Uploadbereitschaft behauptet. [Tatsächliche Testergebnisse](test-report.md), [Android](android.md).
