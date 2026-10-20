# Kinderwelt 0.2 — tatsächliche technische Ergebnisse

Stand 20.10.2026. Geprüfter Codecommit `3e48018df27d357d41305e61e6fa904861829415` auf
`feat/child-friendly-experience`, ausgehend vom aktuellen main einschließlich
PR #5. Code, neue Tests und Android-Version 0.2.0 / Code 2 sind implementiert.
Die folgenden Ergebnisse sind technische Befunde, keine bestätigte
Kinder-Usability oder Lernwirkung.

## Neue APK und erhaltene Pipeline

| Tatsächlich erzeugte Datei | Größe | Signatur / Prüfung |
|---|---:|---|
| `build/android-0.2-release-check/kinderwelt-debug.apk` | 163620889 Bytes | Godot-Entwicklungszertifikat, APK v2 PASS |
| `build/android-0.2-release-check/kinderwelt-unsigned.aab` | 53254525 Bytes | UNSIGNIERT, bundletool/jarsigner PASS |

Absoluter Artefaktordner: `/workspace/Kinderwelt/build/android-0.2-release-check/`.
Kein signiertes Release-AAB, kein Release-Schlüssel, kein Play-Upload.

```text
668753c13b1af052ca125d64f26ab2a2644e2de7f31bbaf0a5a70f7c25df4469  kinderwelt-debug.apk
536fb90556be5f05f568c5be973970160099fe23b7e08371eaa25ae158bf506b  kinderwelt-unsigned.aab
```

APK und AAB enthalten alle fünf Spielbereiche und alle fünf tatsächlich
abspielbaren importierten Musikstücke. Der strengere Prüfer verlangt jetzt
zusätzlich Musik-Importdateien, Sample-Payloads und Herkunftsmanifest. 87 Assets
wurden geprüft. Paketkennung `org.example.kinderwelt` bleibt der ausdrücklich
nicht veröffentlichungsfähige Platzhalter. API 24–36, arm64-v8a/x86_64,
fullUser, Backup aus und keine angeforderten Berechtigungen entsprechen der
Konfiguration. ZIP-Integrität, apksigner v2, APK zipalign 16 KB und ELF-Segmente
beider Artefakte PASS. Entwicklungs-/Studien-/Schlüsseldateien fehlen im Paket.
Eine tatsächliche 0.2-Geräteinstallation wurde hier nicht ausgeführt.

Ausgeführter Build:

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 \
  python3 scripts/android/build.py --output build/android-0.2-release-check
```

Die bestehende gepinnte Toolchain, SDK-Pfadkorrektur, Fehlerausgabe und der
Android-Actions-Workflow bleiben erhalten. Ein sauberer Actions-Checkout erzeugt
die Dateien unter `build/android/` und lädt sie als
`android-development-artifacts` hoch. Lokal wird wegen vorhandener älterer
Builds ein neuer Ausgabeordner verwendet. Neue grafische Prüfungen im
Qualitätsworkflow verwenden Xvfb; dessen Vorhandensein auf Ubuntu-24.04 ist in
der offiziellen Runner-Toolliste bestätigt. Hier wurden sie mit Xorg-Dummy und
Mesa llvmpipe ausgeführt. Der Remote-Actions-Lauf ist **UNBESTÄTIGT**: auch die
Lese-API meldet `Forbidden`.

## Vollständige ausgeführte Prüfungen

`GODOT=... bash tests/qa/run.sh --output /tmp/kinderwelt-02-qa-release`: **PASS**.
Die vorhandenen Tests und Assertionen wurden nicht entfernt oder abgeschwächt.
Die geringere Anzahl von Qualitätsassertionen gegenüber 0.1 ergibt sich aus
weniger dauerhaft angezeigten Erwachsenen-Steuerelementen, nicht gelöschten Tests.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Bestehende Smoke / Learning / Input / Scenarios | 33 + 559 + 59 + 585 = **1236 Checks PASS** |
| Bestehende GUT-Qualität | **6 Tests / 13001 Assertions PASS**, alle 144 Aufgaben-/Viewport-Kombinationen |
| Neue Experience-Suite | **6 Tests / 22891 Assertions PASS** |
| Gepinnte GUT-Upstream-Auswahl | **13 Tests / 62 Assertions PASS** |
| Bestehende Python-QA-Prüferregression | **16 Tests PASS** |
| Android-/Diagnose-/Audioasset-Python-Tests | **19 Tests PASS** |
| Statischer Quell-/Berechtigungs-/Geheimnisscan | PASS ohne Befund; kein vollständiges Security-Audit |
| Frischer Import/Start, Quellenstabilität, Inhaltsabdeckung | PASS |

Die Experience-Suite prüft alle 36 Aufgaben an vier Viewports auf Textgröße,
Textabschnitte, Überlagerungen in Containern, Breite, Touchmaße und zugängliche
Beschriftungen. Zusätzlich: 15 % größere Schrift über alle Aufgaben bei 320×568,
Token-/Buttonzustandskontraste, deutsche Glyphen, modellierte Dichteprofile,
ständig sichtbare Ton-Taste, keine permanente Elternleiste, kompatible Spielstände,
getrennte Lautstärken, echte Musik-Streams mit vollständiger Loop-Länge,
Stumm/Fortsetzen/Persistenz, Hintergrundpause und korrektes Schließen optionaler
Elternhinweise. Die bestehenden Suiten behalten echte Touch-Dispatch- und
Tastaturnavigationstests sowie die Lösungen aller Aufgaben.

Die Audiotests prüfen die fünf wirklichen WAV-Dateien auf Signalenergie,
Nichtübersteuerung, Anfang/Ende, Länge und SHA256. Das beweist keine subjektiv
hochwertige Instrumentierung oder angemessene Lautheit auf einem Telefon.

Die abschließenden Läufe basieren auf dem festgeschriebenen Codecommit oben;
source_dirty ist in den Maschinenbelegen korrekt true, weil die neuen
Dokumentationsentwürfe damals untracked waren. Laufzeitcode war committed, und
der QA-Quelldigest blieb während der Prüfung unverändert. Vollständige Logs:
`/tmp/kinderwelt-02-qa-release/`, `/tmp/kinderwelt-02-qa-release.log`,
`/tmp/kinderwelt-02-unit-release.log`, `/tmp/kinderwelt-02-build-release-check.log`.
Build-Manifest/Signatur/Provenance liegen beim APK. Kompakte maschinenlesbare
Belege: [child-friendly-evidence.json](child-friendly-evidence.json).

## Tatsächliche grafische Belege

- `tests/qa/render.sh`: alle 36 Aufgaben bei 320×568 und 768×1024, **146 Frames**
  einschließlich Scrollseiten, unter `/tmp/kinderwelt-02-delivery-all-renders/`.
- `tests/qa/experience-render.sh`: **44 echte Renderings**, vier Profile ×
  Spielauswahl sowie Start-/Abschlusszustand aller fünf Bereiche, unter
  `/tmp/kinderwelt-02-delivery-experience/`. Das Dichteprofil 1080×2400 / 420 DPI
  ergibt 412×915 logische Einheiten und 1080×2398 tatsächliche Bildpixel.
- Repräsentative Startansichten aller fünf Bereiche und Tablet-/Dichteansichten
  wurden visuell angesehen; elf unveränderte PNG-Beispiele sind im Repository
  unter `docs/child-friendly-screenshots/`. Dies sind Godot-Desktop-Aufnahmen,
  keine Android-Screenshots. Kein pixelidentischer Golden-Image-Vergleich oder
  vollständige menschliche Freigabe aller Zustände wird behauptet.

Die Aufnahmen stammen vom unmittelbar vorhergehenden Commit `f78084e`; die
abschließende Korrektur von gespeicherter Mute-Beschriftung und optionalem
Prompt-Fokus ändert die gezeigten initialen Layouts nicht. Beide Renderbefehle
prüfen Exitcode, Godot-Fehler, vollständige Bildanzahl und tatsächliche PNG-Maße.

## Gefundene/behandelte Fehler und offene Grenzen

Behoben wurden unter anderem die Desktop-Pixelbehandlung auf Android,
unverständliche bloße Symbolaktionen, permanent reservierte Elternfläche,
zu kleine Bildkarten und Ziele, Loop-Längenberechnung nach Audio-Kompression,
eine Fokusregression bei automatischer Aufgabenwiederholung, Fokus beim
Schließen eines Elternhinweises und falsche Mute-Beschriftung nach Neustart/Reset.
Eine anfänglich fehlerhafte Screenshot-Simulation wurde nicht als Nachweis
verwendet: sie ließ die Desktop-Skalierung zurücksetzen. Der endgültige
Dichte-Test verwendet denselben Konfigurationspfad wie Android und prüft die
wirkliche logische Rendergröße.

**Offen:** Kein Android-Emulator ist eingerichtet; `/dev/kvm` fehlt. Physische
0.2-Installation, tatsächliche DPI/Touchgröße, Safe Areas, Systemleisten,
Rotation, Lautheit, Kopfhörer, Fokus-/Resume-Verhalten auf Android,
TalkBack/Assistenztechnik und Geräteperformance sind nicht geprüft.
Bei hartem `--quit-after` im Headless-Dummy-Audiobetrieb meldet Godot zwei beim
Beenden noch gehaltene WAV-/Playback-Objekte. Die Warnung wird nicht unterdrückt;
Langzeit-/Lifecycle-Verhalten auf Android ist daher zusätzlich zu beobachten.
Keine Scriptfehler und keine fehlgeschlagenen Abschlussassertionen bleiben im
finalen Lauf. Die Musik ist ein funktionsfähiger eigener Retro-Prototyp;
orchestrale Produktion und menschlicher Hörtest stehen aus.

Der Zielzustand „ein siebenjähriges Kind versteht und bedient Kinderwelt
weitgehend selbstständig“ bleibt **nicht nachgewiesen**, bis der
[reale Smartphone-Test](child-friendly-device-checklist.md) stattgefunden hat.
Datenschutz-/Families-/Store-/Signaturfreigaben und Lernwirkungsnachweise bleiben
von diesem Meilenstein getrennt. Keine Marktreife- oder Play-Uploadbehauptung.

## GitHub-Übergabe

`feat/child-friendly-experience` wurde erfolgreich nach origin gepusht. Die
PR-Erstellung mit der fertigen Beschreibung scheiterte erneut mit
`Post "https://api.github.com/graphql": Forbidden`. Ein erfolgreich erstellter
PR oder grüner Remote-Actions-Lauf wird nicht behauptet.

[PR gegen main manuell erstellen](https://github.com/sayac007/Kinderwelt/compare/main...feat/child-friendly-experience?expand=1).
Die Beschreibung liegt in [child-friendly-pull-request.md](child-friendly-pull-request.md).
