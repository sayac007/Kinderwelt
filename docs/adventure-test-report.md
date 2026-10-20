# Adventure 0.3: technische Testlieferung, 20.10.2026

**Eine Mission zum ersten Gerätetest**, keine vollständige Adventure-Kampagne.
Laufzeitcode: `58103edf650d7ceec165dc7de9456e3dbc0b2cb7`, sauberer Arbeitsbaum beim
Build (`source_dirty: false`). Basis: gemergtes Kinderwelt 0.2, `origin/main` mit PR #6.
Die späteren Dokumentationsänderungen verändern diesen Laufzeitcode nicht.
Maschinenlesbare Ergebnisse: [adventure-evidence.json](adventure-evidence.json).
Regeln, Lösungen und freiwilliges Testprotokoll: [Spielanleitung](adventure-mission.md).

## Tatsächlich erzeugte Dateien

Im Cloud-Arbeitsbereich unter `/workspace/Kinderwelt/build/android-0.3-first-mission/`:

| Datei | Bytes | Signatur |
|---|---:|---|
| `kinderwelt-debug.apk` | 164121430 | Godot-Entwicklungszertifikat, v2 technisch geprüft |
| `kinderwelt-unsigned.aab` | 53755876 | bewusst unsigniert, nicht für einen Upload freigegeben |

APK SHA-256: `c4272897668de7903cfd1389888bc822a71e7ec2090bebf0fb80105d5cac938f`.

AAB SHA-256: `35c7fe31cbb030805594dd2d12d9ee9f92660b53b081275b64b429888dc144da`.

`verification.json`, `provenance.json`, vollständige `import.log`, `apk.log`, `aab.log`
und die Manifest-/Signatur-/Bundletool-Ausgaben liegen daneben. Reproduzierbare Befehle
mit vorhandenem, gepinntem Toolchain-Verzeichnis:

```bash
export GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64
bash tests/qa/run.sh --output /tmp/kinderwelt-qa-new
python3 -m unittest discover -s tests/android -v
python3 scripts/android/build.py --output build/android-new
# Mit echtem Grafikbackend, unter CI jeweils via xvfb-run -a:
bash tests/qa/adventure-render.sh /tmp/kinderwelt-adventure-new
bash tests/qa/render.sh /tmp/kinderwelt-legacy-new
bash tests/qa/experience-render.sh /tmp/kinderwelt-experience-new
```

Jedes Ausgabeziel muss neu sein. Lokal wurden Xorg-Dummy und Mesa llvmpipe verwendet,
keine headless erfundenen Bildschirmbilder. Werkzeuge/SDK-Installation und sichere
Signaturverwaltung: [Android-Build-Anleitung](android-build.md). Reproduzierbar bedeutet
hier festgelegte Quellen, Werkzeuge und Prüfungen; keine Behauptung byteidentischer
APK-Dateien über neu erzeugte Debug-Zertifikate und Build-Zeitstempel hinweg.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis und Nachweis |
|---|---|
| Vollständige QA-Orchestrierung | PASS, `/tmp/kinderwelt-03-qa-delivery/report.json` |
| Ursprüngliche vier Spieltestsuiten | 1236 Checks, 0 Fehler (33 + 559 + 59 + 585), unveränderte alten Assertions |
| Neue Adventure-Suite | 679 Checks, 0 Fehler; alle 192 Schalterzustände der drei Stufen, unabhängige Ressourcen-/Sicherheitsberechnung, mehrere Lösungsstrategien, beschädigte Zustände, gesperrte/freie Räume, echte synthetische Touch-Einspeisung, Pause, Spielstand und Wiederaufnahme, Audioauswahl und Stumm, vier Viewports |
| Statische Prüfung | PASS, keine Befunde in 181 untersuchten Dateien; begrenzte Musterprüfung, keine Sicherheitszertifizierung |
| Python-QA-Prüfer | 16 Tests bestanden |
| Gepinntes GUT: Upstream | 13 Tests, 62 Assertions, keine Fehler/Skips |
| GUT: bisherige Aufgabenqualität | 6 Tests, 13001 Assertions, keine Fehler/Skips; alle 36 Aufgaben × 4 Viewports = 144 Fälle |
| GUT: bisherige Oberfläche/Audio | 6 Tests, 22897 Assertions, keine Fehler/Skips |
| Android-/Audio-Python-Tests | 21 Tests bestanden, `/tmp/kinderwelt-03-python-delivery.log`; enthält negative Paket-/Manifestprüfungen, Logdiagnose sowie echte neue WAV-Prüfungen für Hash, Länge, Pegel, Loopgrenze und zwei unterschiedliche Stücke |
| Adventure-Grafik | 45 echte Renderframes, 0 Größenprüfungsfehler; 320×568, 360×800, 800×360, 1080×2400 mit simulierter DPI 420 sowie 320×568 mit Schriftfaktor 1.15; `/tmp/kinderwelt-03-render-delivery/` |
| Bisherige Aufgaben-Grafik | PASS, 146 Frames aller 36 Aufgaben auf zwei Viewports, `/tmp/kinderwelt-03-existing-renders/`, Laufzeitstand `c4d82f1`; danach nur Adventure-Menüfokus und Platzierung des neuen Hauptmenüknopfs geändert |
| Bisherige Experience-Grafik | PASS, 44 Frames einschließlich Dichtesimulation, `/tmp/kinderwelt-03-experience-delivery/`, Stand `58103ed` |
| Android-Export | APK und AAB tatsächlich gebaut; beide Exportlogs PASS, vollständige Artefaktverifikation PASS |

Die APK und das Bundle enthalten alle bisherigen Module sowie das Adventure und seine
zwei importierten, abspielbaren Titel. Verifiziert: ZIP-Dateiformat/Integrität, 104
Anwendungsassets, Paket `org.example.kinderwelt`, Version **0.3.0 / Code 3**, min SDK 24,
Target SDK 36, keine Android-Berechtigungen, Backup deaktiviert, `fullUser`-Orientierung,
`arm64-v8a` und `x86_64`, 16-KB-ELF-Ausrichtung; APK zusätzlich Signatur und ZIP-Ausrichtung,
AAB zusätzlich Bundletool-Validierung und fehlende Release-Signatur. Keine privaten Schlüssel oder
Entwicklungs-/Testdateien im Anwendungspaket. Das bisherige Android-Buildverfahren bleibt.

Die vollständige QA wurde auch mit leerem Importcache und separaten lokalen Spielständen
ausgeführt. Der Prüfprozess bestätigt die vier alten Suiten und die neue Adventure-Suite
getrennt; ein fehlender oder leerer neuer Testlauf kann nicht als PASS erscheinen.
GitHub Actions enthält zusätzlich den Adventure-Renderlauf. Ein erfolgreicher lokaler
Lauf ist **kein Nachweis eines bereits ausgeführten grünen GitHub-Laufs**.

## Screenshots und konkrete Sichtprüfung

[Hauptmenü](adventure-screenshots/phone_hub.png) ·
[Werkstatt](adventure-screenshots/small-phone_workshop.png) ·
[Kraftwerk](adventure-screenshots/phone_power-room.png) ·
[Quellen](adventure-screenshots/phone_sources.png) ·
[Lösung](adventure-screenshots/phone_solution.png) ·
[Offenes Tor](adventure-screenshots/phone_open-gate.png) ·
[Sternwarte](adventure-screenshots/phone_observatory.png) ·
[Querformat](adventure-screenshots/landscape_power-room.png) ·
[Große Schrift](adventure-screenshots/large-text_sources.png).

Die Bilder zeigen tatsächliche Godot-Ausgabe. Die Sichtprüfung führte zu Korrekturen
an Kamerazoom/Vertikalversatz im Querformat, überlappenden Ortsbeschriftungen, zu langen
Statuszeilen, Platzbedarf des Quellenmenüs und Zugänglichkeit des Menüfokus. Der neue
Knopf ist oben im Hauptmenü sichtbar. Kleine/quer gehaltene Displays und große Schrift
benötigen für manche **Menüs** vertikales Scrollen; die eigentliche Welt wird nicht
gewischt oder in einen ScrollContainer gepackt. Dies muss im Gerätetest verständlich sein.

## Offene Grenzen und Freigaben

- **Keine Installation auf einem echten Android-Gerät, kein Emulatorlauf.** Geprüfte
  Paketkonfiguration und Desktop-Touchsimulation ersetzen Fingerbedienung, Systemleisten,
  Rotation, Audioausgabe, App-Unterbrechung, Geräteperformance oder ein Update nicht.
- **Keine menschliche Spiel-/Hörevaluation und kein Kindertest.** Ob das Rätsel hinreichend
  anspruchsvoll ist, Hinweise helfen und Musik motiviert, bleibt offen. Keine nachgewiesene
  Lernwirkung, professionelle Grafik-/Audioqualität oder Marktreife behauptet.
- Neue Musik ist prozedurale Originalmusik mit mehreren Ebenen; Loopübergang, subjektive
  Mischung und Lautstärke auf Telefonlautsprechern sind offen. Titelzahl derzeit zwei.
- Die bekannte Warnung über zwei verbliebene Audioobjekte beim harten headless Engine-Ende
  erscheint weiterhin im Boot-Smoke-Test. Die Adventure-Suite selbst beendet sich nach
  Audioabbau ohne diese Warnung. Das ist keine Messung dauerhafter Android-Speicherstabilität.
- Der lokale Tool-Aufruf meldet vor dem isolierten Export einen nicht beschreibbaren
  Fontconfig-Cache; Import, Exporte und technische Prüfungen bestanden trotzdem. Die
  Softwaregrafik meldet außerdem nicht unterstütztes V-Sync. Beides ist kein Gerätetest.
- Bei unterschiedlicher Debug-Signatur wird Android ein Update einer alten APK ablehnen.
  **Deinstallation löscht lokale Spielstände.** Erstinstallation auf einem getrennten
  Testgerät bevorzugen; Details in der Anleitung. Kein Release-Schlüssel verwendet.
- Google-Play-Paketidentität, Datenschutz, Familien-/Zielgruppenangaben, Altersfreigabe,
  Store-Eintrag, sichere dauerhafte Signatur und manuelle Freigaben bleiben unverändert
  offen. [Bestehende Play-Checkliste](google-play-release-checklist.md) gilt weiter.

Vorläufige Fehlversuche sind keine bestandenen Tests: Der erste Renderharness ließ beim
Wechsel zwischen verschiedenen DPI-Simulationen ein altes, erst verzögert freizugebendes
App-Objekt aktiv. Dessen Fenster-Signal kollidierte mit dem neuen Profil. Der Harness gibt
jede App jetzt vollständig frei. Die erste zusätzliche Touch-Prüfung wartete nicht auf
Godots Eventdispatch; sie wurde auf echte, über Frames eingespeiste Touch-Ereignisse
korrigiert. Die oben genannten endgültigen Läufe sind die erfolgreichen Nachweise.

## GitHub-Übergabe

Branch `feat/explorer-adventure-v03` erfolgreich nach GitHub gepusht.
`gh pr create --base main --head feat/explorer-adventure-v03` wurde tatsächlich versucht;
die GitHub-GraphQL-API antwortete `Forbidden`. Es wurde damit kein PR automatisch erstellt.
[Pull Request gegen main manuell erstellen](https://github.com/sayac007/Kinderwelt/compare/main...feat/explorer-adventure-v03?expand=1).
Remote Actions wurden hier nicht als erfolgreich ausgeführt bestätigt.
