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
