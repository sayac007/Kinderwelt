# Tatsächliche Prüfungen und Android-Artefakte – 0.7.2

> Historischer Versionsbericht. Aktuelle Funktionen, Tests und offene Freigaben: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die folgenden Ergebnisse gelten ausschließlich für den genannten früheren Stand.

Stand: 21. Oktober 2026. Fünf getrennte Phasencommits plus dieser Nachweiscommit. Gebaut aus dem sauberen Quellcommit `52a7cedb91f568be2b2b644aa68e1a5d2f671908`; beide Provenienzdateien melden `source_dirty=false`. Private Grafiken sind bewusst extern; ihr vollständiger materialisierter Inhalt ist im App-Quellhash des privaten Builds erfasst.

## Ausgeführt und bestanden

| Prüfung | Privater Stand | Öffentlicher Stand ohne privaten Pack |
|---|---:|---:|
| Godot-Spielregressionen | 6.085 / 0 Fehler | 6.085 / 0 Fehler |
| Tatsächliche Audiobusprüfungen | 30 / 0 Fehler | 30 / 0 Fehler |
| Frischer App-Import und 60-Frame-Start | bestanden | bestanden |
| Python-Regressionssuite | 56 / 0 Fehler | 56 / 0 Fehler |
| Echte Software-Renderings | 343 | 343 nach Ausschnittkorrektur |
| Vollständige Decodierung Sprachdateien | 1.633 unterschiedliche Dateien | gleiche Sammlung |
| Vollständige Decodierung Musik | 20 Stücke | gleiche Sammlung |
| Quell-/Inhalts-/Ablenker-/Sprach-/Musikprüfungen | bestanden | bestanden |

Nach Ergänzung der erhaltenen Petzold-Zuschreibung nochmals alle 56 Python-Tests im privaten Stand sowie die vier betroffenen Konfigurations-/Nachweistests im öffentlichen Stand bestanden. Der frühere öffentliche Raster-Render mit Nachbarfragment ist verworfen. Die abschließenden 343 öffentlichen Renderings verwenden enge Alpha-Grenzen und Masken; Auswahl und maximale Punkteanzeige wurden stichprobenartig angesehen.

Protokolle: [Phasen](phases.md), [phase5-family.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-family.log), [phase5-public.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-public.log), [phase5-python.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-python.log), [phase5-family-render.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-family-render.log), [phase5-public-verified-render.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-public-verified-render.log), [phase5-public-attribution-tests.log](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/phase5-public-attribution-tests.log). ASR-Rohbefunde und Grenzen: [Stimme](voice.md). Keine manuelle Hörabnahme oder Kinderstudie wurde durchgeführt.

## Tatsächlich erzeugte Dateien

| Variante | Datei im Ausgabeordner | Bytes | MB (dezimal) |
|---|---|---:|---:|
| family | `build/android-v072-family/kinderwelt-debug.apk` | 183,037,438 | 183.037 |
| family | `build/android-v072-family/kinderwelt-unsigned.aab` | 171,670,185 | 171.670 |
| public | `build/android-v072-public/kinderwelt-debug.apk` | 178,166,519 | 178.167 |
| public | `build/android-v072-public/kinderwelt-unsigned.aab` | 166,806,808 | 166.807 |

APKs sind mit temporären Godot-Entwicklungsschlüsseln signiert; AABs sind **unsigniert**. Die APKs sind für Installation vorbereitet und technisch geprüft, wurden hier jedoch auf keinem echten Android-Gerät installiert. Beide Vorschauen haben getrennte Daten und können neben der bisherigen Installation bestehen. APK-Updates erfordern denselben Signierschlüssel; keine dauerhafte Release-Identität wurde eingerichtet.

Alle vier Artefakte: gültige ZIP-/APK-/Bundle-Struktur, tatsächliche Datenidentität, alle erwarteten Sprach-/Musik-/Grafikressourcen, korrekte gewählte Figurenvariante, Version **0.7.2 / Code 9**, API **24–36**, keine Berechtigungen, Backup aus, Rotation `fullUser`, ABIs `arm64-v8a` und `x86_64`, 16-KB-ELF-/APK-Ausrichtung und komprimierte native Bibliotheken geprüft. AAB zusätzlich mit Bundletool validiert; Rendering `gl_compatibility`, keine Release-Signatur.

Pakete: privat `org.example.kinderwelt.preview.family.v072`; öffentlich `org.example.kinderwelt.preview.neutral.v072`. Die Basiskennung bleibt ausdrücklich vorläufig und konfigurierbar. [Buildbefehle](android.md).

Hash-/Signatur-/Größen-/Quellnachweise stehen unter [Archivindex: android-v072-family-*](qa/ARCHIVE_INDEX.tsv) und `android-v072-public-*`. Vollständige Import-/Export-/Bundletool-Logs bleiben in den jeweiligen lokalen Build-Ausgabeordnern.

### SHA256

| Datei | SHA256 |
|---|---|
| family/kinderwelt-debug.apk | `843b6e7b6d8f399527798c226912a7d60c35beba7e60d31045086267ce930821` |
| family/kinderwelt-unsigned.aab | `31a46198cae9c2667ce9b4cc525040e645bb4b46c60985f1493fc52b62495d81` |
| public/kinderwelt-debug.apk | `41c0c19ef1f88324036d0863e192980686cd80e50370cb70a278f107dbcaf95d` |
| public/kinderwelt-unsigned.aab | `bb902722db2b7df9f9f4b7c67576e880918524a543d4d618e2205566fd360746` |

## Größenvergleich

Gemessen mit `scripts/android/analyze_size.py`, jeweils beide ABIs, APK beziehungsweise AAB getrennt. Archivgröße, nicht installierter Speicherbedarf oder Play-Download.

| Stand | APK | AAB |
|---|---:|---:|
| Ausgangsstand 0.7.1 privat | 204.115.006 Bytes | 192.712.182 Bytes |
| 0.7.2 privat | 183.037.438 Bytes | 171.670.185 Bytes |
| 0.7.2 öffentlich | 178.166.519 Bytes | 166.806.808 Bytes |

Private APK: **21.077.568 Bytes kleiner (10,326 %)**. Öffentliche APK: **25.948.487 Bytes kleiner (12,713 %)** als der private Ausgangsstand. In der privaten APK sank der gespeicherte Grafikanteil von 44.084.738 auf 22.550.893 Bytes. Sprachinhalte und Variantenmetadaten änderten sich ebenfalls; dies ist kein isoliertes PNG-Experiment. Vollständige Ausgangs-/Ergebnisgruppen und Differenzen: [size-comparison.json](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/size-comparison.json).

## Noch offen

- Handy-Installation, Touchziele, Drehung in beide Richtungen, Unterbrechung/Aufwecken, Lautsprecher/Bluetooth und Audiofokus. Software-Renderings ersetzen diese Prüfungen nicht.
- Muttersprachliche Hörabnahme DE/EN/RU, besonders kurze Fächer, Zahlen, Wortenden und deutsche Lernsequenzen; auffällige ASR-Stellen gezielt hören. Kein Nachweis, dass jedes Wort schon für jedes Kind klar ist.
- Fachliche/muttersprachliche Abnahme der Aufgaben und freiwillige Tests mit Kindern. 33 Sachfragen bleiben heuristisch schwach; benötigte Bilder und mögliche Fachzuordnungen stehen im Review. Keine personenbezogenen Daten erhoben, keine empirische Lernwirkung behauptet.
- Endgültige Paketkennung, dauerhafte Signierung, Datenschutz/Families/Zielgruppe, Altersfreigabe, Store-Eintrag und Play-Freigaben. AABs bleiben unsigniert; Uploadbereitschaft BLOCKIERT.
- Private Original-/Optimierungspacks separat sichern. Ältere Git-Historie und alte externe Artefakte sind nicht bereinigt; nur der neue öffentliche Quellschnappschuss ist ohne Git-Historie/privaten Pack.
- Remote-Actions müssen nach dem Push gesondert geprüft werden; lokale Ergebnisse sind kein Remote-CI-Ergebnis.

Keine Spielmechanik, Speicherbereinigung oder Lizenzdatei wurde verändert. Versions- und Auflösungsfixtures wurden absichtlich aktualisiert, eigenständige Regressionen ergänzt; Gründe stehen in den Phasencommits.
