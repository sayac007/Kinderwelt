# Ausgeführte Prüfungen für Kinderwelt 0.6

Stand: 20. Oktober 2026. Wanja ist der fünfte spielbare Familiencharakter und vorausgewählte Hauptheld. Acht Fächer mit je 40 Aufgaben, drei Bedienungssprachen und vier klassische Klavierwiedergaben sind integriert.

## Tatsächlich ausgeführt

- **4.914 Godot-Prüfungen bestanden:** ursprüngliche 24 Lösungsfixtures, richtige/falsche Antworten aller 320 Aufgaben, einmalige Sterne, lokale Speicherung und Figurenmigration, echte Touch-Eingaben in alle acht Fächer, vier frei wählbare Wege je Fach, fünf Anzeigeformate einschließlich simulierter hoher Dichte, Hilfen und reale Audio-Ende-/Playlist-Steuerung. Alle **960 lokalisierten Aufgaben** wurden auf 320 × 568 bei großer Schrift auf abgeschnittene Titel und Überschneidungen geprüft.
- **32 Python-Tests bestanden:** ursprüngliche Inhalte, deterministischer Inhaltsgenerator, Übersetzungs-/Grafikverträge, Quell-/Audiodateihashes, tatsächliche PCM-Dekodierung aller **1.589 unterschiedlichen Sprachdateien** und vier Musikstücke, Dauer und Pegel, Exportfehler-Diagnose, negative Manifest-/Payload-/ELF-Fälle, korrekte Asset-Pack-Zuordnung und Größenanalyse.
- Regulärer und cachefreier Start der erlaubten App-Dateien jeweils über 60 Frames bestanden, einschließlich geordnetem Audio-Shutdown.
- **272 echte OpenGL-Renderings bestanden:** ursprüngliche 24 Aufgaben, 15 Sachaufgaben-Stichproben, acht Welten, letzte Wegseite, drei Sprachen, fünf Figuren in vier Animationszuständen sowie Musik und Einstellungen auf vier Anzeigeprofilen. Renderer: Desktop llvmpipe, keine native Android-GPU.
- Begrenzter Quell-/Berechtigungsaudit ohne Laufzeit-Netzwerkaufrufe oder aktivierte Android-Berechtigungen. Keine umfassende Sicherheitszertifizierung.
- Standard- und Testpaket **APK/AAB technisch PASS**: Paketkennung, Version **0.6.0 / 6**, API 24–36, Berechtigungsfreiheit, deaktiviertes Backup, Rotation, 3.287 erforderliche App-Ressourcen, fünf Figuren und Katzenshader, alle Sprach-/Musikdateien und Lizenzen, ARM64/x86_64, 16-KB-ELF-/ZIP-Ausrichtung, gültige APK-Entwicklungssignatur, Bundletool-Validierung und unsignierter AAB-Status. Aufgaben-/Sprachmanifeste und Modellkarten wurden zusätzlich byteweise mit den geprüften Quellen verglichen.

## Gefundene und behobene Fehler

Eine russische Überschrift war im kleinen Hochformat abgeschnitten. Die Anordnung wurde korrigiert; alle Sprachvarianten bei großer Schrift bestehen nun die Layoutprüfung. Die Paketprüfung fand außerdem fehlende Musiklizenztexte. Beide Exportfilter sind korrigiert und durch einen eigenen Regressionstest abgesichert. Die zusätzliche Inhaltsprüfung wurde an Godots tatsächliches `assetPackInstallTime/assets/` im AAB angepasst; Tests decken APK-, Base- und Install-Time-Verzeichnisse sowie manipulierte/fehlende/doppelte Daten ab.

## Tatsächlich erzeugte Dateien

| Variante | Datei | Bytes | SHA256 |
| --- | --- | ---: | --- |
| standard | `build/android-v06-verified/kinderwelt-debug.apk` | 134,111,498 | `d64a15c01d2d9a1d415d2cce4aa9def416438b77d91847c947fab290c50e459e` |
| standard | `build/android-v06-verified/kinderwelt-unsigned.aab` | 123,325,267 | `ba340066434aea88ad3014a74b77e5079e90e6838c8221eb63f9e3e9db301178` |
| preview | `build/android-v06-preview/kinderwelt-debug.apk` | 134,111,538 | `af1a06a123cebff496f8fdb2c63cd4c1b19501bed98d9e15e29cea0770f4eee6` |
| preview | `build/android-v06-preview/kinderwelt-unsigned.aab` | 123,325,303 | `c486bd65a9134d92fb943635f1ad29eac5904bd26b0fe1fc8795fa45128f8012` |

Das Standard-APK hat rund 134,1 MB, das AAB rund 123,3 MB. Dies sind Archivgrößen, kein installierter Platzbedarf und keine gemessene Play-Downloadgröße. Die Testvariante heißt **Kinderwelt 0.6 Test**, Paket `org.example.kinderwelt.preview`, mit eigenem lokalen Spielstand. Sie kann neben der Standard-App installiert werden. Beide APKs verwenden temporäre Godot-Entwicklungsschlüssel; eine bestehende Installation mit anderem Schlüssel lässt sich damit nicht direkt aktualisieren. Keine privaten Schlüssel werden mitgeliefert. Ein AAB ist nicht direkt installierbar und bleibt unsigniert.

Die Quell-Commits und SHA256 der isolierten Exportkopien stehen in [test-evidence.json](test-evidence.json). Beide Builds stammen aus sauberen Commits; die heutigen App-Dateien stimmen mit beiden Exportkopien überein (bei der Testvariante mit der dokumentierten Paket-/Namensänderung). Die spätere Korrektur des Datenprüfers änderte keine App-Dateien. Die zuerst wegen fehlender Lizenztexte abgewiesenen Dateien unter `build/android-v06` sind keine freigegebenen Testartefakte.

## Sichtprüfung, Download und Grenzen

Stichproben aus den tatsächlichen Renderings wurden betrachtet: Wanja/Familienauswahl auf kleinen Bildschirmen, Laufwelt mit neuem Fach, Physik im Hoch-/Querformat und russisches Silbenlernen. Aktuelle Bilder ersetzen die alten Figurenbilder vollständig unter [screenshots](screenshots/). Nicht alle 272 Bilder wurden einzeln manuell beurteilt.

Die vollständigen lokalen Testlogs liegen unter `/tmp/kinderwelt-06-complete-tests.log`, `/tmp/kinderwelt-06-render-final.log`, `/tmp/kinderwelt-06-android-preview.log` und `/tmp/kinderwelt-06-verify-corrected.log`. Die Standarddateien wurden aus `0df0b94` gebaut und nach der Datenprüferkorrektur erneut vollständig technisch verifiziert. Die Testvariante wurde aus dem korrigierten Prüfer-Commit gebaut. Ein direkter API-Abruf des Remote-CI-Status war mit **Forbidden** gesperrt; kein bestandener GitHub-Lauf wird behauptet.

**Offen:** Installation auf echten Android-Geräten, Safe-Areas/Touch/Swipe, Performance und Speicherbedarf, Audiopegel und Hörverständlichkeit. Deutsche/englische Stimmen sind weiblich, die lizenzierte russische Stimme ist männlich. Aussprache sowie die zweisprachige Abfolge deutscher Lernwörter müssen Muttersprachler anhören. Fachliche/altersspezifische Abnahme, Lehrplanabgleich anhand hier gesperrter Primärseiten und Tests mit Kindern/Erwachsenen stehen aus. Es wurden keine Kinder untersucht und keine personenbezogenen Nutzungsdaten erhoben. Keine nachgewiesene Lernwirkung, Marktreife oder Google-Play-Uploadbereitschaft. Release-Schlüssel, Store-Freigaben sowie YouTube-Titelzuordnung/SKIBIDI-Lizenz bleiben offen.
