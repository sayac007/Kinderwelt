# Sprachklarheit und freier Punktezähler – 0.7.1

Die Rückmeldung aus dem Handytest zeigte einen Fehler, den die bisherigen Prüfungen nicht erfassten: Eine Datei kann korrekt dekodierbar sein, stille Ränder und die erwartete Gesamtdauer haben und trotzdem Wörter verschlucken. Die alte deutsche Kerstin-low-Aufnahme „Physik“ hatte 0,834 Sekunden erzeugte Dauer, einschließlich 0,18 Sekunden Vorlauf und 0,35 Sekunden Nachlauf. Für das erzeugte Wort blieben etwa 0,304 Sekunden. Eine langsamere Einstellung oder längere Pause allein löste die Aussprachefehler dieser Stimme nicht zuverlässig.

Nach der Entscheidung „Klarheit zuerst, männliche Stimme ist okay“ wurde die gesamte deutsche Sammlung mit **Thorsten high (CC0, 22.050 Hz)** neu erzeugt. Deutsch verwendet den Sprechdauerfaktor 1,6 und keine Zufallsvariation der Lautdauern. Die deutsche Physik-Aufnahme enthält jetzt rund **0,789 Sekunden modellseitig zugeordnete phonetische Wortdauer**, getrennt von eingefügter Stille. Sie dauert insgesamt rund 1,51 Sekunden. Englisch bleibt LJSpeech, Russisch Denis; deren kurze Fach-/Lookansagen verwenden ebenfalls feste Lautdauern und einen Dauerfaktor 1,5. Einige Fachnamen bekommen einen kurzen, tatsächlich gesprochenen Satzkontext. Bei deutschen Auswahlaufgaben werden die Optionen als vollständiger Satz verbunden, statt einzelne isolierte Einwortsätze zu erzeugen.

Die freie ONNX-Entwicklungsinstrumentierung legt den vorhandenen VITS-Dauertensor offen. Sie verändert nicht die Audioberechnung und wird nicht in der App ausgeliefert. Für jede neu erzeugte Aufnahme müssen die vorhergesagten Lautdauern genau der erzeugten Samplezahl entsprechen. Deutsche Manifeste enthalten Zeitintervalle der phonetischen Wörter; auch die kurzen englischen/russischen Ansagen enthalten solche Messwerte. Bei ausgeschriebenen Zahlen kann ein Schriftwort in mehrere phonetische Wörter zerfallen. Das sind **Modellzuordnungen**, keine menschlich geprüften Einzelwortgrenzen und kein Beweis, dass ein Kind jedes Wort versteht.

Die bisherigen englischen/russischen längeren Aufgabenaufnahmen bleiben erhalten. Die deutsche Sammlung umfasst weiterhin 663 Zuordnungen mit 583 unterschiedlichen Dateien; insgesamt sind es 1.621 unterschiedliche Sprachdateien. Die App arbeitet weiter ohne Netzwerk, Mikrofon oder TTS-Modell. Die beigefügte Schauspieleraufnahme wird nicht verwendet.

Für „Chemie“ wird außerdem die Standardlautung `çeˈmiː` ausdrücklich zugeordnet; die ursprüngliche Lautfolge hatte einen überlangen ersten Vokal und eine ungünstige Betonungszuordnung. Satzgrenzen bleiben bei dieser Korrektur erhalten. Auch danach liefert die unabhängige Rückerkennung für dieses Wort teilweise abweichende Ergebnisse: Es bleibt ein ausdrücklicher Punkt für die Hörabnahme.

## Tatsächliche Prüfverfahren

- Alle ausgelieferten Sprachdateien vollständig mit FFmpeg dekodieren, Dauer, Pegel, Dateihash und stille Ränder prüfen.
- Modellseitige Lautdauer unabhängig von künstlicher Stille kontrollieren; für die Fachnamen Mindestdauern prüfen. Sehr kurze Funktionswörter wie „es“ haben natürlicherweise kürzere Zeiten als „Physik“.
- Die echte Godot-Audiobus-Ausgabe erfassen: „Physik“, vollständige Aufgabe und danach Lob in allen drei Sprachen. Eine sofort richtige Antwort darf die Aufgabe nicht unterbrechen. Samplezahl, Pegel, verstrichene Zeit und tatsächlich gespielte Clipfolge werden geprüft.
- 31 feste Stichproben je Sprache mit unabhängigem multilingualem Whisper small (int8) ohne vorgegebenen Referenztext zurückerkennen: acht Fächer, sechs Lobvarianten, Wiederholungshinweis und je acht Aufgaben/Hilfen. Vergleich mit den ursprünglichen Dateien. Rohtexte und Modell-/Dateihashes im Nachweisordner.

Automatische Rückerkennung bleibt ein Suchverfahren für problematische Wörter. Schreibvarianten, Akzent und ASR-Fehler können Abweichungen erzeugen; geringe Fehlerquoten beweisen keine vollständige Hörverständlichkeit. Nicht erkannte Wörter bleiben als Befunde sichtbar. [Aktuelle Messergebnisse und Grenzen](test-report.md), [neue und alte Hörproben](voice-previews/README.md).

## Punktezähler

Der konkrete Layoutfehler entstand durch die Mindestbreite von Godots Schaltfläche: „Eichhörnchen“ vergrößerte die geplante Figuren-Schaltfläche von 83 auf **129 logische Pixel**. Ab Position x=10 endete sie damit bei x=139, während der Punktezähler schon bei x=96 beginnt. Die Texteinstellung begrenzt die Figuren-Schaltfläche jetzt auf ihren vorgesehenen Platz und zeigt bei Bedarf eine Ellipse; der vollständige Name steht im Tooltip und in der Figurenauswahl. Der Zähler ignoriert Berührungen und schneidet eigene Zeichnung an seinen Grenzen ab.

Die Regression prüft die tatsächlichen Godot-Rechtecke aller sieben Namen in drei Sprachen und fünf Bildschirmprofilen mit 3.200 Punkten. Dazu kommen echte Touchtests auf Figuren-/Menüschaltfläche und Überschneidungsprüfungen für Schließen, Lautsprecher und Frage in Aufgaben. Neue echte Renderings zeigen die maximale Punktzahl in Welt und Aufgabe auf vier Profilen.

## Reproduzieren

Die App selbst benötigt keine Entwicklungs-Sprachmodelle. Für erneute Sprachgenerierung wurden Piper 1.4.2, ONNX Runtime 1.31.0, ONNX 1.23.2, NumPy 2.5.4 und FFmpeg verwendet. Der optionale unabhängige ASR-Test verwendet sherpa-onnx 1.13.8 und lokale Whisper-small-Modelldateien. Die Modellhashes stehen in Manifesten bzw. ASR-Berichten. Die Skripte laden keine Modelle selbst nach.

```sh
python scripts/generate-quest-voice.py --locale de --model /pfad/de_DE-thorsten-high.onnx
python scripts/qa/speech_recognition.py --model /pfad/sherpa-onnx-whisper-small --output /tmp/sprachpruefung.json
KINDERWELT_SPEECH_REPORT=/tmp/wiedergabe.json GODOT=/pfad/Godot bash tests/run.sh
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 GODOT=/pfad/Godot bash tests/qa/quest-render.sh /tmp/neue-bilder
```

Echte Handy-Lautsprecher, Bluetooth, Umgebungsgeräusche, Android-Audiofokus und die muttersprachliche Hörabnahme bleiben separat zu prüfen. Die manuelle Abnahme sollte besonders kurze Fachnamen, Zahlen, Anlaute und die im ASR-Bericht auffälligen Wörter wiedergeben, mit und ohne Musik. Kinder müssen freiwillig teilnehmen; es werden keine Stimmen oder personenbezogenen Daten aufgezeichnet.
