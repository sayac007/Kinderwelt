# Sprache, Selbstständigkeit und Dorf · Aufgabe 03

Alle fünf Bereiche im Hub sind jetzt eigenständige Spiele. Die neuen drei
Bereiche enthalten jeweils sechs frei wählbare Szenarien. Es gibt keine Fristen,
verlorenen Leben, Zwang zur Erwachsenenbeteiligung oder gesperrten Folgestufen.
Die bisherigen Brücken- und Marktspiele einschließlich ihrer lokalen Fortschritte
bleiben erhalten. Aufgaben 04 und 05 wurden nicht umgesetzt.

## Spielen

**Bildergeschichte:** Eine kurze Folge aus Bildern und synthetischen Klängen
zeigt die Geschichte. Die Pfeile blättern auch ohne Zeitdruck einzeln vor/zurück.
Das Wiederholungssymbol startet die Folge erneut; eine eigene Aktion beendet
sie sofort. Ein Bild im Vorrat und danach einen Platz antippen. Die Platzfolge
ist durch Mengenpunkte gekennzeichnet. Bereits gelegte Bilder lassen sich durch
Antippen wieder herausnehmen. Auch eine andere Reihenfolge ist zunächst erlaubt;
wenn sie nicht zu einer hinterlegten Geschichte passt, bleibt alles veränderbar.
Es gibt sechs Geschichten mit 3–5 Karten: Samen, Brot, Regen, Drachen, Malen,
Picknick. Deutsche Kartentexte sind zusätzliche Tooltips, keine Eingabeanforderung.

**Entdeckerwerkstatt:** Die Fahne zeigt das Zielbild. Große Bildschalter ändern
zwei Eigenschaften; der Dreieckspfeil probiert die Einstellung aus und zeigt das
Ergebnis. Rückgängig nimmt auch einen Versuch zurück. Man kann nach einem
passenden Ergebnis weiter experimentieren. Die sechs Modelle sind Kugelbahn
(Höhe/Oberfläche), Licht (Richtung/Blende), Wasser (Kanal/Ventil), Wind
(Segel/Windstärke), Waage (Steine auf beiden Seiten) und Garten (Wasser/Licht).
Mehrere Einstellungen sind erlaubt; etwa bei Waage, Garten und Kugelbahn führen
mehrere Kombinationen zum Ziel. Diese bewusst einfachen Spielregeln sind keine
naturwissenschaftlich exakten Simulationen und keine Pflegeanleitung.

**Gemeinsames Dorf:** Zwei neutrale Figuren sind durch unterschiedliche
Kopfbedeckungsformen erkennbar. Ihre Wunschbilder stehen oben; jede große
Ideenkarte zeigt eine mögliche Verteilung beziehungsweise Vereinbarung. Nach
einem Tipp werden die berücksichtigten Bedürfnisse ausgefüllt; Umrisse zeigen
noch offene Bedürfnisse. Jede Idee kann ausprobiert und zurückgenommen werden,
auch nach einem passenden Ergebnis. Die Figuren bleiben freundlich; es gibt
keine moralischen Punkte oder beschämende Fehlermeldung. Die sechs Szenarien
behandeln Ruhe/Musik, Sonne/Schatten, unterschiedliche Baumaterialmengen,
Werkzeuge, verschiedene Früchte und Platz für Pause/Spiel. Wo möglich sind
mehrere passende Ideen hinterlegt. Die Daten beschreiben diese vereinfachte
Spielwelt, kein allgemeingültiges Urteil über soziale Situationen.

**Gemeinsame Bedienung:** Haus = Hub, Raster = freie Szenarienwahl, runder Pfeil
oben = Neustart, Rückpfeil unten = einen Schritt zurück, Note = wiederholen,
Hand = Hilfe. Die Hilfestufen zeigen zunächst Quelle/Ziel, machen dann einen
Schritt vor und zeigen schließlich die Lösung schrittweise. Eigene Aktionen,
Neustart und Verlassen brechen ein Beispiel ab. Mit reduzierter Bewegung wird
es ohne Zwischentweens ausgeführt. Die Geschichten lassen sich unabhängig vom
automatischen Replay per Pfeil in eigenem Tempo ansehen.

Zwei Figuren mit Sprechblase öffnen **freiwillige Gesprächsimpulse**. Sie benötigen
kein zweites Konto, keinen Erwachsenen-Tastendruck und keine Bestätigung für
den Abschluss. Das Spiel bleibt bei sichtbarem Impuls vollständig bedienbar.
Der Schalter ist zugänglich, aber keine kindersichere Zugangssperre. Alle neuen
Bereiche speichern nur lokal entdeckte Szenarien, keine Entscheidungen oder
Angaben zu Personen. Angefangene Anordnungen/Versuche bleiben Sitzungszustand;
beim erneuten Öffnen kann jedes Bild direkt neu gewählt werden. Das bekannte
Erwachsenen-Reset entfernt auch die neuen Abschlussmarkierungen.

## Architektur und Datenvertrag

`content/modules.json` registriert `runtime`, `levels` und `name_key` für die drei
Bereiche. `core/learning_catalog.gd` delegiert ihre Prüfung an
`core/scenario_catalog.gd`; die Validatoren der Brücken/Marktspiele bleiben
unverändert. Eine ungültige Sammlung wird nicht teilweise geladen.

`core/scenario_game.gd` erweitert den bestehenden `learning_game.gd` um eine
freie Szenarienwahl ohne Rangstufen, freiwillige Impulse und unterbrechbare
Bild-/Klangfolgen. Die gemeinsame Art-Fabrik lässt bisherige Grafiken unverändert;
`core/scenario_art.gd` ergänzt eigene, prozedurale Szenen. `game.gd` und `model.gd`
je Modul trennen Oberfläche und Spielregeln wie bei Aufgabe 02. Rückgängig nutzt
lokale Zustandsschnappschüsse. Session-IDs verhindern, dass ältere Replay- oder
Beispiel-Timer einen neu gestarteten Durchlauf verändern.

Die optionalen Schema-1-Spielstände `learning.<module>.completed` verwenden die
vorhandene Speicherung. Die neuen Bereiche führen keine Schwierigkeitserhöhung,
Erfolgsserie oder moralische Bewertung ein. Logik-/Mathematik-Vorschläge bleiben
von ihnen getrennt. Bestehende Spielstände sind weiter lesbar.

Jede Datei `games/<module>/levels.json` enthält:

```json
{"schema": 1, "module": "language", "levels": []}
```

`levels` braucht mindestens sechs Einträge, jeweils mit eindeutiger Zeichenketten-
`id`, existierenden `title_key`/`prompt_key` und `narration: null`.
Die neuen Sammlungen benötigen keine `tier`-Felder. Alle Szenarien sind offen.

### Bildergeschichte

- `cards`: 3–5 Karten mit eindeutigen `id`, `scene`, ganzzahligem `step` 0–4,
  `cue` 0–7, vorhandenem `caption_key` und `narration: null`.
- `scene`: `garden`, `bread`, `rain`, `kite`, `paint` oder `picnic`; `step`
  bezeichnet die in `scenario_art.gd` gezeichnete Phase. Die mitgelieferten
  Geschichten nutzen nur die tatsächlich verschiedenen Phasen des jeweiligen
  Motivs. Zusätzliche Motive benötigen eigene Zeichnungen.
- `tray`: eine Permutation der Karten-IDs für den anfänglichen Vorrat.
- `orders`: eine oder mehrere vollständige Permutationen der IDs. Hier können
  mehrere nachvollziehbare Geschichten akzeptiert werden; Hinweise bevorzugen
  eine Reihenfolge, die bereits gelegte Karten erhält. Passt keine, zeigt die
  Hilfe zunächst Rückgängig. Andere Reihenfolgen werden nicht bestraft.

### Experimente

`experiment` ist eines der sechs oben genannten Modelle (`ramp`, `light`,
`water`, `wind`, `balance`, `garden`). `initial` enthält zwei gültige Einstellungen;
`goal` muss im vollständigen Zustandsraum erreichbar sein.

| Modell | Einstellungen | Ergebnisregel |
| --- | --- | --- |
| `ramp` | Höhe 0–3, rau 0–1 | max(0, 2 × Höhe − 2 × rau) |
| `light` | Richtung 0–2, Blende 0–1 | Pflanze erreicht bei Richtung 2 und offener Blende |
| `water` | Kanal 0–2, Ventil 0–1 | Pflanze erreicht bei Kanal 1 und offenem Ventil |
| `wind` | Segel 0–2, Wind 0–2 | Weg = Segel × Wind |
| `balance` | links/rechts je 0–3 Steine | Gleichgewicht bei gleicher positiver Menge |
| `garden` | Wasser/Licht je 0–2 | Blüte bei Wasser 1 und mindestens Licht 1 |

Ergebnis 1 bedeutet bei den vier Ja/Nein-Modellen „Zielbild erreicht“, 0 zeigt
noch einen anderen Zustand. Ohne gedrückten Versuchspfeil gilt kein Experiment
als abgeschlossen. Der Validator und die Tests prüfen alle möglichen
Einstellungen; ein Hinweis verändert bevorzugt möglichst wenig am eigenen Versuch.

### Dorf

- `people`: genau zwei Einträge mit `needs`, einer Mengen-Map.
- `stock`: verfügbare Mengen; alle Ideen müssen dieses Budget einhalten.
- `choices`: 2–4 Ideen mit eindeutiger `id`, `caption_key`, `narration: null`
  und `gives`, zwei Mengen-Maps in derselben Figurenreihenfolge.
- Symbolschlüssel: `quiet`, `music`, `sun`, `shade`, `blocks`, `tool`, `water`,
  `apple`, `pear`, `space`, `play`; Mengen ganzzahlig 1–6, pro Map höchstens drei
  Symbolarten. Leere Zuteilungen sind erlaubt.
- Mindestens eine Idee muss die hinterlegten Bedürfnisse beider Figuren decken.
  Umverteilung und alternative Ideen sind jederzeit möglich. Es gibt weder
  Emotionserkennung noch eine Bewertung realer Kinder oder Familien.

Ideen-IDs können zusätzliche, rein visuelle Details auslösen, etwa Kopfhörer,
Raumtrennung oder einen gemeinsamen Teller. Neue Details gehören in
`scenario_art.gd::plan_detail`; die Lösbarkeitsprüfung verwendet die Datenmengen,
nicht den Namen der Idee.

### Lokalisierung, Audio und rechtmäßige Inhalte

Alle neuen Oberflächen-, Karten- und Impulstexte stehen unter stabilen Schlüsseln
in `content/locales/de.json`. Deutsch ist Standard; fehlende Übersetzungen fallen
auf Deutsch zurück. `Localization.set_locale("en")` kann später eine
`content/locales/en.json` verwenden; eine englische Übersetzung wird noch nicht
mitgeliefert. Die vorhandenen Texte aus Aufgaben 01/02 wurden nicht im Rahmen
dieser Erweiterung vollständig umgestellt.

Die Geschichten verwenden lokal erzeugte kurze Töne zusammen mit Bildwechseln.
**Es gibt keine Sprachausgabe oder Sprachaufnahme.** Töne alleine erzählen nicht
den semantischen Inhalt; die Bildfolge trägt ihn. Die vorhandenen `narration: null`-
Slots markieren geplante Aufnahmen für Geschichte, Karte und Dorfidee. Aktuell
akzeptiert der Validator nur leere Slots. Für spätere Aufnahmen müssen Rechte,
Sprecher-Einwilligung, Sprachversion, Abspielpfad und Fehlerbehandlung verlässlich
geklärt und die Unterstützung gesondert implementiert werden. Keine externen
Aufnahmen, TTS-Dienste, zusätzlichen Pakete oder Laufzeit-Netzwerkzugriffe wurden
hinzugefügt. Grafiken und Synthesetöne sind eigener Code unter der Repository-Lizenz.

## Neue Inhalte prüfen

1. Daten und zugehörige deutsche Textschlüssel ergänzen, eindeutige IDs erhalten.
2. Passende Grafiken und gegebenenfalls mehrere erlaubte Geschichten/Ideen wählen.
3. `GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh`
   ausführen. Für neu hinzugefügte Motive/Regeln auch Tests erweitern.
4. Bilder und reale Eingaben am Gerät prüfen. Eine rechnerisch lösbare Situation
   belegt keine Verständlichkeit, Lernwirkung oder angemessene kulturelle Deutung.

Siehe [tatsächliche Ergebnisse und offene Abnahme](scenario-test-report.md).
