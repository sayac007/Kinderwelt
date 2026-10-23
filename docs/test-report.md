# Tatsächlich ausgeführte Prüfungen: Kinderwelt 0.9.0

Stand: 23.10.2026 (Europe/Berlin). Implementierung: [Punkte, native Lerninhalte und Boni](rewards-native-learning-v090.md). Vorherige Ergebnisse: [0.8.1](test-report-v081.md). Kein Nachweis pädagogischer Wirksamkeit, keine Google-Play-Freigabe.

Alle 320 Grundfragen wurden in allen drei Sprachfassungen gegen den zuvor ausgelieferten Stand geprüft: vollständig ersetzt. 40 neue Aufgaben je Fach plus je zwei freiwillige Boni; 200 unterschiedliche neue Sachfragen je Sprachfassung. Mathe, Sprache und Logik haben jeweils 40 unterschiedliche Rätselkonfigurationen. Frühere Erfolge bleiben im Archiv, neue Aufgaben werden erneut belohnt. Die beabsichtigte höhere Schwierigkeit wurde nicht empirisch nachgewiesen.

## Technische Prüfungen

- Vollständige Suite `tests/run.sh`: bestanden für Familien- und neutrale Variante (jeweils 84 Python-Tests); keine Godot-Fehler im erfolgreichen Lauf. Die abschließende Rechtschreibkorrektur wurde zusätzlich durch alle 84 Python-Tests samt vollständiger Audiodatei-Decodierung geprüft.
- Godot-Grundregression: 6056 Prüfungen; Welten: 3608; neue Belohnungsregression: 991. Neustartnachweis mit zwei echten Prozessen: 3200 + 10 + 50 + 100 = 3360 Punkte werden erneut angezeigt, keine doppelten Belohnungen.
- Produktionseinstieg und frischer Import ausschließlich der ausgelieferten App-Dateien; jeweils 60 Frames und geregelter Audioabschluss.
- Reale Audio-/Unterbrechungsprüfungen am Desktop-Mixer: 30 Wiedergabe-, 66 Sequenz- und 34 Weltsprachprüfungen. Android-Benachrichtigungen werden simuliert; dies ist kein Gerätetest.
- Python-Regressionen: 84 Tests einschließlich nativer Buchstabenrekonstruktion, Bonusgleichungen, kyrillischer UI und aller 2719 einzigartigen tatsächlich decodierten Ogg-Sprachdateien (1947 Zuordnungen pro Sprache). Hash, Dauer, Pegel und Anfang/Ende werden überprüft; außerdem alle 20 Musiktitel und deren Quellen/Lizenzen.
- Grafische Suite: 461 echte OpenGL-Bilder, vier Displayprofile (320×568, 360×800, 800×360 und 1080×2400), drei Sprachen, beide Bonusstufen, Maximalstand 54.400, kombinierte Bild-Zahlen-Regeln, Reihenfolgen und bestätigte alte Punkteübernahme, Rotation, bisherige Figuren/Looks/Welten/Menüs. Die Bilder eines Hörrätsels bleiben beim Wechsel des früheren Lösungsobjekts Ohr → Mond identisch. Manuell betrachtet wurden ausgewählte kleine und breite Ansichten; keine vollständige manuelle Bildfreigabe behauptet.
- Actionlint 1.7.7, Inhaltsgenerator-Reproduzierbarkeit, Figurenherkunft, Lokalisierungs-/Ablenkerbericht und Lizenzhinweise geprüft. Die Ablenkerheuristik markiert weiterhin 33 Grundaufgaben; menschliche Prüfung bleibt offen.

## Stimme

Der gewünschte gemeinsame weibliche Sprecher für alle Sprachen ist offen. Verworfen wurde eine Umwandlung, die die deutsche Aussprache verschlechtert; die nativen DE/RU-Stimmen bleiben erhalten. Unabhängiges Whisper-small-Screening ohne Referenz-Prompt auf den tatsächlich ausgelieferten Aufnahmen:

| Stichprobe | Deutsch | Englisch | Russisch |
|---|---:|---:|---:|
| 31 feste Aufnahmen je Sprache | 5,950 % | 3,359 % | 10,464 % |
| 8 zusätzliche Clip-Zuordnungen je Sprache | 10,969 % | 1,337 % | 5,495 % |

Werte sind Zeichenfehlerraten; sie messen ASR-Abweichungen und zertifizieren kein kindliches Verständnis. Zum Beispiel werden einzelne russische Fachwörter und deutsche Bonusformulierungen fehlerhaft erkannt; diese bleiben im Hörreview gezielt zu prüfen. Manche Bonus-Zuordnungen teilen dieselbe Aufnahme. Die Stichproben sind keine statistisch unabhängige Abdeckung aller Dateien. Messdaten und Hashes: `docs/qa/speech-advanced-recognition-v090.json`, `docs/qa/speech-advanced-additional-v090.json`. Die Artefakte enthalten `kinderwelt-listening.html` mit 78 abspielbaren Offline-Proben.

## Android-Artefakte

Finale lokale Builds: `build/android-v090-complete/`. Tatsächliche Dateigrößen und SHA-256 stehen in `docs/qa/android-v090-delivery.json`. Beide Varianten sind separat installierbar; Version 0.9.0, Code 13.

| Datei | Größe (MiB) | Signatur |
|---|---:|---|
| `kinderwelt-debug-family.apk` | 212.28 | Entwicklung |
| `kinderwelt-unsigned-family.aab` | 200.75 | **UNSIGNIERT** |
| `kinderwelt-debug-neutral.apk` | 207.63 | Entwicklung |
| `kinderwelt-unsigned-neutral.aab` | 196.11 | **UNSIGNIERT** |

Geprüft: ZIP/APK/AAB-Struktur, vollständige App-/Audio-/Grafikdateien und Abgleich mit den getesteten Quellen, Paket/Version, minSdk 24, targetSdk 36, keine Berechtigungen, Backup deaktiviert, `fullUser`-Rotation, GL Compatibility, arm64-v8a/x86_64, 16-KB-ELF-/ZIP-Ausrichtung, APK-v2-Signatur und exakter Zertifikatsfingerabdruck; Bundletool-Validierung und ausdrücklich unsignierte AABs. Keine Release-Schlüssel verwendet.

Ab 0.9.0 ist der Vorschaukanal unabhängig von der Versionsnummer. Lokal wiederverwendeter Entwicklungsschlüssel; CI verwendet einen privaten, aber löschbaren Actions-Cache. Ein Cache ist kein dauerhaft zugesicherter Signierspeicher. Die alten 0.8.1-APKs hatten flüchtige Schlüssel. Die neue App wird parallel installiert; alte Paket-Spielstände werden nicht automatisch kopiert. Details: [Android bauen](android.md).

Die geprüften lokalen Exporte stammen aus einem sauberen Quellstand; Commit und Inhalts-Hashes stehen in den beigefügten Provenienzberichten. Die letzte Korrektur betrifft „Fußabdruck“ als übliche Schreibung zum gültigen Großbuchstaben-Lernwort „FUSSABDRUCK“.

## GitHub und offene Prüfungen

Der Branch `feat/rewards-native-learning` basiert auf `origin/main` einschließlich gemergtem PR #10. GitHub-Lauf, Ergebnis und Downloadlink werden im Pull Request und in den Actions-Artefakten ausgewiesen; ein lokaler Erfolg ist kein Beleg eines bereits erfolgreichen Remote-Laufs.

Offen: Hörfreigabe und gemeinsamer weiblicher Sprecher, Muttersprachler-/Fachreview aller neuen Bonus- und Rätseltexte, echte Android-Geräte-/Updateprüfung, kinderspezifische Usability und empirische Evaluation. Keine personenbezogenen Daten neu erfasst. Endgültige App-ID, Release-Signierung und Google-Play-Freigaben bleiben offen.
