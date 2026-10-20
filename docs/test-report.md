# Ausgeführte Prüfungen für Kinderwelt 0.6

Stand: 20. Oktober 2026. Wanja ist fünfter spielbarer Familiencharakter und Hauptheld. Die App enthält 320 Aufgaben, acht Fächer, drei Bedienungssprachen und vier klassische Klavierwiedergaben.

## Tatsächlich ausgeführt

- **4.914 Godot-Prüfungen bestanden**, darunter die ursprünglichen 24 Lösungsfixtures, richtige/falsche Antworten aller 320 Aufgaben, einmalige Sterne, gespeicherte Fortschritte und Figurenmigration, tatsächliche Touch-Eingaben in alle acht Fächer, alle vier Wege jedes Fachs, fünf Bildschirmformate einschließlich simulierter hoher Dichte, Hilfen und Musiksteuerung. Alle 960 lokalisierten Aufgaben wurden auf 320 × 568 bei großer Schrift auf abgeschnittene Titel und Überschneidungen geprüft.
- **29 Python-Tests bestanden**: Inhaltsgenerator-Reproduzierbarkeit, ursprüngliche Aufgaben unverändert, Übersetzungs- und Grafikverträge, Musik-/Noten-/Audiohashes, tatsächliche PCM-Dekodierung aller **1.589 unterschiedlichen Sprachdateien** und vier Musikstücke, Dauer und Pegel, Exportfehler-Diagnose, negative Android-Manifest-/Payload-/ELF-Fälle sowie Größenanalyse.
- Regulärer und cachefreier Start der erlaubten App-Dateien jeweils über 60 Frames bestanden; geordnetes Beenden der Audio-Wiedergabe.
- 272 tatsächliche OpenGL-Renderings: ursprüngliche 24 Aufgaben, 15 Sachaufgaben-Stichproben, acht Welten, letzte Wegseite, drei Sprachen, fünf Figuren in vier Animationszuständen sowie Musik und Einstellungen auf vier Anzeigeprofilen. Nach einer Layoutkorrektur wird die endgültige Bildserie erneut erzeugt.
- Begrenzter Quell-/Berechtigungsaudit: keine Laufzeit-Netzwerkaufrufe oder aktivierten Android-Berechtigungen gefunden. Keine Sicherheitszertifizierung.

APK-/AAB-Exporte für Version **0.6.0 / 6** werden aus diesem Stand separat erstellt; Ergebnisse und Dateihashes werden nach dem tatsächlichen Export ergänzt. Frühere 0.5-Dateien sind keine Lieferung dieses Stands.

## Offene manuelle und empirische Prüfungen

Echte Android-Installation, physische Touch-/Swipe-Eingaben und Safe-Areas, Geräteperformance, Audiopegel und Sprachverständlichkeit bleiben offen. Deutsch/Englisch sind weibliche synthetische Stimmen; die lizenzierte russische Stimme ist männlich. Deutsche Lernwörter folgen bei englischer/russischer Bedienung als eigene deutsche Aufnahme. Hörprüfung dieser Abfolge und Ausspracheprüfung durch Muttersprachler stehen aus.

Fachliche/altersspezifische Abnahme der neuen Sachaufgaben, Lehrplanabgleich anhand der hier gesperrten Primärseiten und Test mit Kindern/Erwachsenen bleiben offen. Es wurden keine Kinder untersucht oder personenbezogenen Nutzungsdaten erhoben. Technische Tests belegen keine Lernwirkung, pädagogische Wirksamkeit oder Marktreife. YouTube-Titelzuordnung und eine SKIBIDI-Nutzungslizenz fehlen; das Original ist nicht enthalten. Release-Schlüssel, Store-Freigaben und Google-Play-Upload bleiben offen.
