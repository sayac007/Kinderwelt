# Architektur · Aufgabe 01

`core/main.tscn` startet den gemeinsamen UI-Runtime in `core/main.gd`.
Navigation, adaptive ein-/zweispaltige Hub-Ansicht, Replay, Hinweise,
Einstellungen und freiwillige Co-Play-Gesprächshilfe sind gemeinsam.
Die Scrollansicht hält alle Eingänge auch im schmalen Hochformat erreichbar.
`core/pictogram.gd` zeichnet fünf unterschiedliche, farbunabhängig erkennbare
Formen. `core/cues.gd` erzeugt kurze ausblendende Sinustöne ohne Assets oder Netz.

## Registrierung und Levelvertrag

`content/modules.json` registriert genau fünf eindeutige IDs mit deutschem Namen,
Piktogramm und `res://`-Levelpfad. `core/catalog.gd` lädt die Registrierung und
validiert die Fundament-Level: `schema: 1`, passende `module`-ID, positive
numerische `target`-Anzahl. Jede `games/<id>/foundation.json` ist eine isolierte,
austauschbare Content-Datei. Die fünf Demos teilen absichtlich den gleichen
Tap-Runtime; spezifische Lernmechaniken sind erst Aufgaben 02 und 03.

Runtime-Lebenszyklus: `open_module(entry)` lädt Content und setzt Fortschritt
zurück; `advance()` bearbeitet eine Aktion, `hint()` zeigt das Ziel, `instruct()`
wiederholt das Signal. Abschluss wird höchstens einmal pro Durchlauf gespeichert;
`hub()` und Wiederholung bleiben jederzeit erreichbar. Neue Mechaniken können
später eigene Szenen hinter diesem Navigationsvertrag registrieren.

`instruction` enthält eine deutsche Autorenbeschreibung; `narration: null` ist
ein ausdrücklich unbesetzter Slot für rechtmäßig aufgenommene Erzählung.
Aktuell werden keine Erzählaufnahmen oder TTS angeboten. Die Klangsignale
ersetzen keine Sprache. Piktogramm-Hervorhebung und Fortschrittspunkte zeigen
die Fundamenthandlung ohne erforderlichen Text. Eine Kind-Usability-Prüfung
wurde nicht durchgeführt.

## Zustand und Sicherheit

`core/save_store.gd` speichert ausschließlich unter `user://progress.json`:
Schema 1, abgeschlossene Modul-IDs, Stummschaltung und reduzierte Bewegung.
Schreiben über temporäre Datei mit anschließendem Rename; Schreibfehler werden
angezeigt. Beschädigte oder unbekannte Schema-Versionen fallen auf Defaults
zurück. Es gibt noch keine Migration aus älteren Schemas, keine Cloud, Namen,
Telemetrie oder Netzwerk-APIs. Tests verwenden eigene temporäre XDG-Verzeichnisse.
Co-Play ist eine optionale, nicht persistente Gesprächshilfe ohne exklusive
Steuerung oder zweiten Spieler. Reduzierte Bewegung unterbindet Hinweistweens.

`android/` enthält ausschließlich den Scope-Hinweis. Export-/Release-Konfiguration
ist bewusst Aufgabe 05 und wird hier nicht implementiert.

## Lizenzen

Neuer Quellcode, prozedurale Piktogramme und synthetische Töne in diesem Commit:
MIT, siehe LICENSE. Keine externen Grafiken, Musik oder Schriftdateien eingebunden.
Godots mitgelieferte Fonts und Engine behalten ihre jeweiligen Engine-Lizenzen.
Die ursprünglichen YAML-Spezifikationen bleiben unverändert.

# Erweiterung · Aufgabe 02

Die Abschnitte zum Tap-Runtime oben beschreiben weiterhin die drei unveränderten
Fundament-Demos. Für Logik und Mathematik registriert `content/modules.json`
zusätzlich `runtime` (GDScript-Control) und `levels` (JSON-Levelsammlung).
`core/main.gd` instanziert den registrierten Runtime im vorhandenen Scrollbereich.
`core/catalog.gd::levels(entry)` ist die gemeinsame Level-Ladeschnittstelle;
`core/learning_catalog.gd` prüft Schema, eindeutige IDs, drei Stufen mit mindestens
drei Aufgaben und modulspezifische Lösbarkeit. Kein Content wird aus dem Netz geladen.

`core/learning_game.gd` stellt Levelwahl, Wiederholung, Rückgängig, Bildanleitung,
dreistufige Hilfen und optionale Abschlussvorschläge bereit. `game.gd` unter jedem
Modul baut die eigene Oberfläche; `model.gd` implementiert Regeln unabhängig vom
SceneTree. `core/game_art.gd` zeichnet Holzsegmente, Figuren, Früchte, Umrisse und
Bedienpiktogramme. Alle neuen Darstellungen sind prozedural und unter der
bestehenden MIT-Lizenz verfügbar. Es gibt keine zusätzlichen Abhängigkeiten.

## Brücken

`games/logic/levels.json` enthält `schema: 1`, `module: "logic"` und `levels`.
Jeder Level hat eine eindeutige `id`, `tier` (1–3), `gaps` (Lückenlängen) und
`pieces` (einmal verfügbare Holzstücklängen). Ganzzahlige Längen liegen bei 1–6;
es sind bis zu vier Lücken und zwölf Stücke zugelassen. Die ausgelieferten neun
Aufgaben nutzen bis zu drei Lücken und acht Stücke. Teilstücke können beliebig
kombiniert werden; überschüssiges Material darf liegenbleiben. Der Validator
verlangt eine vollständige Lösung ohne Wiederverwendung eines Stücks.

Die Spielfigur steht vor der Lücke und wird auf der anderen Seite dargestellt,
sobald alle Felder dieser Lücke überbrückt sind. Bei aktivierter Bewegung
überquert sie die Brücke animiert; mit reduzierter Bewegung erscheint direkt
der Endzustand. Punkte und Segmentumrisse zeigen
Länge und Reststrecke ohne Ziffern. Zu lange Stücke bleiben im Vorrat und die
Lücke erhält ein Kreuz; kleine Teilstücke lassen sichtbar Wasser offen.
Backtracking sucht Hinweise, die vorhandene Entscheidungen erhalten. Ist eine
Entscheidung lokal passend, lässt aber keine Gesamtlösung mehr zu, zeigt die
Hand zuerst auf Rückgängig. Keine Sackgasse erfordert einen Neustart.

## Marktstand

`games/math/levels.json` nutzt dasselbe Sammlungsschema mit `module: "math"`.
Unterstützte Modi:

| `mode` | Zusätzliche Felder | Handlung |
| --- | --- | --- |
| `match` | ein `targets`-Korb, `items` | Sichtbare Umrisse mit passender Fruchtmenge füllen |
| `compare` | `counts` mit 2–3 Mengen | Den Korb mit der größten Menge wählen |
| `sort` | zwei `targets`, `items` | Äpfel und Birnen nach Form zuordnen |
| `share` | 2–3 gleich große `targets`, `items` | Früchte gleichmäßig an Figuren verteilen |

Ein Ziel ist `{ "count": 3, "kind": "apple" }`; Fruchtarten sind `apple`, `pear`
oder für frei gemischte Verteilung `any`. `items` zählt die tatsächlich verfügbaren
Einzelstücke auf. Mengen sind ganze Zahlen 1–10, der verteilbare Vorrat umfasst
höchstens zehn Früchte. Vergleichsaufgaben benötigen eine eindeutige größte Menge.
Freie Plätze bei `any` zeigen neutrale Kreise statt eines Apfelumrisses;
damit wird keine unzutreffende Sortenvorgabe signalisiert. Die Formen der
abgelegten Früchte bleiben erhalten. Falsche Form/Überfüllung wird
mit Umriss und Kreuz erklärt, ohne Fruchtverbrauch, Zeitdruck oder Strafe.

## Hilfen und Vorschläge

Die erste Hilfe zeigt per Hand/Fokus eine passende Quelle und ein Ziel, ohne den
Zustand zu verändern. Die zweite führt genau eine Platzierung (oder nötiges
Rückgängig) aus. Die dritte zeigt die verbleibenden Schritte nacheinander;
mit reduzierter Bewegung wird die Lösung direkt dargestellt. Ein Lösungsbeispiel
ist jederzeit durch eigene Aktion, Levelwechsel oder Hub-Rückkehr abbrechbar.
Session-IDs verhindern, dass ein alter Animationstimer einen neuen Level verändert.
Einzelentscheidungen im Vergleich können schon mit der zweiten Hilfe vollständig
gelöst sein. Bildanleitung und synthetische Töne bleiben jederzeit wiederholbar.
Es gibt keine Sprachaufnahmen; Ton, Bewegung und Lesen sind keine Voraussetzung
für die Steuerung. Verständlichkeit für Kinder wurde noch nicht empirisch geprüft.

`core/learning_progress.gd` ergänzt Schema-1-Saves optional um `learning` pro Modul:
`completed` (Level-ID-Map), `tier` (Vorschlagsstufe) und `recent` (maximal drei
verschiedene Abschlüsse mit Level-ID, Stufe und Hilfestatus). Alte Schema-1-Saves
bleiben gültig. Ungültiger optionaler Fortschritt fällt auf Defaults zurück;
JSON-Zahlen werden zur Laufzeit normalisiert. Zwei verschiedene unassistierte
Abschlüsse auf aktueller Stufe unter den drei letzten Abschlüssen erhöhen nur
die Vorschlagsstufe. Wiederholung ersetzt den bisherigen Eintrag derselben Aufgabe.
Fehler erzeugen keine Statistik und keine Herabstufung. Auch erledigte und höhere
Level bleiben frei auswählbar; der Erwachsenen-Reset entfernt alle Lernstände.

## Content hinzufügen

1. Neue Daten in der passenden `levels.json` ergänzen, eindeutige ID vergeben.
2. Modus-/Längenregeln oben einhalten und pro Stufe mindestens drei Level erhalten.
3. `GODOT=... bash tests/run.sh` ausführen. Der Loader muss die gesamte Sammlung
   akzeptieren; jeden neuen Level zusätzlich mit echten Eingaben und Bildern prüfen.
4. Instruktionen benötigen verständliche Bilder und ggf. rechtmäßige Narration.
   Keine Lernwirkung aus bestandenen Softwaretests ableiten.

Das Layout verwendet die tatsächliche Fenstergröße statt einer festen virtuellen
900-Pixel-Breite. Der Fokus folgt zwischen Vorrat und Ziel, wodurch auch kleinere
Hochformatfenster mit Scrollansicht bedienbar bleiben. Tests prüfen 360×800 und
1024×600; physische DPI, Bildschirmleser und Android-Geräte bleiben manuelle Checks.
