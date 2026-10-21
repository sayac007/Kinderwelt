# Tatsächliche Prüfungen Kinderwelt 0.7

Stand: 21. Oktober 2026. Die folgenden Ergebnisse stammen aus tatsächlich ausgeführten lokalen Prüfungen; der GitHub-Actions-Status wurde nicht beobachtet.

**Bestanden:** 5.378 Godot-Prüfungen ohne Fehler, 34 Python-Tests, regulärer und cachefreier Start mit jeweils 60 Frames sowie 335 echte Desktop-OpenGL-Renderings. Die 16 Android-Verifier-Tests wurden nach der Änderung der Preview-Paketkennung zusätzlich erfolgreich ausgeführt.

Geprüft wurden alle 35 Figuren-/Look-Kombinationen und die Atlasmasken, Speicherung pro Figur und alte Spielstände, acht direkt erreichbare Fächer, alle 960 lokalisierten Aufgabenansichten bei kleiner Fenstergröße, wiederholte Drehungen derselben offenen Aufgabe, Hinweise ohne Unterbrechung, sechs Lobvarianten, tatsächlicher Musikwechsel, Punkte ohne Mehrfachgewinn und die drei Kulissen einschließlich reduzierter Bewegung. Die ursprünglichen 24 Aufgaben bleiben enthalten.

1.621 unterschiedliche Sprachdateien und alle 20 Musikstücke wurden tatsächlich dekodiert und auf Hash, Dauer und Pegel geprüft. Der lokale Quellaudit fand keine Laufzeit-Netzwerkzugriffe oder Android-Berechtigungen in seinem begrenzten Prüfumfang. Das ist keine Sicherheitszertifizierung.

Die Renderings wurden mit Godot 4.7.2 und Mesa llvmpipe in vier Profilen erstellt: 360×800, 320×568, 800×360 und 1080×2400 mit simulierten 420 DPI. Darunter sind echte Größenwechsel desselben laufenden Fensters. Ausgewählte Bilder wurden manuell betrachtet; keine vollständige visuelle Einzelabnahme aller 335 Bilder.

## Android-Dateien

Beide Varianten wurden aus dem sauberen Commit `1da98ae76b3202d31fb1d1aacc354a068faa6a0e` erzeugt. Der nachfolgende Dokumentationscommit verändert keine ausgelieferten App-Dateien. Beide Quellhashes und alle Artefakthashes wurden nach dem Build erneut mit den aktuellen Dateien verglichen. Die separate Preview verändert ausschließlich Paket- und Anzeigenamen.

| Variante | Datei | Bytes | Signatur |
|---|---|---:|---|
| standard | `build/android-v07/kinderwelt-debug.apk` | 197,707,702 | temporärer Godot-Entwicklungsschlüssel, v2 geprüft |
| standard | `build/android-v07/kinderwelt-unsigned.aab` | 186,388,224 | UNSIGNIERT |
| preview | `build/android-v07-test/kinderwelt-debug.apk` | 197,707,754 | temporärer Godot-Entwicklungsschlüssel, v2 geprüft |
| preview | `build/android-v07-test/kinderwelt-unsigned.aab` | 186,388,350 | UNSIGNIERT |


Die Test-App heißt **Kinderwelt 0.7 Test**, Kennung `org.example.kinderwelt.preview.v07`. Sie kann neben der bisherigen Standard- oder 0.6-Test-App installiert werden und verwendet einen eigenen lokalen Spielstand. Die Standard-App verwendet `org.example.kinderwelt`. Bei einem anderen früheren Entwicklungsschlüssel ist kein direktes Update möglich; bestehende Daten nicht durch unbedachtes Deinstallieren verlieren.

Bei allen vier Dateien bestanden: ZIP-/Bundleformat, Paketkennung, Version 0.7.0 / Code 7, API 24–36, `fullUser`-Rotation, keine Android-Berechtigungen, deaktiviertes Backup, arm64-v8a und x86_64, 16-KB-ELF-Ausrichtung, komprimierte native Bibliotheken, vollständige Spiel-/Grafik-/Audioressourcen und Lizenzdateien. Die APKs bestanden zusätzlich Signatur- und 16-KB-ZIP-Ausrichtungsprüfung; Bundletool validierte beide AABs. Pro Datei wurden 3.413 App-Ressourceneinträge kontrolliert. Keine privaten Schlüssel im Repository.

SHA-256:

```text
98548390d1d694163d66a1c0bed7caa4c336d176ad328c1c636a951779ab759d  build/android-v07/kinderwelt-debug.apk
727f50ec2a77dd949df39472c8e1d9e32b2d32998ab33696dfb6289ddb0f8016  build/android-v07/kinderwelt-unsigned.aab
597d462f8bd1a86c42d928a0bafe4e1179790db31704ccca20600f51899547ff  build/android-v07-test/kinderwelt-debug.apk
df11888448252363a913abe5b27c8d21c6588f248ded9ffac32301b83b2f138a  build/android-v07-test/kinderwelt-unsigned.aab
```

Größen sind Archivgrößen, keine gemessene Geräte-Downloadgröße oder installierter Speicherbedarf. Die APKs sind etwa 197,7 MB, die AABs etwa 186,4 MB groß.

## Nachweise und Reproduktion

[Maschinenlesbare Gesamtergebnisse](test-evidence.json), [vollständiges Testsuite-Protokoll](qa-evidence/v07/tests.log), [Rendering-Protokoll](qa-evidence/v07/renderings.log), [335 Bildnamen, Größen und Hashes](qa-evidence/v07/renderings.json), [Quellaudit](qa-evidence/v07/audit.json). Android: [Standard-Build](qa-evidence/v07/android-standard.log), [Test-Build](qa-evidence/v07/android-preview.log), [Standard-Verifikation](qa-evidence/v07/standard-verification.json), [Preview-Verifikation](qa-evidence/v07/preview-verification.json). Provenienz, Manifest-, Signatur- und Größenberichte liegen im selben Nachweisordner. Screenshots: `docs/screenshots/`, Look-Galerien: `docs/character-proposals/`.

```sh
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/quest-render.sh /tmp/neue-renderings
python3 scripts/android/build.py --output build/neuer-standard
python3 scripts/android/build.py --preview --output build/neuer-test
```

Für den Renderer wird ein verfügbarer X11-/OpenGL-Bildschirm benötigt. Neue Ausgabeverzeichnisse verwenden. Die Metadaten-Neuerzeugung mit `python3 scripts/graphics/compile_wardrobe.py` ergab vor dem Quellcommit identische Bytes. Android-Toolchain und Installation: [android.md](android.md).

## Offen und ausdrücklich nicht nachgewiesen

- Installation, Start, Leistung/Speicherbedarf, Touch und wiederholte Drehung auf echten Android-Geräten, insbesondere Geräte-Safe-Areas und schmale/alte Geräte. Desktop-Simulation ersetzt dies nicht.
- Verständlichkeit jedes Wortes durch deutsch-, englisch- und russischsprachige Zuhörer sowie Kinder. Eigenständige Stimmen: Deutsch Kerstin, Englisch LJSpeech, Russisch Denis. Keine Kate-Beckinsale-Kopie; die Interviewaufnahme wurde nicht verwendet. [Hörproben](voice-previews/README.md).
- Kinderbeobachtung und fachliche/pädagogische Evaluation der Aufgaben. Keine empirisch nachgewiesene Lernwirkung.
- Google-Play-Freigaben, Datenschutz-/Zielgruppen-/Store-Prüfungen und dauerhafte Release-Signatur. Beide AABs sind unsigniert und nicht uploadbereit.
- Remote-CI-Läufe und deren Artefakt-Upload müssen nach dem Push auf GitHub geprüft werden. Lokale erfolgreiche Exporte belegen keinen bestandenen Remote-Lauf.
