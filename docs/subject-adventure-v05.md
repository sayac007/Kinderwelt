# Kinderwelt: Mathe, Deutsch und Logik

## Spielen

Beim ersten Start erscheinen vier große Figuren. Antippen löst einen farbigen Schimmer, einen kurzen Farbwechsel, Sterne und kleine Blitze aus. „Los geht’s“ öffnet die Spielwelt. Ein Schild antippen: Die Figur läuft dorthin, dann öffnet sich die Aufgabe. Freie Wege können ebenfalls angetippt werden. Wischen verschiebt den sichtbaren Weg. Die drei Fachbereiche sind direkt am unteren Rand erreichbar.

Aufgaben werden gesprochen und im Bild gezeigt. Der Lautsprecher wiederholt den Auftrag; „Zeig mal“ gibt eine visuelle und gesprochene Hilfe. Fehler kosten nichts. Ein erstmaliger Erfolg bringt einen Stern und zehn Punkte; Wiederholungen erhöhen den Zähler nicht. Danach jubelt die gewählte Figur. Anschließend wird der nächste Wegabschnitt sichtbar. Alle Aufgaben sind ohne künstliche Wartezeiten zugänglich.

Die Zahnrad-Schaltfläche öffnet Figurenauswahl, Musikbox und Einstellungen. Musik, Effekte und Sprache haben getrennte Lautstärken. Automatisches Vorlesen und Bewegung lassen sich abschalten. Ein begleitender Erwachsener ist freiwillig. Spielstände sind lokal und können nach Bestätigung gelöscht werden.

## Eigene Aufgaben

| Bereich | Acht Aufgaben |
|---|---|
| Mathe | Sechs Äpfel zählen; 3 + 2; 7 − 3; vier bis zehn ergänzen; fünf und sieben vergleichen; 2–4–6 fortsetzen; 10 + 4; fünf bis acht ergänzen |
| Deutsch | Anfangsbuchstaben von Sonne, Maus, Apfel und Fisch; Haus–Maus reimen; Ro-bo-ter und Blu-me in Silben gliedern; BALL dem Bild zuordnen |
| Logik | Drei Bildmuster fortsetzen; zwei Gegenstände nach Kategorie ausschließen; Baum und Roboter ihren Schatten zuordnen; den größten Baum erkennen |

Dies sind eigenständig formulierte Aufgaben. Öffentliches Sofatutor-Material konnte in dieser Umgebung **nicht eingesehen** werden: direkte Aufrufe, Suchmaschinen, Google Play und ein alternativer Lesedienst lieferten HTTP 403. Daher wird weder die Übernahme konkreter Sofatutor-Aufgaben noch eine durchgeführte visuelle Anbieteranalyse behauptet. Ein fachlicher Abgleich mit frei zugänglichen Beispielen bleibt offen.

## Architektur und Medien

- `core/quest/main.gd`: eigenständiger Einstieg, Navigation und Einstellungen.
- `games/quest/progress.gd`: Aufgabenregister, Antwortprüfung und einmalige Belohnungen.
- `games/quest/world.gd`: direkte Bewegung, Kamera und Stationen.
- `games/quest/task.gd`, `picture.gd`, `choice.gd`: Aufgabe, konkrete Gegenstände und Antworten.
- `core/quest/hero.gd`: vier eigenständige gerenderte 2D-Sprites im gewünschten 3D-Comicstil. Körperteile werden im Godot-Canvas bewegt; es sind keine riggbaren 3D-Modelle. Die Figuren sind vollständig offline verfügbar.
- `core/quest/narration.gd`, `core/music.gd`: ein Sprachplayer und höchstens zwei Musikplayer. Sprache senkt Musik um 13 dB. Keine Laufzeit-Sprachsynthese und keine Mikrofonaufnahme.
- `core/save_store.gd`: Schema 2, explizit erlaubte Einstellungen und bekannte gelöste Aufgaben; atomisches Schreiben. Keine Namen, Altersangaben oder Beobachtungsprotokolle.

Figuren, Kulisse, Objekte, Symbole und App-Icon wurden für diese App erzeugt. Die Bildreferenzen des Nutzers dienten als Stilrichtung; keine fremden Figuren oder Marken sind übernommen. Nunito ist unter SIL Open Font License eingebunden (`assets/quest/OFL.txt`). Die zehn Musikstücke sind eigene synthetische Kinderwelt-Kompositionen; Dateihashes stehen in `assets/music/manifest.json`.

52 deutsche Sprachclips wurden mit **Piper 1.4.2**, `de_DE-thorsten-medium`, Länge 1,08 und Lautstärke 0,8 erzeugt und als Mono-Vorbis mit 22.050 Hz gespeichert. Eine Lautstärkereserve verhindert übersteuerte Codec-Spitzen. Die Modellkarte nennt CC0 für den Thorsten-Datensatz. Modell, Synthesewerkzeug und Wörterbücher werden nicht mit der App ausgeliefert. Hörverständlichkeit, Aussprache der Anlaute und Silben sowie das subjektive Klangbild müssen Menschen prüfen.

Quelle des Modells: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-medium.tar.bz2

Archiv-SHA256: `50487d9c95fdf2191f31d2588569381063ba1591dcd4c7d4bdd30f12b2191714`.
Modell-SHA256: `2d98b40baac55e4206f64114110a3474807e26440b80d465cd202af1e95be5e0`.

Neuerzeugung nach geprüftem Download und Entpacken, in einer separaten Python-Umgebung mit `piper-tts==1.4.2` und FFmpeg:

```sh
python scripts/generate-quest-voice.py --model /pfad/de_DE-thorsten-medium.onnx
```

Die Synthese kann zwischen Läufen abweichen. Das Android-Build verwendet die eingecheckten, durch Hashes geprüften Clips und benötigt das Modell nicht.

## Offene menschliche Prüfungen

Zuerst prüft ein Erwachsener Installation, Lautstärken, sämtliche Sprachclips, Touch-Ziele, Bildschirmdrehung, Unterbrechung und Fortsetzen auf einem echten Gerät. Besonders auf Nahtstellen der Sprite-Bewegung, Bildwiederholrate und Lesbarkeit achten. Anschließend kann ein Kind freiwillig wenige Aufgaben ausprobieren: Findet es Figurenauswahl, Weg, Hilfe und Fachwechsel selbst? Ein Abbruch ist jederzeit möglich. Keine Namen, Stimmen, Fotos oder personenbezogenen Beobachtungsdaten erfassen. Eine systematische Studie braucht eine gesonderte Schutz- und Einwilligungsentscheidung.

Die Aufgaben sind ein pädagogischer Entwurf. Weder Lerntransfer noch eine den führenden Play-Spielen vergleichbare Attraktivität oder Marktreife sind empirisch belegt.
