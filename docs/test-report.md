# Ausgeführte Prüfungen

Stand: 20. Oktober 2026. App-Quellcommit: `19b2d2e5359e0cd465040684c31bb59784f11c4d`. Die aktuellen App-Dateien stimmen per SHA256 mit der isolierten Exportkopie überein. Spätere Änderungen an Prüfwerkzeugen und Bericht beeinflussen diese App-Dateien nicht.

## Ergebnisse

- **397 Funktionsprüfungen bestanden:** unabhängige Lösungen aller 24 Aufgaben, falsche Antworten, sichere Zahlen-/Datentypen, einmalige Sterne, lokale Speicherung, sichtbare Figurenauswahl, tatsächliche Touch-Eingaben, Bewegung bis zur Station, drei Fachwechsel, vier normale Bildschirmformate plus simulierte hohe Dichte, Hilfen, Audio-Wiederholung und Ducking, zehn ladbare Musiktitel und Favorit, Menü-Scroll-Regression.
- **24 Python-Tests bestanden:** Exportfehler-Diagnose, negative Manifest-/Payload-/ELF-Fälle, alle erforderlichen Ressourcen, zehn Musikstücke, 52 tatsächlich dekodierte Sprachclips, Dateihashes, Sprachpegel ohne übersteuerte Spitzen sowie Größenkategorisierung einschließlich Godot-Fontdateien.
- **Regulärer und cachefreier Start bestanden**, jeweils 60 Frames. Die cachefreie Kopie enthält ausschließlich App-Dateien und benötigt keine weiteren Projektteile.
- **144 echte Godot-Renderings bestanden:** alle 24 Aufgaben, Erfolge, vier Figuren-/Animationszustände, Musikbox und Einstellungen auf vier Anzeigeprofilen. Native Android-Grafiktreiber wurden hier nicht ausgeführt.
- Begrenzte Quellprüfung: keine Laufzeit-Netzwerkaufrufe oder aktivierten Android-Berechtigungen gefunden. Das ist keine umfassende Sicherheitszertifizierung.
- APK und AAB beider Paketvarianten technisch **PASS**: Paket, Version 0.5.0/5, API 24–36, keine Berechtigungen, Backup deaktiviert, Rotation, vollständige Medien, ARM64/x86_64, 16-KB-ELF-/ZIP-Ausrichtung, gültige APK-Entwicklungssignatur, Bundletool und unsignierter AAB-Status. Font-Lizenz und Modellkarte sind enthalten. Keine privaten Schlüssel im Paket oder Repository.

Der Remote-Status von GitHub Actions konnte wegen **Forbidden** beim API-Abruf nicht gelesen werden; es wird kein bestandener Remote-Lauf behauptet. Die hier dokumentierten Prüfungen wurden lokal tatsächlich ausgeführt.

Die aktuell gespeicherten Ergebnisdaten und SHA256-Nachweise stehen in [test-evidence.json](test-evidence.json). Die Exportprotokolle enthalten keine ADB- oder Godot-Fehler. Das reine Build-Preset startet keine angeschlossene Gerätesuche.

## Erzeugte Dateien

| Variante | Speicherort | Bytes | SHA256 |
|---|---|---:|---|
| Standard | `build/android-delivery/kinderwelt-debug.apk` | 84,117,406 | `d0d02573951ef251c0430540b98136ec1df0b7062f740e32b1b4fbf3eb805910` |
| Standard | `build/android-delivery/kinderwelt-unsigned.aab` | 73,702,869 | `32102725a1ce0163f43a8f2f018ee85481f04aaca68c3aa5e357e647cc352f60` |
| Testpaket | `build/android-delivery-test/kinderwelt-debug.apk` | 84,117,442 | `945a67183e1d03a3ba9ac5273d825b321678a264b7bcbf3b0cf58cb40509e1b9` |
| Testpaket | `build/android-delivery-test/kinderwelt-unsigned.aab` | 73,702,909 | `6130d058bb9cef8957bebb06866e4474f010d4553fea9ac5a3a9bd7af41053c4` |

Die Standard-APK ist rund 84,1 MB groß, das Standard-AAB rund 73,7 MB. Das ist die Archivgröße, weder der installierte Platzbedarf noch eine gemessene gerätespezifische Play-Downloadgröße. Das Testpaket heißt auf dem Gerät **Kinderwelt 0.5 Test** und hat einen eigenen lokalen Spielstand.

## Sichtprüfung und Grenzen

Die Sichtprüfung erfolgte stichprobenartig an tatsächlichen Godot-Bildern: Figurenauswahl mit Leuchteffekten, Spielweg, Mengenaufgabe, Ergänzung bis zehn, Reim, Muster, Vergleich im Querformat, Erfolg, Musikbox und Einstellungen. Ausgewählte Bilder stehen in [screenshots](screenshots/). Dabei gefundene weiße Texturflächen, gestörte Sprite-Teilpositionen, zu dünne Schrift und ein verdeckter Menü-Rückweg wurden vor der Lieferung korrigiert.

**Offen:** echte Android-Installation, Hörverständlichkeit/Aussprache, Bedienung durch ein Kind, physische Safe-Areas und Gesten, Geräteperformance, Unterbrechungen unter realem Speicherdruck und fachlicher Sofatutor-Abgleich. Es wurden keine Kinder beobachtet oder personenbezogene Daten erhoben. Die fachliche Gestaltung ist eine Hypothese; Lernwirkung und vergleichbare Attraktivität zu führenden Play-Spielen sind nicht nachgewiesen. Release-Signatur, Store-Freigaben und Google-Play-Upload bleiben offen.
