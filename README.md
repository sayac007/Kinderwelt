# Kinderwelt · fünf spielbare Lernbereiche

Offline nutzbares Godot-Projekt mit Fundament, Logik und Mathematik sowie den
Modulen aus `03_language_autonomy_social.yaml`. Brückenwerkstatt und Marktstand
enthalten je neun Level. Bildergeschichte, Entdeckerwerkstatt und gemeinsames
Dorf enthalten jeweils sechs frei wählbare Geschichten, Experimente und Szenarien.
Alle fünf Bereiche sind solo spielbar; Begleitung ist freiwillig. Aufgaben 04 und
05 wurden noch nicht umgesetzt.

## Starten

Festgelegte Version: **Godot 4.7.2.stable.official.ed1daf0bf**, Linux x86_64.
Am 19.10.2026 über den offiziellen GitHub-Release-Redirect als aktuell ermittelt.
Keine Add-ons, Konten, Dienste oder Laufzeit-Netzwerkverbindungen erforderlich.

```bash
bash scripts/install-godot.sh
export GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64
# Cloud-Sandbox: beschreibbare Einstellungen und lokale Spielstände
export XDG_DATA_HOME=/workspace/.kinderwelt/data
export XDG_CONFIG_HOME=/workspace/.kinderwelt/config
export XDG_CACHE_HOME=/workspace/.kinderwelt/cache
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
"$GODOT" --editor --path .
# F5 startet das Projekt; alternativ:
"$GODOT" --path .
```

Auf anderen Linux-Rechnern `GODOT_INSTALL_DIR` beim Installieren anpassen.
Auf Windows/macOS dieselbe Godot-Version vom offiziellen Release verwenden.
Die Installation benötigt curl, unzip, awk und sha512sum; sie verifiziert das
Archiv vor dem Entpacken gegen die offizielle Prüfsummenliste.

## Spielen und testen

Im Hub einen der fünf Bereiche wählen. Logik und Mathematik bieten Vorschläge
und freie Levelwahl; die drei neuen Bereiche sind ohne Rangstufen frei wählbar.

- **Brückenwerkstatt:** Holzstück auswählen, anschließend die passende Lücke
  antippen. Gepunktete Holzstücke können kombiniert werden; die Umrisse zeigen
  die noch fehlenden Felder. Die Figur erreicht die andere Seite, wenn die Lücke
  vollständig überbrückt ist. Mehrere Aufteilungen sind möglich.
- **Marktstand:** Frucht auswählen und in einen Korb mit passenden Umrissen
  legen. Äpfel und Birnen haben unterschiedliche Formen. Mal geht es um eine
  passende Menge, mal um Sortieren oder gleiches Verteilen. Bei vollen Körben
  zeigt die Anleitung auf den Korb mit mehr Früchten: diesen direkt antippen.
- **Bildergeschichte:** Eine Bild-/Klanggeschichte ansehen, bei Bedarf mit Pfeilen
  im eigenen Tempo blättern, dann 3–5 Bilder in Reihenfolge legen. Herausnehmen
  und Neuordnen sind jederzeit möglich.
- **Entdeckerwerkstatt:** Zwei Bildeinstellungen verändern, den Versuchspfeil
  drücken und das Ergebnis mit dem Fahnenbild vergleichen. Alle Versuche sind
  reversibel; mehrere Einstellungen können zum Ziel führen.
- **Gemeinsames Dorf:** Eine bebilderte Idee für zwei unterschiedliche Bedürfnisse
  ausprobieren. Umrisse zeigen noch offene Wünsche, ohne Punkte oder Beschämung.
  Zwei Figuren mit Sprechblase öffnen freiwillige Gesprächsimpulse.
- Das Haus führt zurück, das Raster zur Levelwahl. Der runde Pfeil startet neu.
  Rückgängig nimmt den letzten Schritt zurück. Das Ton-/Wiederholungssymbol
  zeigt die Bildanleitung erneut. Die Hand hilft in drei Stufen: **zeigen → einen
  Schritt helfen → schrittweise vormachen**. Reduzierte Bewegung zeigt das
  Beispiel ohne Animation. Hilfe ist freiwillig und blockiert keinen Level.

Tab/Pfeiltasten und Enter/Leertaste sowie Maus und Touch nutzen Godots Buttons.
Fokuswechsel scrollen zum nächsten Ziel; alle Ziele sind mindestens 96 × 72
logische Pixel groß. Escape führt zum Hub. Erwachsene finden Ton, reduzierte
Bewegung, freiwillige Gesprächshilfe und bestätigten lokalen Reset im Zahnrad.
Keine Erwachsenenaktion ist nötig. Das Zahnrad ist keine kindersichere Sperre.

Zwei verschiedene, ohne Hilfe abgeschlossene Aufgaben derselben Stufe unter den
letzten drei Abschlüssen führen zu Vorschlägen der nächsten Stufe. Fehler ziehen
keine Punkte ab und senken keine Stufe; Wiederholung derselben Aufgabe zählt
nicht doppelt. Fortschritt und Vorschläge bleiben lokal gespeichert.

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
```

Der Test verwendet ein temporäres Benutzerverzeichnis, niemals echte Spielstände.
Siehe [Architektur](docs/architecture.md), [Logik-/Mathematik-Testbericht](docs/logic-math-test-report.md),
[Bedienung und Content-Anleitung der neuen Module](docs/scenario-authoring.md) und
[aktuellen Szenarien-Testbericht](docs/scenario-test-report.md).
Es gibt synthetische Töne, **keine implementierte Sprachausgabe**. Die Bedienung
stützt sich auf Bilder, Mengenpunkte, Fokus und wiederholbare Hinweise; deutsche
Beschriftungen sind ergänzend. Verständlichkeit ohne Lesen ist auf einem physischen Gerät
mit Kind und Begleitung noch zu prüfen.

## Qualität und Evaluation

Die vorhandene Testsuite bleibt unverändert über `bash tests/run.sh` erreichbar.
Der vollständige QA-Einstieg ergänzt gepinntes GUT 9.7.1, frischen Import/Start,
statische Risiko-/Schlüsselprüfungen und eine dynamische Matrix aller Aufgaben:

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/run.sh
```

[Qualitätssystem und Ergebnisformate](docs/quality-system.md),
[aktueller Testbericht](docs/test-report.md),
[manuelle Kinder-/Geräteprüfung](docs/child-usability-checklist.md) und
[Lernhypothesen/Evaluationsplan](docs/learning-hypotheses.md).
Keine Kinderbeobachtungen werden standardmäßig erfasst; eine optionale lokale
Vorlage ist nicht aktiviert. Technische Erfolge belegen weder Lernwirkung noch
Marktreife. Reale Geräteleistung und empirische Evaluation bleiben offen.
