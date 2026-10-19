# Kinderwelt · Fundament

Offline nutzbares Godot-Projekt gemäß `01_foundation.yaml`. Alle fünf YAML-Dateien
wurden gelesen; ausschließlich das Fundament ist umgesetzt. Die fünf Eingänge
führen zu ausdrücklich einfachen Interaktions-Demos (dreimal Bild antippen),
noch nicht zu den Lernspielen aus Aufgaben 02–05.

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

Bild auswählen → großes Bild dreimal antippen → Sterne. `? ☞` hebt das Ziel hervor,
`↻ ♪` wiederholt das visuelle Signal mit Ton. `↺` beginnt neu, `⌂` führt zurück.
Tab/Pfeiltasten, Enter/Leertaste sowie Maus und Touch nutzen Godots Button-Eingaben.
Escape führt zum Hub. Große Ziele sind mindestens 96 × 72 logische Pixel groß.
Erwachsene finden Ton, reduzierte Bewegung, freiwillige Gesprächshilfe und einen
bestätigten lokalen Reset hinter dem Zahnrad. Keine Erwachsenenaktion ist zum
Spielen nötig. Das Zahnrad ist keine kindersichere Zugangssperre.

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
```

Der Test verwendet ein temporäres Benutzerverzeichnis, niemals echte Spielstände.
Siehe [Architektur](docs/architecture.md) und [Testbericht](docs/test-report.md).
Es gibt synthetische Töne, **keine implementierte Sprachausgabe**. Die Bedienung
stützt sich auf Bilder, Mengenpunkte, Fokus und wiederholbare Hinweise; deutsche
Beschriftungen sind ergänzend. Verständlichkeit ohne Lesen ist auf einem Gerät
mit Kind und Begleitung noch zu prüfen.
