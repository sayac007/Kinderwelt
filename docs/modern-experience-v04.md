# Kinderwelt 0.4: gemeinsame Plattform und Pflanzenmission

Basis: `origin/main` mit PR #7 (`7735ba7`), neuer Branch
`feat/kinderwelt-modern-experience-v04`. Keine Änderungen direkt an `main`.
Die fünf bestehenden Bereiche und alle 36 Aufgaben bleiben erhalten. Die gemeinsame
Karte, Figuren, Musik und Sprache sind neu; die Bestandsaufgaben wurden fachlich nicht
neu geschrieben. Picos Kraftwerk bleibt ein optionaler Prototyp.

## Schnell ausprobieren

Die tatsächlichen APK-/AAB-Dateien und Ergebnisse stehen im [Prüfbericht](modern-test-report.md).
Oben auf der Karte führen **Figur**, **Musik**, **Klang** und **Eltern** direkt zu den
jeweiligen Ansichten. Die illustrierte Karte verbindet Brücken, Markt, Geschichten,
Werkstatt und Dorf. Ein sichtbarer Scrollbalken kennzeichnet den weiteren Kartenverlauf.
Orte lassen sich großflächig antippen; die Bezeichnung wird auf Deutsch vorgelesen.

In **Figur** stehen Mina, Leo, Sam und Jule mit verschiedenen Frisuren, Hauttönen,
Kleidung und Gesten zur Auswahl. Alle haben identische Lernmöglichkeiten. Die gewählte
Figur wird lokal gespeichert und begleitet die Pflanzenmission. Eine kurze Auswahlgeste,
ruhiges Atmen, Bewegung, Nachdenken und Erfolg verwenden dieselben gezeichneten Körperteile.
Die Vorschautaste wechselt zwischen Laufen und Denken; die Erfolgsgeste endet wieder.
Reduzierte Bewegung wird berücksichtigt.

**Die durstige Pflanze** ist über die Werkstatt und einen direkten Kartenknopf erreichbar:

- Ein Rohr **antippen**: um 90 Grad drehen.
- Ein Rohr **ziehen und loslassen**: mit einem anderen Platz tauschen, auch einem leeren.
- Alternativ **Legen** wählen, dann Rohr und Ziel antippen. Eine komplexe Geste ist nie nötig.
- Wasserhahn oder **Wasser** antippen: eine Gießportion testen. Verbundene Rohre füllen
  sich blau; wandernde Tropfen zeigen den Weg, offene Enden tropfen sichtbar.
- **Hören** wiederholt den gesprochenen Auftrag; **Stufe** öffnet Varianten, Hilfe und
  „Neu versuchen“. **Zurück** nimmt den letzten Spielzug zurück. **Karte** verlässt die Mission.

Die Figur tritt ins Bild, spricht den Auftrag über die gemeinsame Sprachwiedergabe,
und die Pflanze wächst bei einer gültigen Lösung. Nach Erfolg bleiben die Pflanzen auch
bei geschlossenem Hahn gewachsen. Ein geprüfter Lösungsnachweis speichert diesen Fortschritt.
„Neu versuchen“ setzt nur diese Variante zurück. Fehler kosten keine Leben oder Punkte.

## Drei fachliche Varianten, dieselbe Bedienung

| Stufe | Auftrag | Modellierte Wassermenge |
|---|---|---:|
| Einstieg | Eine Pflanze über zwei gerade Rohre versorgen | 20 Einheiten Reserve |
| Fortgeschritten | Pflanze und Vogelbad über eine Abzweigung verbinden | 8 Einheiten |
| Experte | Zwei Pflanzen mit je drei Tropfen versorgen, Lecks vermeiden | genau 6 Einheiten |

Die Simulation prüft echte, zueinander passende Rohranschlüsse. Norden/Osten/Süden/Westen
sind vier Bits; ein Ausgang ohne passenden Gegenanschluss ist ein Leck. Nur von der Quelle
erreichbare Rohre führen Wasser. Ziele benötigen 2 Einheiten im Einstieg, insgesamt 3 in
der mittleren Stufe, 6 in Experte. Jedes offene Ende verliert zwei Einheiten. Erfolg setzt
alle erreichbaren Ziele und ein ausreichendes Budget voraus. Die Zahlen beschreiben eine
vereinfachte **Gießportion**, keine zeitabhängige Flüssigkeitsphysik.

Damit kann eine Expertenverbindung beide Pflanzen erreichen und wegen eines zusätzlichen
leckenden T-Stücks trotzdem scheitern. Ein passendes gerades Rohr spart das Wasser.
Rohrformen und Inventar bleiben auch beim Verschieben erhalten. Feste Quelle und Ziele
lassen sich nicht versehentlich entfernen. Ein kurzer Fingerdrift bleibt ein Tippen,
eine längere Bewegung wird erst beim Loslassen zu einer Änderung; außerhalb wird abgebrochen.

Lösungsorientierungen für Erwachsene, Zellnummern zeilenweise ab 0 bei vier Spalten:

| Stufe | Erforderliche Anschlüsse, Quelle 4 und Ziele fest |
|---|---|
| Einstieg | Zellen 5 und 6: West–Ost |
| Fortgeschritten | 5: West–Ost; 6: West–Ost–Süd; 10: Nord–Süd |
| Experte | 5: West–Ost; 6: West–Nord–Süd; 2: Süd–Ost; 10: Nord–Süd; 14: Nord–Ost |

## Gemeinsame Sprache und Musik

Die neue Mission besitzt drei kurze deutsche Aufträge, eine Hilfe und einen Erfolgssatz
als **tatsächlich abspielbare Offline-Clips**. Sprachautomatik ist standardmäßig an und
abschaltbar. Der Wiederholen-Knopf funktioniert auch bei ausgeschalteter Automatik.
Globales Stumm und Sprachlautstärke null bleiben immer stumm. Musik wird während Sprache
um 13 dB abgesenkt und danach zurückgestellt. Sprache, Musik und Effekte haben getrennte,
persistente Regler. Sichtbarer Zusatztext ist optional; kurze Statushinweise bleiben.

Die Stimme ist ausdrücklich ein **synthetischer eSpeak-NG-Prototyp**. Dies steht auch in
den Einstellungen. Hochwertige natürliche Aufnahmen fehlen. Die Bestandsaufgaben erhalten
Ortsansagen, aber noch keine jeweils neu eingesprochenen 36 Aufgabenstellungen; sie sind
in dieser Iteration fachlich unverändert. [Audioherkunft und Grenzen](audio-v04.md).

Die Musikbox bietet zehn echte elektronische Miniaturen mit unterschiedlichen Melodien,
Tempi und Audioinhalten, illustrierte Cover, direkte Vorschau, vorher/nachher, Zufall und
Merkfunktion. Die Auswahl wird gespeichert. Ohne Merken wechseln passende Situationen
auf thematische Musik; mit Merken bleibt der gewählte Titel. Die zwei Originale aus 0.3
bleiben erhalten, acht weitere eigene Kompositionen ergänzen sie. Vorbis-Clips werden
bei Bedarf geladen; zwei Musikplayer ermöglichen Übergänge, nicht zehn gleichzeitig.

## Austauschbare Komponenten

| Verantwortung | Dateien |
|---|---|
| Navigation und bestehende Module | `core/main.gd`, `core/modern/map.gd`, `place_art.gd` |
| Gemeinsame Gestaltung, originale Symbole | `core/design.gd`, `core/modern/icons.gd`, `assets/icons/ui/` |
| Wiederverwendbare Kinderfigur und Posen | `core/modern/hero.tscn`, `hero.gd` |
| Reine Lern-/Wasserlogik und validierte Zustände | `games/water/model.gd` |
| Touch-Transaktion ohne Szenenabhängigkeit | `games/water/gesture.gd` |
| Gartendarstellung und Wachstumsanimation | `games/water/board.gd` |
| Mission, Varianten, Hilfe und Fortschritt | `games/water/game.gd` |
| Narration, Lautstärke und Ducking | `core/modern/narration.gd`, `core/music.gd`, `core/cues.gd` |
| Musikregister, Auswahl und Cover | `core/modern/tracks.gd`, `musicbox.gd`, `cover.gd` |
| Bestehender atomarer lokaler Speicher | `core/save_store.gd` |

Alte Spielstände erhalten sichere Vorgaben für neue Felder. Figuren-ID, Musikoptionen,
Sprachoptionen, Rohrzustände und stufengerechte Lösungsnachweise bleiben lokal. Ein
beschädigter oder fremder Lösungsnachweis schaltet keinen Erfolg frei. Ein unveränderter
reiner Rohrgraph lässt sich später in einer anderen Ansicht weiterverwenden.

Die normalen Spiele besitzen keine virtuellen Bewegungspfeile. Auch Picos untere
Raumpfeile wurden durch Bauplan/Pult/Pico ersetzt; dort bleiben Tap-to-move, echte Türen
und die bestehende Bewegungslogik erhalten. Die neue Referenzmission benötigt keine
begehbare Adventure-Welt. Sie benutzt die vorhandene Android-DPI- und Safe-Area-Abbildung.
Nur Karte, Auswahl und längere Menüs scrollen; das Rohrfeld selbst nicht.

## Was die Umsetzung nicht nachweist

Die neue Bildsprache ist originale prozedurale 2D-Comicgrafik mit wiederverwendbaren
Körperteilen und Vektorsymbolen. Eine professionelle Art-Direction-Abnahme, natürliches
Sprechertalent und Konsolen-Musikproduktion sind nicht erreicht oder durch Automatisierung
nachgewiesen. Ob Erstklässler die Aufgaben, Symbole und Gesten verstehen und motiviert
bleiben, entscheidet erst der [freiwillige Gerätetest](modern-device-checklist.md).
