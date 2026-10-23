# Kinderwelt 0.8.0 – sieben Welten pro Fach

> Historischer Versionsbericht. Aktuelle Funktionen, Tests und offene Freigaben: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die folgenden Ergebnisse gelten ausschließlich für den genannten früheren Stand.

Jedes der acht Fächer speichert eine eigene frei wählbare Kulisse. Über Zahnrad → „Kulisse wählen“ öffnet sich die bebilderte Auswahl; dieselbe Auswahl bleibt in den Einstellungen erreichbar. Acht große Bildschaltflächen bieten sieben feste Welten und automatischen Wechsel. Beschriftungen, zugängliche Namen und neue gesprochene Hinweise sind in DE/EN/RU vorhanden.

## Spielbare Welten

- **Kletterbaum:** Aufgaben stecken in Nüssen neben Eichhörnchen auf Ästen. Die gewählte Figur klettert tatsächlich entlang eines vertikalen Weges und erreicht den Ast. Kamera und Berührungseingabe folgen der vertikalen Achse; beim Aufstieg wandert der Ausschnitt Richtung Baumkrone. Herunterziehen zeigt höhere Äste.
- **Meeresgrund:** Antippbare Truhen mit Aufgabenbildern, Schiffwracks, Fische und Schildkröten mit unabhängigen Bewegungen sowie aufsteigende Luftblasen. Die Figur schwimmt mit geneigtem Körper und sanfter Bewegung zur Fundstelle.
- **Stadt:** Der ausgewählte Charakter bleibt als Fahrer sichtbar. Das Auto fährt zu Aufgabenbildern an einer Haltestelle, unter einem Brückenbogen oder an einem Haus; die Räder drehen sich. Straße und Stationen scrollen unabhängig von der gemalten Kulisse.
- **Mond:** Aufgaben an Mondstationen, passende Kraterlandschaft und niedrige, langsamere Sprungbewegung statt normalem Lauf.

Berge, Zuhause und Schloss bleiben vorhanden. Jede Welt öffnet die ursprünglichen Aufgaben des gewählten Fachs; alle 320 Aufgaben, sieben Figuren, fünf Looks, 20 Musikstücke und drei Sprachen bleiben erhalten. Keine zusätzliche Belohnung für wiederholte Lösungen.

## Technik, Daten und Größe

`core/quest/scenery.gd` definiert Auswahl, Atlasregionen und Auflösung; `games/quest/world.gd` projiziert den Weg auf die jeweilige Bewegungsachse. `world_props.gd` zeichnet wiederverwendete Gegenstände, `vehicle.gd` die kleine Autoebene vor dem Fahrer. Alle Weltinhalte sind auf den Spielbereich begrenzt, damit sie Punktestand und Menüs nicht überzeichnen.

Lokales Speicherschema 4 übernimmt die frühere globale Kulisse als Anfangswert **jedes** Fachs. Bekannte Aufgaben, Figuren und Kleidung bleiben unverändert. Neue Fächerwerte werden anhand der zugelassenen IDs geprüft. Die globale Altangabe dient ausschließlich der Migration; die aktuelle Wahl steht in `subject_sceneries`.

Für die vier neuen Kulissen kommt **eine** gemeinsam verwendete, ursprünglich generierte PNG-Textur hinzu. Herkunft, Hash und 4-MiB-Quelldateibudget stehen in `art/adventure-worlds.json`; der Test schützt dieses Budget. Bewegte Tiere verwenden vorhandene Grafiken. Auto, Nüsse, Äste, Truhen und Mondstationen brauchen keine Animationsvideos oder Bildfolgen. Das Quelldateibudget ist keine Aussage über APK- oder installierte Größe; tatsächliche APK-/AAB-Größen stehen im [Testbericht](test-report.md).

„Weniger Bewegung“ hält Fische, Blasen, Eichhörnchen, Geister, Autoräder, Körperneigung und dekorative Sprünge still. Notwendige Fortbewegung und Auswahl bleiben spielbar. Zwischen Aufgaben kann entlang des Weges mit Touch oder Maus gezogen werden. Hoch-/Querformat und hohe Pixeldichte werden weiterhin durch die vorhandene Layoutlogik behandelt.

## Neue Prüfungen

`tests/worlds.gd` prüft Migration und ungültige Eingaben, getrennte Fachwerte auf Datenträger, Atlasregionen, echte Auswahl per Berührung, Reisen zur ersten Aufgabe in allen sieben Welten auf vier Anzeigeprofilen, Erreichbarkeit sämtlicher 40 Mathe-Stationen je Welt und Profil sowie vertikale Kamera, Auto, Schwimmen und reduzierte Bewegung. Die Aufgabenlogik aller acht Fächer bleibt zusätzlich in der bisherigen Suite geprüft.

`tests/qa/world_speech.gd` erfasst die tatsächliche Audiobusfolge aus Fachansage und Welthinweis in vier Welt-/Sprachkombinationen. Die bisherigen Fachansageprüfungen verwenden ausdrücklich die Bergkulisse, damit beide Fälle unabhängig bleiben; ihr Zeitlimit wurde nicht angehoben. Die vollständige Decodierung schützt alle zwölf neuen Clips und die bisherigen Sprachdateien.

Die neuen Hinweise wurden nach einem ersten unabhängigen ASR-Screening verkürzt und vereinfacht. Berichte enthalten Referenz und tatsächliche Erkennung; bessere Zeichenwerte ersetzen keine menschliche Hörprüfung. Die Offline-Hörseite enthält nun 54 Proben einschließlich aller neuen Welthinweise.

## Manuell offen

Auf einem Android-Gerät: Kulisse für zwei Fächer unterschiedlich wählen, App beenden/öffnen, Baum mehrere Äste hochklettern, sämtliche vier Seiten erreichen, an der Brücke und einer Truhe Aufgaben lösen, während Welt und Aufgabe drehen, Audio-Unterbrechung/Resume, reduzierte Bewegung und Lesbarkeit/Bedienung auf kleinen Displays prüfen. Reale Bildrate, Akkubelastung und installierter Speicherbedarf wurden nicht gemessen. Muttersprachliche Hörprüfung und freiwillige Kinderbeobachtung sind offen. Keine Aussage über empirische Lernwirkung oder Play-Freigabe.
