# Tatsächlich ausgeführte Prüfungen: Kinderwelt 0.9.1

Stand: 23.10.2026 (Europe/Berlin). Diese Lieferung ersetzt die deutschen und russischen Männerstimmen vollständig durch dieselbe weibliche Qwen-Serena-Stimme und führt ein neu erzeugtes App-Icon ein. Aufgaben, Punkte, Familien-/Neutralfiguren und Spielwelten bleiben erhalten. Vorheriger abgeschlossener Prüfbericht: [0.9.0](test-report-v090.md).

## Bereits gemessene Sprachstichprobe

Unabhängiges Whisper-small/int8-Screening ohne Referenz-Prompt: 31 feste Aufnahmen je Sprache. Der geänderte englische Geografie-Clip wurde nach der tatsächlichen finalen Erzeugung zusätzlich geprüft und sein altes Ergebnis ersetzt. Eine deutsche Zählansage wurde gezielt neu erzeugt und erneut gemessen; alle übrigen Vergleichsdateien sind anhand ihres tatsächlichen SHA256 zugeordnet.

| Sprache | Zeichenabweichung |
|---|---:|
| Deutsch | 2,487 % |
| Englisch | 2,522 % |
| Russisch | 2,805 % |

Rohtexte, Hashes und ASR-Modellhashes: [speech-female-v091.json](qa/speech-female-v091.json). Unterschiedliche Zahlenschreibungen und „Geografie/Geographie“ zählen ebenfalls als Abweichungen. Es handelt sich weder um eine Vollprüfung aller gesprochenen Wörter noch um eine menschliche Hörfreigabe. Einige Zuordnungen teilen dieselbe Aufnahme.

Die tatsächlichen reinen Ansagen werden klar erkannt: beispielsweise „Physik“, „Hier entdecken wir die Chemie“, „Это физика“, „Это химия“ und jetzt auch „Geography“. Neue weibliche Modellstimme statt Pitch-Anhebung oder unverständlicher englischer Phonemübertragung. Details zu Herkunft, vollständigen Wellenformen und offenen Hörprüfungen: [Stimme](voice.md).

## Vollständiger Quellstand und ausgeführte Regression

Alle Sprachbanken sind vollständig: je 1947 Zuordnungen, mit 904 deutschen, 903 englischen und 912 russischen eindeutigen Aufnahmen. Die alten deutschen und russischen Männeraufnahmen sind entfernt. Modellkarten, Lizenztexte, Sprecherinnen und SHA256 stimmen mit der festgehaltenen Herkunft überein. Alle festgeschriebenen Qwen-Gewichte, Tokenizer, Konfigurationen und Notices wurden zusätzlich gegen die tatsächlich lokal verwendeten Dateien geprüft.

- `GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=family bash tests/run.sh`: Exit 0. **88 Python-Tests bestanden**, einschließlich vollständiger realer Decodierung aller **2719** Sprachdateien. Hash, Dauer, Stille an beiden Rändern, unveränderte vollständige Quellwellenform-Metadaten und kalibrierte Pegelreserve geprüft.
- Godot: **6056** Aufgabenprüfungen, **3608** Weltenprüfungen, **991** Punkteprüfungen; echter Prozessneustart zeigt wieder 3360 Punkte und vergibt keine doppelten Belohnungen. Produktionsstart und frischer Import ausschließlich der ausgelieferten App-Dateien: jeweils 60 Frames, geregelter Audioabschluss.
- Reale Godot-Mixerprüfung: **36** Wiedergabe-, **75** Sequenz- und **38** Weltsprachprüfungen, jeweils ohne Fehler. Vollständige Dauer, richtige Reihenfolge, Musikabsenkung, Unterbrechungen, fortbestehender Lautstärkeabgleich beim Reglerwechsel und Pegelreserve geprüft. Messdaten: [Wiedergabe](qa/speech-playback-v091.json), [Sequenzen](qa/speech-sequences-v091.json), [zusätzliche Pegelmessung](qa/voice-levels-v091.json). Android-Unterbrechungen werden dabei simuliert.
- Neutrale Variante separat vorbereitet, importiert und durch `tests/boot.gd` geprüft: ebenfalls 60 Frames und sauberer Audioabschluss. Eine zweite vollständige Suite für diese Variante wurde in diesem Schritt nicht ausgeführt.
- Grafische Suite bereits ausgeführt: **461 echte OpenGL-Bilder** mit Familienfiguren, vier Displayprofilen und drei Sprachen; Punkteheader, Boni, Aufgaben, Welten, Figuren/Looks, Rotation und Menüs bestanden. Kein neuer Renderdurchlauf nach dem abschließenden Austausch ausschließlich der Audiodateien.
- Herkunftsprüfung: 24 Quellen und 14 aktive Figuren-PNG-Ressourcen geprüft, vier historische Figurenquellen gesperrt. Neues Icon einschließlich unverändertem Generierungsoriginal und dessen SHA256 nachgewiesen. Keine rechtliche Gesamtabnahme behauptet.
- Zwei neue Launcher-Tests encodieren/decodieren echte WebP-Bilder für APK-/AAB-Pfade und verwerfen vertauschte, fehlende beziehungsweise beschädigte Launcher-/Startressourcen. Die Toleranz wurde auch an bestehenden älteren Android-Archiven gegen deren damalige Bildquelle gemessen (maximale mittlere RGB-Abweichung 0,739 von 255); das neue Bild lässt diese alten Launcher bewusst durchfallen.
- Inhaltsreproduzierbarkeit, Lokalisierung, technische Quellprüfung und Hinweise aller 20 Musikstücke bestanden. Die bestehende Ablenkerheuristik markiert weiterhin 33 Grundaufgaben für menschliche Prüfung; Aufgaben wurden in diesem Schritt nicht geändert. Python-Syntax und `git diff --check` bestanden.

Beim ersten Import im vorhandenen Entwicklungsverzeichnis meldete Godot doppelte UIDs aus alten, lokal ignorierten `build/voice-*`-Vergleichsbanken. Der Test mit ausschließlich ausgelieferten Dateien hatte diese Verzeichnisse nicht. Lokal verhindert jetzt `build/.gdignore` deren erneutes Importieren; dieses lokale Hilfsmittel wird nicht ausgeliefert. Es gab keine Godot-Script-/Parse-Fehler im erfolgreichen vollständigen Lauf.

Zusätzlich wurden 48 weitere deutsche Zuordnungen mit derselben unabhängigen ASR geprüft: **1,050 %** Zeichenabweichung, mit tatsächlichen Dateihashes verknüpft ([Messdaten](qa/speech-female-additional-de-v091.json)). Eine neue Mondlicht-Aufnahme wurde dabei gezielt erneut geprüft; eine weiterhin abweichend erkannte Zahlenformulierung bleibt Teil der manuellen Hörprüfung.

## Android-Builds ausdrücklich zurückgestellt

Auf ausdrücklichen Nutzerwunsch wurden für diesen Quellstand **keine neuen APKs oder AABs gebaut**. Der Push-Commit enthält `[skip ci]`, damit auch GitHub keine automatischen Push-/PR-Android-Exporte startet. Kein manueller Workflow wurde für diesen finalen App-Quellstand ausgelöst. Daher liegen keine neuen Paket-, Signatur-, Installations- oder Geräteprüfungen für Version 0.9.1 vor. Vorhandene ältere 0.9.0-Dateien sind keine Artefakte dieser Änderung.

Die Android-Prüfskripte und ihre Regressionen sind vorbereitet; ihre Prüfung an einem tatsächlich neu exportierten Paket folgt erst beim später angeforderten Build.

## Manuell offen

Weicher Höreindruck und wahrgenommene Ähnlichkeit zur englischen Referenz, muttersprachliche Hörfreigabe insbesondere für Buchstaben, Verneinungen und Zahlen, Mischung mit Musik, reale Android-Lautsprecher/Bluetooth/Audiofokus sowie Installation als Update mit erhaltenem Punktestand. Der Testkanal `v090` bleibt bestehen und die Anzeigenversion steigt auf 0.9.1 / Code 14. Die vertrauenswürdige Push-Pipeline verwendet den bisherigen branchbezogenen Entwicklungsschlüsselcache; dessen dauerhafte Verfügbarkeit ist nicht garantiert. Keine Release-Schlüssel, keine geänderten Google-Play-Freigaben, kein Wirksamkeitsnachweis.
