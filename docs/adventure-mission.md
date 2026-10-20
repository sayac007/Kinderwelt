# Kinderwelt 0.3: erster Adventure-Test

Diese Iteration liefert **eine Mission**, „Das geheimnisvolle Kraftwerk“. Grundlage ist
`origin/main` mit dem gemergten PR #6 (`e952200`). Branch: `feat/explorer-adventure-v03`.
Weitere Missionen und Änderungen an den anderen vier Lernbereichen sind ausdrücklich
zurückgestellt. Die bisherigen fünf Spiele mit ihren 36 Aufgaben bleiben erhalten.

## Ausprobieren

1. Android-Debug-APK aus dem verlinkten [Testbericht](adventure-test-report.md) installieren.
2. Oben im Hauptmenü **⚡ Picos Kraftwerk testen** wählen.
3. Einführung lesen oder mit „Los geht’s / Überspringen“ schließen. Standard ist **Tüftler**.
4. Boden antippen: Die Figur läuft dorthin. Maschine antippen: Die Figur geht hin und
   benutzt sie erst bei Ankunft. Die Kamera folgt der Figur. Alternativ funktionieren
   die Pfeiltasten; die großen unteren Tasten führen zu Raumtüren oder zum Pult.
5. Rechts liegt das Kraftwerk. Energiequellen und Schaltpult benutzen. „Wirkung ?“ erklärt
   den aktuellen Zustand. Hilfe, Pause und Rückkehr zur Kinderwelt sind jederzeit erreichbar.
6. Nach der Lösung bleibt das Tor mechanisch entriegelt. Rechts die Sternwarte betreten
   und das Teleskop antippen: Pico feiert die Entdeckung, die Musik wechselt.

Es gibt kein Zeitlimit, keine Leben und keine Strafe für Überlastung. Schalter können
beliebig zurückgestellt werden. Ein neuer Versuch oder ein Stufenwechsel benötigt eine
bewusste Auswahl; andere Spielstände werden dabei nicht gelöscht.

## Rätselregeln

| Quelle | Energie | Material | Wärme |
|---|---:|---:|---:|
| Sonne | 8 | 1 | 1 |
| Wind | 9 | 2 | 3 |
| Akku | 6 | 3 | 0 |

Relais (4) **und** Torleitung (8) müssen eingeschaltet sein. Die optionale Werkstattlampe
benötigt weitere 3 Energie. Die erzeugte Energie muss alle eingeschalteten Verbraucher
versorgen. Zu viel Material, Wärme oder Gesamtleistung löst die Schutzabschaltung aus.
Die Simulation ist ein bewusst vereinfachtes Ressourcenrätsel, kein Elektrotechnikmodell.

| Variante | Material maximal | Wärme maximal | Sicherung maximal | ungenutzte Energie maximal |
|---|---:|---:|---:|---:|
| Entdecker | 6 | 9 | 24 | unbegrenzt |
| Tüftler (Standard) | 5 | 4 | 18 | unbegrenzt |
| Meister | 5 | 3 | 15 | 3 |

**Lösungswege (für Begleitende; nicht vor dem ersten Versuch zeigen):**

- Sonne + Akku, Relais + Tor an, Lampe aus: 14 erzeugt, 12 benötigt, Material 4,
  Wärme 1, Rest 2. Gültig in allen drei Varianten; eine kühle, materialsparende Meisterlösung.
- Wind + Akku, Relais + Tor an: 15 erzeugt, Material 5, Wärme 3, Rest 3.
  Ebenfalls in allen Varianten gültig. Die Lampe kann zusätzlich eingeschaltet werden:
  dann wird die gesamte Energie genutzt. Das ist eine andere Optimierung als Material sparen.
- Sonne + Wind, Relais + Tor an: 17 Energie, Material 3, Wärme 4. Eine besonders
  materialsparende Tüftlerlösung, wegen Wärme und Sicherung in Meister ungültig.

Die Grenzen werden angezeigt, jede Änderung aktualisiert Zähler, Schalterzustand und
Diagnose. In der Welt zeigen Quelllampen, Verbraucherlampen, Stromfluss, Zahnrad und Tor
Zustandsänderungen; reduzierte Bewegung stoppt dekorative Bewegung und öffnet das Tor sofort.
Ob dies dem vorgesehenen spielerfahrenen Siebenjährigen **mehrere Minuten interessante
Herausforderung** bietet, muss erst der freiwillige Gerätetest zeigen.

## Architektur und Wiederverwendung

| Datei | Verantwortung |
|---|---|
| `games/adventure/power.gd` | Reine Simulation, Ressourcen, Varianten, Auswertung, validierter Zustand; ohne Welt verwendbar |
| `games/adventure/movement.gd` | Begrenzte Bewegung, Zielpunkt und Geschwindigkeit |
| `games/adventure/world.gd` | Raumgrafik, Kamera, Touch-Ziele, animierte Zustandsdarstellung |
| `games/adventure/game.gd` | Interaktionen, Oberflächen, Raumübergänge, Hilfe, Pause, Audioeinstellungen |
| `games/adventure/progress.gd` | Versionierter lokaler Zustand, geprüfter Lösungsnachweis, sichere Wiederaufnahme |
| `games/adventure/tracks.gd` | Erweiterbares Musikregister ohne Begrenzung auf zwei Einträge |
| `core/music.gd`, `core/cues.gd` | Bestehende Audioplayer, Überblendungen, Lautstärken, Stummschaltung, App-Unterbrechung |

Das Adventure verwendet ein eigenes Feld im vorhandenen lokalen Spielstand. Raum, Position,
Schalter und gültiger Tor-Nachweis werden bei Änderungen, Raumwechsel, App-Unterbrechung/Verlassen und
alle drei Sekunden gespeichert. Ungültige Daten öffnen keinen gesperrten Raum; ein Nachweis
aus einer anderen Stufe schaltet die neue Variante nicht frei. Unbekannte Felder beschädigen
die bisherigen Fortschritte nicht. System-Zurück führt zum Hauptmenü und speichert.

**Steuerungsentscheidung:** Tippen statt Bildschirm-Joystick vermeidet dauerhaft verdeckte
Fingerflächen und erlaubt große Interaktionsbereiche. Im Querformat steht die Navigation
seitlich. Die Welt selbst scrollt nicht per Wischgeste; nur die Kamera bewegt sich. Lange
Hilfetexte und Menüs dürfen auf kleinen/quer gehaltenen Geräten oder mit großer Schrift
vertikal scrollen; der Fokus wird mitgeführt. Android-Sicherheitsabstände verwenden dieselbe
Berechnung wie die bestehende Oberfläche. Echte Finger, Notches und Systemleisten sind
noch nicht auf einem Gerät überprüft.

## Musik und Grafik: tatsächlicher Stand

Zwei eigene elektronische Kompositionen mit Melodie, Bass, Akkorden, Arpeggios, Echo,
Kick, Snare und Hi-Hat sind als abspielbare WAV-Dateien enthalten:

- [Funkenflug](../assets/music/adventure/workshop.wav): 132 BPM, etwa 29 Sekunden.
- [Sternensprung](../assets/music/adventure/stars.wav): 146 BPM, etwa 26 Sekunden.

Eigene Motive und Synthese, keine fremden Aufnahmen, Nintendo-Melodien oder Samples.
Generator: `python3 scripts/compose-adventure.py`; Metadaten und SHA-256 stehen in
`assets/music/adventure/manifest.json`. Unter MIT wie der übrige eigene Code.
Das Register kann später mindestens zehn Titel aufnehmen; es existieren heute genau zwei
neue Titel, keine vorgetäuschten weiteren Stücke. Die fünf bisherigen Weltmusiken bleiben.
Musikwechsel über Pause oder Teleskop, getrennte Lautstärken, globales Stumm und bestehende
Überblendung. Die WAV-Grenzen sind kurz ausgeblendet; ein klanglich unauffälliger Loop und
angenehme Lautstärke auf dem Zieltelefon sind manuell zu prüfen.

Alle Figuren, Werkzeuge, Maschinen und Räume sind eigenständige, im Spiel gezeichnete
Vektorgrafiken. Die Screenshots zeigen die tatsächliche Godot-Ausgabe. Es handelt sich um
**Prototypgrafik und prozedurales Audio**. Professionelle Illustrationsqualität, moderne
Konsolenproduktion, motivierende Musik und gutes Spielgefühl sind nicht nachgewiesen.

## Freiwilliger erster Gerätetest

Zunächst eine erwachsene Person, dann optional das Kind; keine personenbezogenen Daten,
Aufnahmen oder automatischen Nutzungsdaten erfassen. Das Kind kann jederzeit aufhören.
Begleitung und Hinweise sind freiwillig. Den bisherigen Datenschutz-/Freigabeprozess nicht
als durch diesen Prototyp erledigt behandeln.

- Erwachsene: Installation, Flugmodus, lesbare Beschriftungen, große Trefferflächen,
  Tippen/Ankunft, alle Räume, alle drei Stufen, Zurück, Rotation, Systemleisten,
  App-Wechsel/Fortsetzen, vollständiges Beenden/Wiederstart, Stumm und beide Regler prüfen.
- Erst dann: Das Kind möglichst selbst Ziel und Bedienung entdecken lassen. Beobachten,
  ob Ursache und Wirkung verstanden werden, wo es hängen bleibt und ob es eine zweite
  Lösung ausprobieren möchte. Keine Lernwirkung aus einem Erfolg ableiten.
- Ohne Namen/Altersexaktdaten protokollieren: Gerätetyp/Android, reproduzierbare technische
  Probleme und allgemeine freiwillige Rückmeldung. Keine Datenerhebung über den technischen
  Test hinaus ohne gesonderte Entscheidung.

Der Debug-Schlüssel entsteht wie bisher außerhalb des Repositorys im isolierten Build.
Ein vorhandenes 0.2-APK kann eine andere Debug-Signatur haben. Ein Update kann dann
abgewiesen werden. **Nicht unbedacht deinstallieren: Dabei werden lokale Spielstände gelöscht.**
Für einen ersten Versuch möglichst ein separates Testgerät verwenden. Eine konsistente,
sicher außerhalb des Repositorys verwahrte Entwicklungssignatur ist vor dauerhaften
Update-/Migrationstests einzurichten. Es wurde kein Release-Schlüssel erzeugt oder verwendet.
