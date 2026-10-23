# Sprachausgabe und reproduzierbare Testbuilds – 0.7.3

> Historischer Versionsbericht. Aktuelle Funktionen, Tests und offene Freigaben: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die folgenden Ergebnisse gelten ausschließlich für den genannten früheren Stand.

Die gewohnte Oberfläche, Figuren, Kleidung, Kulissen, alle 320 Aufgaben und die Speicherlogik bleiben erhalten. Diese Iteration verbessert englische Ansagen und die Prüfung der vollständigen Audiowiedergabe. Version 0.7.3 / Code 10 verwendet weiterhin vorläufige Testkennungen.

## Tatsächliche Audioänderungen

Englische Sachaufgaben nennen die Auswahl als zusammenhängenden Satz mit Kommas und „or“. Bisher wurden drei einzelne Einwortsätze synthetisiert. Die englische Logikansage lautet „This is logic.“. Alle 200 Auswahlfragen behalten ihre drei ursprünglichen Optionen und deren Reihenfolge.

Bei der vollständigen Decodierung fiel ein neu erzeugter Clip durch: Spitzenpegel **1,0309247** nach Vorbis-Decodierung, oberhalb des zulässigen Bereichs. Die bestehende Prüfung wurde nicht gelockert. Der Generator prüft nun auch zwischengespeicherte Aufnahmen auf hörbaren und sicheren Spitzenpegel; ein ungültiger Cache wird verworfen. Neue Vorbis-Ergebnisse werden erneut decodiert und bei Bedarf mit gleichmäßiger Absenkung aus der ursprünglichen WAV-Datei neu codiert. Zielwert neuer Dateien ≤0,95. Samples, Pausen und Wortdauer werden nicht gekürzt. Der betroffene Clip wurde neu erzeugt und mit Spitzenpegel **0,702619** angenommen. Ein eigener echter Vorbis-Test prüft Pegelreserve, vollständige Dauer und Cache-Ablehnung trotz passendem Dateihash.

Deutsch und Russisch bleiben einschließlich ihrer Manifestbytes und Audiohashes im zuvor gelieferten Stand. Orientierende deutsche Modell-/Tempovergleiche lieferten keinen verlässlichen Ersatz für Thorsten high. Die russische Satzvariante verschlechterte die feste ASR-Stichprobe von 7,464 % auf 9,281 % Zeichenabweichung und wurde verworfen. Auch eine kurze Dmitri-CC0-Vergleichsserie rechtfertigte keinen Wechsel der gesamten Sammlung. Keine Lizenzdatei wurde geändert.

Die erneute vollständige ASR-Stichprobe der ausgelieferten Dateien umfasst 31 feste Beispiele je Sprache: **DE 4,189 %, EN 1,987 %, RU 7,464 %**. EN zuvor 3,617 %. Die englischen Referenztexte sind teilweise geändert; dies ist kein kontrollierter Hörvergleich und keine kindliche Verständlichkeitsfreigabe. Alle Rohtexte und Dateihashes stehen unter [v073-asr.json](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/v073-asr.json); verworfene Versuche sind getrennt gekennzeichnet. Deutsche „Chemie“, einzelne Wortgrenzen und russische Auswahlwörter bleiben Hörprüfpunkte.

## Vollständige Folgen statt nur Dateidauer

Die echte Godot-Audiobusprüfung umfasst zusätzlich 66 Prüfungen: deutsche Frage oder Silbenhilfe, in EN/RU lokalisierte Erklärung mit vollständiger deutscher Folgeaufnahme, anschließend das bereits während der Frage angeforderte Lob. Sie prüft die tatsächlich geladenen Ressourcen in der richtigen Reihenfolge, abgegriffene Sampledauer und Musikabsenkung/-wiederherstellung. Simulierte Anwendungs-Pause darf keine Sprechzeit verbrauchen; Fortsetzen und Stummschaltung werden geprüft.

Beim Schreiben der Prüfung wurde ein Test-Rennen korrigiert: `playing=false` kann bereits vor Verarbeitung des `finished`-Signals sichtbar werden. Der Test wartet deshalb auch auf den abgeschlossenen Narrationszustand. Die bestehende App-Wiedergabe musste dafür nicht geändert werden. Zusammen mit den bisherigen 30 Prüfungen sind es **96 Audiolaufprüfungen**. Detaillierte JSON-Berichte werden von `tests/run.sh` automatisch unter `qa-results/` gespeichert und können durch Actions hochgeladen werden.

Privater und isolierter öffentlicher Stand: vollständige Suite mit **6.085 Spielprüfungen, 96 Audiolaufprüfungen, frischem Import/60-Frame-Start und 61 Python-Tests bestanden**. Nach der abschließenden Verallgemeinerung der Cacheprüfung und Provenienzformat-Anpassung wurden die betroffenen Encoder-/Buildtests nochmals ausgeführt. Änderungen an Versionsfixtures sind ausdrücklich für 0.7.3 / 10; keine Prüfung wurde entfernt oder abgeschwächt. Rohprotokolle unter [Archivindex: v073-*.log](qa/ARCHIVE_INDEX.tsv).

## Öffentliche Quellschnappschüsse bauen

Der bisherige Builder fragte `git rev-parse HEAD` erst nach dem Export ab. Ohne Git-Repository konnte er dann scheitern. Ein Quellschnappschuss in einem ignorierten Unterordner konnte sogar fälschlich den sauberen Git-Status des Elternrepositorys übernehmen.

Die Provenienz unterscheidet nun ausdrücklich das eigene Git-Arbeitsverzeichnis von einem unversionierten Schnappschuss. Bei einem Schnappschuss sind `source_commit` und `source_dirty` null; es wird keine saubere Git-Version behauptet. Das tatsächlich materialisierte App-Verzeichnis bekommt weiterhin einen vollständigen Inhalts-Hash. Provenienzformat 2 erfasst außerdem beobachtete Git-Statusänderungen während des Builds. Der Android-Build benötigt für einen Schnappschuss keine Git-Historie. Separate Regressionen prüfen fehlende Historie, das übergeordnete Repository und saubere/geänderte eigene Quellen.

Die tatsächlichen Android-Build-Ergebnisse stehen im [aktuellen Testbericht](test-report.md). Alle vorläufigen Paketkennungen sind weiterhin konfigurierbar; Release-Signierung und Play-Freigaben bleiben offen.

## Offline anhören

```sh
python3 scripts/qa/listening_pack.py --output build/listening-v073.html
```

Die erzeugte einzelne HTML-Datei enthält 42 Proben aus den tatsächlich ausgelieferten Audiodateien, Modellkarten und erwartete Texte zum Aufklappen. Deutsch-Lernproben spielen in EN/RU die richtige lokalisierte/native Folge. Ein aktueller Browser mit Ogg-Unterstützung ist erforderlich. Die Datei benötigt keine Netzwerkverbindung, speichert keine Antworten und nimmt keinen Ton auf. JavaScript wurde syntaktisch geprüft; Browser- und Hörabnahme bleiben manuell. Musikbalance und Android-Lautsprecher bitte zusätzlich in der APK prüfen.
