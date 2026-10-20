# Kinderwelt 0.2 · Child-Friendly Experience

Offline nutzbares Godot-Projekt mit Fundament, Logik und Mathematik sowie den
Modulen aus `03_language_autonomy_social.yaml`. Brückenwerkstatt und Marktstand
enthalten je neun Level. Bildergeschichte, Entdeckerwerkstatt und gemeinsames
Dorf enthalten jeweils sechs frei wählbare Geschichten, Experimente und Szenarien.
Alle fünf Bereiche sind solo spielbar; Begleitung ist freiwillig. Das Qualitätssystem
aus Aufgabe 04 und die Android-Verifikationspipeline aus Aufgabe 05 sind ergänzt.
Google-Play-Freigabe und Geräteprüfungen stehen aus.

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
Es gibt fünf integrierte eigene Retro-Musikstücke, getrennte Musik-/Effektregler
und synthetische Spielklänge, **keine implementierte Sprachausgabe**. Die Bedienung
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

## Android-Verifikation

Die [Android-Build-Anleitung](docs/android-build.md) beschreibt den gepinnten
Werkzeugsatz und die Befehle für Debug-APK und unsigniertes AAB. GitHub Actions
baut beide als überprüfbare Artefakte; die Ausführung auf GitHub ist gesondert
zu bestätigen. Der bestehende Qualitätsworkflow bleibt erhalten.

[Build-Ergebnisse](docs/release-report.md),
[Google-Play-Freigaben](docs/google-play-release-checklist.md),
[Store-Entwurf](docs/store-listing-de.md) und
[Datenschutz-Entwurf](docs/privacy-policy-draft.md).
**Upload gesperrt:** Platzhalter-Paketkennung, fehlende Release-Signatur,
offene aktuelle Policy-Prüfung und ausstehende Geräte-/Betreiberfreigaben.

## Meilenstein 0.2

Helles Designsystem, illustrierte Spielauswahl, beschriftete gemeinsame Navigation,
Android-Dichteskalierung, größere Schrift auf Wunsch und optionaler Erwachsenenmodus.
Alle 36 Aufgaben bleiben erhalten. Die eigene Musik ist tatsächlich integriert;
Nutzung und Spielstände bleiben offline und lokal.

[Architektur und Vorher/Nachher](docs/child-friendly-experience.md) ·
[Musik und Herkunft](docs/music-provenance.md) ·
[tatsächliche Tests und APK](docs/child-friendly-test-report.md) ·
[nächster Smartphone-Test](docs/child-friendly-device-checklist.md).

Die neue Debug-APK liegt in dieser Sitzung unter
`build/android-0.2-release-check/kinderwelt-debug.apk` (Version 0.2.0, Code 2).
Auf GitHub liefert der Android-Workflow sie im Artefakt
`android-development-artifacts`; der Remote-Lauf ist separat zu prüfen.
Die Bedienbarkeit für Siebenjährige und die Lautheit auf dem Gerät sind noch
nicht durch Menschen nachgewiesen. Es gibt keine Play-Veröffentlichung.
