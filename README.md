# Kinderwelt · Fundament, Logik und Mathematik

Offline nutzbares Godot-Projekt gemäß `01_foundation.yaml` und `02_logic_math.yaml`.
Brückenwerkstatt und Marktstand enthalten jeweils neun spielbare Level in drei
Stufen. Die drei übrigen Hub-Eingänge bleiben Fundament-Demos; Aufgaben 03–05
sind unverändert und noch nicht implementiert.

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

Im Hub die Brücke oder die Obstpunkte wählen, dann den Pfeil für den aktuellen
Levelvorschlag oder eine der neun Levelkarten. Alle Stufen sind frei zugänglich.

- **Brückenwerkstatt:** Holzstück auswählen, anschließend die passende Lücke
  antippen. Gepunktete Holzstücke können kombiniert werden; die Umrisse zeigen
  die noch fehlenden Felder. Die Figur erreicht die andere Seite, wenn die Lücke
  vollständig überbrückt ist. Mehrere Aufteilungen sind möglich.
- **Marktstand:** Frucht auswählen und in einen Korb mit passenden Umrissen
  legen. Äpfel und Birnen haben unterschiedliche Formen. Mal geht es um eine
  passende Menge, mal um Sortieren oder gleiches Verteilen. Bei vollen Körben
  zeigt die Anleitung auf den Korb mit mehr Früchten: diesen direkt antippen.
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
Siehe [Architektur](docs/architecture.md) und [Testbericht](docs/test-report.md).
Es gibt synthetische Töne, **keine implementierte Sprachausgabe**. Die Bedienung
stützt sich auf Bilder, Mengenpunkte, Fokus und wiederholbare Hinweise; deutsche
Beschriftungen sind ergänzend. Verständlichkeit ohne Lesen ist auf einem physischen Gerät
mit Kind und Begleitung noch zu prüfen.
