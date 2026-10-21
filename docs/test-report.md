# Tatsächliche Prüfungen und Android-Artefakte – 0.8.0

Stand: 21. Oktober 2026. [Neue Welten und Bedienung](worlds-v080.md), [vorheriger Stand 0.7.3](test-report-v073.md).

## Ausgeführt und bestanden

- Private und isolierte öffentliche Figurenvariante: vollständige bestehende Suite mit jeweils **6.085 Godot-Spielprüfungen**, **3.604 neuen Weltprüfungen**, **130 tatsächlichen Audiobusprüfungen** (30 bisherige, 66 mehrsprachige Folgen, 34 neue Welthinweisprüfungen), frischem Import/60-Frame-Start sowie **62 Python-Tests**.
- Nach der abschließenden Fahrer-Darstellung wurden die erweiterten **3.608 Weltprüfungen je Variante** erneut bestanden. Das zusätzliche Kriterium prüft, dass die Karosserie die Füße verdeckt. Alle früheren Weltprüfungen bleiben enthalten. Für diese letzte Darstellungsänderung wurden die übrigen, bereits bestandenen Prüfungen nicht wiederholt.
- Abschließend **383 echte Godot-Bildaufnahmen je Variante** auf vier Profilen: 320×568, 360×800, 800×360 sowie 1080×2400 mit simulierter Dichte 420 dpi. Sieben Kulissen, Szene nach Aufstieg auf einen Ast, animierte Folgebilder, Bildauswahl, ursprüngliche Aufgaben, Sachfragen-Stichproben, Figuren/Looks, Sprachen, Punktestand und Rotation. Software-OpenGL/Mesa, keine Smartphone-Messung. Ausgewählte öffentliche Aufnahmen: `docs/screenshots/worlds-v080-*`.
- Echte simulierte Berührungen erreichen alle acht Kulissenoptionen in DE/EN/RU auf vier Profilen; getrennte Fachwerte überstehen den Dateispeicher. Für jede der sieben Welten werden sämtliche 40 Mathe-Stationen auf allen vier Profilen in den sichtbaren Bereich gebracht und öffnen ihre eigene Aufgabe. Die bisherige Suite prüft weiterhin die Logik aller acht Fächer und aller 320 Aufgaben.
- Alle **1.645 unterschiedlichen Sprachaufnahmen** und **20 Musikstücke** vollständig mit FFmpeg decodiert. Hashes, Dauer, stille Ränder und Pegel geprüft. Alle bisherigen Sprachaufnahmen/Manifestzeilen, Aufgaben-JSON und Musikmanifest sind gegenüber 0.7.3 unverändert; zwölf neue Welthinweise ergänzt.
- Unabhängiges ASR-Screening der vier neuen Hinweise je Sprache, ohne Textvorgabe: nach vereinfachter Formulierung DE **2,564 %**, EN **2,778 %**, RU **4,867 %** Zeichenabweichung. Erste Formulierungen: 8,219 / 4,560 / 8,917 %. Unterschiedliche Referenztexte; kein kontrollierter Hörvergleich und keine menschliche Verständlichkeitsfreigabe. Insbesondere „Nüsse“, „орех у белки“ und einzelne Verben bleiben durch Menschen zu hören.
- Offline-Hörseite mit **54 Proben**, einschließlich aller neuen Hinweise, erzeugt; eingebettete Wiedergabesequenzen und JavaScript-Syntax geprüft. Kein Netzwerk, keine Aufnahme oder Bewertungsspeicherung. Browser-/Hörprüfung bleibt manuell.

Die bisherigen Audiotests setzen ausdrücklich die Bergkulisse, damit sie reine Fachansagen prüfen; ein eigener Test erfasst die zusätzlich vollständigen Welthinweise. Das bisherige Zeitlimit wurde nicht erhöht. Im ersten Durchlauf lief der alte Test wegen des zusätzlichen Hinweises in sein Zeitlimit. Die Fälle werden jetzt getrennt tatsächlich am Mixer geprüft.

Rohprotokolle, Daten und Quellenvergleich: `docs/qa/v080-*`. Alle Tests liefen lokal; Remote-CI ist **nicht verifiziert**, die GitHub-API-Abfrage lieferte erneut `Forbidden`.

## Tatsächlich erzeugte Dateien

| Variante | Lokaler Pfad | Bytes | MB dezimal |
|---|---|---:|---:|
| family | `build/android-v080-family/kinderwelt-debug.apk` | 185,906,124 | 185.906 |
| family | `build/android-v080-family/kinderwelt-unsigned.aab` | 174,523,158 | 174.523 |
| public | `build/android-v080-public/kinderwelt-debug.apk` | 181,035,213 | 181.035 |
| public | `build/android-v080-public/kinderwelt-unsigned.aab` | 169,659,784 | 169.660 |

Version **0.8.0 / Code 11**. APKs sind mit temporären Godot-Entwicklungsschlüsseln signiert; beide AABs sind **unsigniert**. Keine Release-Schlüssel eingesetzt. Diese Vorschauen haben eigene Paketkennungen `org.example.kinderwelt.preview.family.v080` und `org.example.kinderwelt.preview.neutral.v080` und getrennte lokale Spielstände. Vorherige Testinstallationen können daneben bestehen; deren Spielstände werden nicht automatisch zwischen Paketen übertragen. Bei einem Update mit identischer Paketkennung und kompatibler Signatur übernimmt das Speicherschema 4 die alte Kulissenwahl und erhält bekannte Lösungen/Figuren/Looks.

Alle vier Artefakte bestanden: ZIP-/APK-/Bundle-Format, erwartete Paketkennung/Version, deklarierte Spieldaten und sämtliche Sprach-/Musik-/Grafikressourcen einschließlich des neuen gemeinsamen Atlas und der Welt-/Auto-Skripte, API **24–36**, keine Berechtigungen, Backup aus, Rotation `fullUser`, `arm64-v8a` und `x86_64`, 16-KB-ELF- sowie APK-ZIP-Ausrichtung. APK-v2-Signaturen geprüft, AABs mit Bundletool validiert und unsignierter Status bestätigt. Hier auf keinem echten Android-Gerät installiert.

### Quellen

Privater Build aus sauberem Quellcommit `22b44cf040086846d609c8a9878a2704119012a2`, ohne beobachtete Statusänderung während des Builds. Öffentlicher Build tatsächlich aus `build/public-source-v080-verified/` ohne eigenes Git-Repository oder privaten Figurenpack. Provenienz meldet dort korrekt `unversioned-snapshot`, `source_commit=null`, `source_dirty=null`. Beide Varianten dokumentieren den tatsächlichen Hash des materialisierten App-Verzeichnisses. Nachfolgende Nachweisänderungen betreffen Dokumentation; App-Code und Ressourcen sind identisch zum gebauten Stand.

### SHA256

| Datei | SHA256 |
|---|---|
| family/kinderwelt-debug.apk | `3d2fd2851a80ec8875785e4ef0a24bfbbe4c73a7040fab126486d0a73145f95b` |
| family/kinderwelt-unsigned.aab | `e7f69533b2538241d536d54d0e51794f993834b400fcf0d130af7802e4da2f56` |
| public/kinderwelt-debug.apk | `137bc0463ff4054df5dc772dbcc462a8938dcaa8d401294c5b82eb44f5c9e1e5` |
| public/kinderwelt-unsigned.aab | `daa3a93ac9526943f6b06e6b64542e58385af55db9c2f8d3483cef442403015f` |

## Tatsächlicher Größenzuwachs

| APK-Variante | 0.7.3 Bytes | 0.8.0 Bytes | Zuwachs |
|---|---:|---:|---:|
| family | 183,085,862 | 185,906,124 | +2,820,262 / +1.54 % |
| public | 178,214,939 | 181,035,213 | +2,820,274 / +1.58 % |

Vier neue Hintergründe teilen sich eine einzige PNG-Quelldatei mit **2.915.177 Bytes**. Tiere verwenden vorhandene Grafiken; Auto, Äste, Nüsse und Stationen brauchen keine Bildfolgen oder Videos. Die APK bleibt bei rund 186 MB privat beziehungsweise 181 MB öffentlich. Dies sind Archivgrößen, keine Messung des installierten Speichers oder eines Play-Downloads. Detaillierte Gruppen und Hashes stehen in den Größenanalysen.

## Offen

Geräteprüfung: Kulisse für mindestens zwei Fächer unterschiedlich wählen und nach Neustart kontrollieren; am Baum höher klettern, alle vier Seiten erreichen, Truhe/Brückenaufgabe lösen; im Hoch-/Querformat bleiben Steuerung und Punkte getrennt; Stummschaltung, reduzierte Bewegung, Audio-Unterbrechung/Resume und Telefonlautsprecher prüfen. Bildrate, Akkubelastung, Wärme und installierter Speicher wurden nicht am Gerät gemessen.

Muttersprachliche Hörabnahme, fachliche/kindliche Bedienungsprüfung und empirische Lernwirkung bleiben offen. Diese Prüfungen erfassen keine Nutzerprofile oder Tonaufnahmen. Endgültige App-ID, dauerhafte Signierung, Datenschutz/Families/Zielgruppe, Altersfreigabe, Store-Eintrag und Play-Freigaben bleiben offen; **Uploadbereitschaft BLOCKIERT**. Ältere private Grafiken bleiben in der bisherigen Git-Historie; ein öffentlicher Quellschnappschuss enthält keine Historie oder privaten Grafikpack.
