# Tatsächliche Prüfungen und Android-Artefakte – 0.7.3

Stand: 21. Oktober 2026. [Änderungen und Messgrenzen](experience-polish-v073.md); [vorheriger geprüfter Stand 0.7.2](test-report-v072.md).

## Ausgeführt und bestanden

- Privater und isolierter öffentlicher Stand: jeweils **6.085 Godot-Spielprüfungen**, **30 bisherige plus 66 zusätzliche Audiolaufprüfungen**, frischer Import/60-Frame-Start und **61 Python-Tests**.
- Abschließende Python-Suite erneut vollständig im privaten Stand und im tatsächlich zum Bauen verwendeten öffentlichen Quellschnappschuss bestanden. Der Git-Regressionsfall wurde zusätzlich mit einem sauberen Elternrepository und ignoriertem Schnappschuss geprüft.
- Alle **1.633 unterschiedlichen Sprachdateien** und **20 Musikstücke** vollständig mit FFmpeg decodiert; Hash, Dauer, Pegel und stille Ränder geprüft.
- Konkreter gefundener Fehler: neuer englischer Auswahlclip überschritt nach Vorbis-Decodierung mit 1,030925 die Pegelgrenze. Ungültiger Cache verworfen, Clip neu erzeugt und nach Decodierung geprüft; kein Testlimit gelockert. Eigener echter Codec-/Cachetest ergänzt.
- Mehrsprachige Folge aus lokalisierter Erklärung, vollständiger deutscher Aufnahme und anschließendem Lob am tatsächlichen Godot-Audiobus erfasst. Ressourcenreihenfolge, Sampledauer, simulierte Pause/Fortsetzung, Stummschaltung und Musikabsenkung geprüft. Desktop-Mixerprüfung, kein Android-Gerätetest.
- Feste ASR-Stichprobe: 31 Beispiele je Sprache, ohne Referenzvorgabe; **DE 4,189 %, EN 1,987 %, RU 7,464 %** Zeichenabweichung. EN zuvor 3,617 %, teilweise mit anderen Ansagetexten; kein kontrollierter Hörvergleich. Russische Variante mit 9,281 % verworfen. DE/RU-Manifestbytes und Audiohashes sind unverändert.
- Offline-Hördatei mit 42 Proben aus den tatsächlich ausgelieferten Dateien erzeugt; JavaScript-Syntax geprüft. Browser-/Hörabnahme bleibt manuell.

Rohprotokolle und JSON-Berichte: `docs/qa/v073-*`. Es wurden keine erneuten 343 visuellen Renderings für diese Iteration ausgeführt; Figuren, Kulissen, Aufgaben, Layout und Speicherlogik wurden unverändert übernommen. Die Einstellungen zeigen die neue Version.

## Tatsächlich erzeugte Dateien

| Variante | Lokaler Pfad | Bytes | MB dezimal |
|---|---|---:|---:|
| family | `build/android-v073-family/kinderwelt-debug.apk` | 183,085,862 | 183.086 |
| family | `build/android-v073-family/kinderwelt-unsigned.aab` | 171,708,612 | 171.709 |
| public | `build/android-v073-public/kinderwelt-debug.apk` | 178,214,939 | 178.215 |
| public | `build/android-v073-public/kinderwelt-unsigned.aab` | 166,845,218 | 166.845 |

APKs sind mit temporären Godot-Entwicklungsschlüsseln signiert; beide AABs sind **unsigniert**. Die APKs wurden hier auf keinem echten Android-Gerät installiert. Vorschauen verwenden eigene Pakete `org.example.kinderwelt.preview.family.v073` und `org.example.kinderwelt.preview.neutral.v073`; vorhandene 0.7.2-Installationen können daneben bestehen, mit getrennten lokalen Spielständen. Die Basiskennung bleibt konfigurierbar und vorläufig. Keine Release-Schlüssel oder Play-Freigaben wurden geändert.

Alle vier Dateien bestanden: ZIP-/APK-/Bundle-Struktur, deklarierte Inhalte und sämtliche Sprach-/Musik-/Grafikressourcen, Version **0.7.3 / Code 10**, richtige Figurenvariante/Paketkennung, API **24–36**, keine Berechtigungen, Backup aus, Rotation `fullUser`, `arm64-v8a` und `x86_64`, 16-KB-ELF-Ausrichtung und APK-ZIP-Ausrichtung. APK-v2-Signatur geprüft; AAB mit Bundletool validiert und unsignierter Status bestätigt.

### Quellen und Build ohne Git-Historie

Privater Build aus sauberem Git-Quellcommit **`198cd1d92e3cb853fa87fa0097d90b765b2b6749`**, ohne beobachtete Git-Statusänderung während des Builds. Die anschließenden Nachweisänderungen betreffen Dokumentation und die zusätzliche Git-Testfixture; App-Code und ausgelieferte Ressourcen bleiben identisch.

Der öffentliche APK-/AAB-Build wurde **tatsächlich aus `build/public-source-v073-build/` ohne eigenes `.git` und ohne privaten Grafikpack ausgeführt**. Alle 61 Python-Tests bestanden auch dort. Provenienzformat 2 meldet korrekt `unversioned-snapshot`, `source_commit=null` und `source_dirty=null`, statt den Eltern-Git-Stand zu übernehmen. Beide Builds dokumentieren den tatsächlichen Inhalts-Hash des materialisierten App-Verzeichnisses. Der Schnappschuss stammt aus dem obigen Quellcommit; Produzentenmetadaten sind von einer eigenen Git-Verifikation getrennt.

Die Paketprüfung und vollständige Android-Exportkette liefen für beide Varianten; die Gitlosigkeit ist durch den tatsächlichen Build geprüft, nicht nur durch einen Mock. [Buildbefehle und Voraussetzungen](android.md).

### SHA256

| Datei | SHA256 |
|---|---|
| family/kinderwelt-debug.apk | `c35b5aadecc8cc758cb840a3c2bac8da10c656ec5feece7922bc5255034d87df` |
| family/kinderwelt-unsigned.aab | `fc4899938d14e2d154b04dec71fe64935b30dee8a16c4ed59972b47970b7305c` |
| public/kinderwelt-debug.apk | `2bd4733541453821d1a5078182174b891ccb9679b7386cdeb104389269dba564` |
| public/kinderwelt-unsigned.aab | `0b44901bd73f1d47a64a992ab4f9c8775dddcab7650a348ad7515b6a45807027` |

## Größenvergleich

| Stand | Private APK | Öffentliche APK |
|---|---:|---:|
| 0.7.2 | 183.037.438 Bytes | 178.166.519 Bytes |
| 0.7.3 | 183.085.862 Bytes | 178.214.939 Bytes |

Der neue Stand enthält aktualisierte Sprachdateien und Metadaten. Archivgröße, nicht installierter Speicherbedarf oder Play-Download. Originaler privater 0.7.1-Ausgangsstand: 204.115.006 Bytes. Detaillierte Gruppen und Dateihashes in `v073-family-size-analysis.json` und `v073-public-size-analysis.json`.

## Offen

Muttersprachliche und kindliche Hörverständlichkeit, insbesondere deutsche „Chemie“, Wortgrenzen und russische Auswahlwörter. Die Offline-Hördatei erleichtert die manuelle Abnahme und erfasst keine Bewertungen, Namen oder Tonaufnahmen. Smartphone-Lautsprecher/Bluetooth, Musikbalance, Touch, Drehung, Android-Audiofokus und Aufwecken sind noch am Gerät zu prüfen.

Fachliche/muttersprachliche Aufgabenfreigabe, freiwillige Kinderbeobachtung und empirische Lernwirkung bleiben offen. Endgültige App-ID, dauerhafte Signierung, Datenschutz/Families/Zielgruppe, Altersfreigabe und Store-/Play-Freigaben stehen aus; **Uploadbereitschaft BLOCKIERT**. Ältere private Grafiken bleiben in der bisherigen Git-Historie; der getrennte öffentliche Quellschnappschuss enthält keine Historie oder privaten Pack.

Die Remote-Actions-Läufe konnten wegen GitHub-API-Forbidden nicht eingesehen werden. Ein Push und lokale Testerfolge bestätigen keinen erfolgreichen Remote-Lauf.
