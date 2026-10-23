# Kinderwelt: Qualität und Prüfstand

**Zielgruppe:** Klasse 1–2, aktuelle Aufgaben für die zweite Klasse. Ein lokales Godot-Lernabenteuer mit 320 Grundaufgaben und 640 freiwilligen Boni. Kein Wirksamkeitsnachweis und keine Google-Play-Freigabe.

## Orientierung

| Bereich | Inhalt / zuständige Dateien |
|---|---|
| Lernen | Je 40 Stationen in Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch, Geografie; Sprache jeweils DE/EN/RU. Zahlen-/Wort-/Regelrätsel, Sachfragen mit indirekten Bildhinweisen. |
| App | `core/quest/main.tscn` und `core/quest/`: Oberfläche, Weltbewegung, Aufgaben, Audio, lokaler Spielstand; keine externe Spielserver-Abhängigkeit. |
| Redaktion | `scripts/content/generate.py` kompiliert versionierte TSV-/JSON-Quellen und `advanced.py`/`experience.py`/`pedagogy.py` nach `games/quest/`. [Quellen und Ablauf](CONTENT_AUTHORING.md). |
| Medien | Lokale Vorbisclips: DE/RU Serena, EN LJSpeech. [Sprachverfahren und Hörgrenzen](voice.md). [Musik](music.md), [Bildherkunft](character-origins.md). |
| Varianten / Android | Getrennte neutrale und private Figurenquellen; [Build und technische Paketprüfung](android.md). Keine privaten Familien-Assets für neutrale Tests nötig. |

## Ausführen

Dieselben Befehle wie im [README](../README.md):

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Für wiederholte Bildprüfungen ein neues Ausgabeverzeichnis wählen.

Die bestehende CI ruft die vollständige Suite und die grafische Suite auf. Laufzeitdaten landen in `qa-results/`; Android-Ausgaben in `build/`. Auf den anschließenden Wunsch nach einer heute spielbaren Version wird zusätzlich die unveränderte Android-Pipeline für Testpakete ausgeführt. Release-Signierung und Google-Play-Freigaben bleiben ausgeschlossen.

## Aktuell verifiziert

**23.10.2026, Anwendungsstand `2f179ce6615e0bb7130e1bad4815fd1bf882ddff`.** Vollständige neutrale Suite, grafische Suite und zusätzlicher Familienstart bestanden. Der lokale Android-Build bestätigt diesen sauberen Commit (`source_dirty: false`, keine Änderung während des Builds). Der spätere Dokumentationscommit ändert die Anwendung nicht. GitHub prüft den Draft-PR zusätzlich; der jeweilige Laufstatus steht im PR, nicht als vorweggenommenes Ergebnis hier.

| Dimension | Tatsächlich verifiziert / Grenze |
|---|---|
| Automatisierte Regressionen | **106 Python-Tests**, darunter 16 neue pädagogische Tests; 9.896 Aufgaben-, 3.608 Welten- und 991 Punkteprüfungen bestanden. Neustart stellt 3.360 Testpunkte wieder her, ohne doppelte Belohnung. Generator reproduziert die Quellen ohne Diff; 320 Grundaufgaben und 640 Boni mit stabilen IDs. |
| Audio | **3.170 tatsächliche Ogg-Dateien decodiert**, alle 5.841 Text-/ID-Zuordnungen und Dateihashes geprüft; 36 Wiedergabe-, 75 Sequenz- und 38 Weltsprachprüfungen bestanden. DE/RU: offizielle weibliche Serena-Stimme, EN: weibliche LJSpeech; TTS-Integration unverändert. Neun neue Dateien unabhängig mit Whisper erkannt; Schreibweisen von Zahlen und einzelne Erkennungsabweichungen bleiben sichtbar. Keine muttersprachliche Hörfreigabe oder erfundene Wortzeitstempel. |
| Darstellung | **11.520 Messungen mit der tatsächlich verwendeten fetten Schrift**, kein Abschneiden. Alle 2.880 lokalisierten Grund-/Bonusansichten bei großer Schrift und 320×568 auf Text-/Bild-/Antwortüberschneidung geprüft. **605 echte Renderbilder** in vier Displayprofilen, drei Sprachen, einschließlich 144 neuer Sach-/Logikbonusansichten. Einzelne Bilder manuell angesehen, darunter Russisch mit großer Schrift; kein vollständiger manueller Bild-/Gerätetest. |
| Android | Familien-APK **287.237.798 Bytes**, AAB **274.078.762 Bytes**, 0.9.1 / Code 14, vorläufig `org.example.kinderwelt.preview.family.v090`. Paketstruktur, alle 6.529 erwarteten Ressourcen je Paket, API 24–36, zwei ABIs, ELF-/ZIP-Ausrichtung, Konfiguration und Signaturstatus bestanden. APK mit bestehendem Entwicklungsschlüssel; **AAB unsigniert**, keine Release-/Play-Freigabe. Lokal nur Familie gebaut; beide Varianten werden im unveränderten vertrauenswürdigen GitHub-Push-Workflow gebaut. |
| Datenschutz / Herkunft | Bestehender begrenzter Quell-/Konfigurationsaudit bestanden: keine Netzwerk-/Konten-/Werbeintegration, keine Android-Berechtigungen, Backup deaktiviert. Bild-/Modellherkunft und Musikhinweise geprüft. Keine Familiengrafiken geändert oder personenbezogenen Testdaten neu erhoben; keine umfassende Sicherheits-/Rechtszertifizierung. |
| Redaktion / Grenzen | Typisierte Hinweis-, Regel-, Antwort-, Referenz- und Duplikatprüfungen über alle Aufgaben/Sprachen bestanden. Zwei bekannte Helm-Bildlücken bleiben offen. Fachliche Matrix und Schwierigkeitsindikatoren sind überprüfbare Unterrichtsmodelle, kein unabhängiges Fachgutachten oder empirischer Lernwirkungsnachweis. |

Lokale reproduzierbare Ausgaben: `qa-results/kwqa-full-suite.log`, `qa-results/visual-kwqa-final/`, `build/android-kwqa-01/delivery.json` sowie `family/provenance.json` und `family/verification.json`. Keine Laufberichte neu ins Git aufgenommen. Die tatsächlichen Paketdateien liegen unter `build/android-kwqa-01/kinderwelt-debug-family.apk` und `build/android-kwqa-01/kinderwelt-unsigned-family.aab`. APK-SHA-256: `e7411cb3ee29f02de0e1c70a921351264359509d4599928af2cf93bdb42450ff`; AAB: `e5232ba8120d3bdfeda2cab4a0aa4de2d113b59c264e095d1e8540305a703eff`. GitHub baut separat; dessen Paketnachweise und Downloads stehen im jeweiligen Actions-Artefakt.

Der [frühere Ausgangsbericht](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/test-report.md) bleibt als historischer Vergleich erhalten; er beschreibt nicht den aktuellen Prüfstand.

## KW-QA-01: Dokumentation konsolidiert

139 Dateien / **7.383.943 Bytes** wurden im verifizierten Git-Archiv erhalten; `docs/qa/` enthält jetzt zwei notwendige Referenzdateien / **78.669 Bytes**. Keine Historie gelöscht. Alle 139 Remote-Blobs samt Archivtag geprüft, lokale Dokumentations- und CI-Dateiverweise gültig; zwei neue Linkregressionen und der umgezogene ASR-Fixture-Test bestanden. GitHub-Einstellungs-/Actionsseiten erfordern Anmeldung; keine allgemeine öffentliche HTTP-Erreichbarkeit behauptet. [Inventar und Ablageentscheidung](qa/README.md).

## KW-QA-01: Inhaltskorrekturen

**880 einzelne Datensätze geändert: 240 Grundaufgaben und alle 640 Boni.** Dabei wurden 608 Fragetexte und 880 Hinweise überarbeitet (jeweils Datensätze, nicht dreifach gezählte Übersetzungen). Weiterhin 320 Grundaufgaben, acht Fächer, 960 eindeutige IDs und 10/50/100 Punkte; Spielstandrevision und Belohnungslogik unverändert.

| Ursprünglicher Befund | Korrektur und Absicherung |
|---|---|
| Verratende Hinweise | 600 Sachhinweise mit direkter Lösung entfernt; alle 120 Wortaufgaben erhalten Laut-/Lesestrategien statt Buchstabenlisten. Mathehinweise unterstützen Rechenwege ohne Endantwort. Regressionen prüfen alle drei Sprachen und bewusst eingebaute Fehler. |
| Logikboni | Alle 40 50-Punkte-Boni: zwei tatsächlich verschiedene Schritte, zweimal fortsetzen und die neuen Zahlen addieren. Alle 40 100-Punkte-Boni: aus Beispielen Regel ableiten und rückwärts anwenden. Die fünf gemeldeten +1/+1-Fälle werden einzeln als Negativfälle getestet; Grammatik bereinigt. |
| Ablenker | Alle ursprünglichen 33 auffälligen Grundaufgaben mit Begründung nachgeprüft; weitere Fragen/Optionen redigiert. Kleine, ausschließlich prüfende Kategorietabelle. Zwei offene Bildlücken bei `physics_09` und `body_16`: Es fehlen alternative Kopfschutzbilder. Die Kategorienheuristik wurde geändert; „33 → 2“ ist deshalb kein gemessener Qualitätszuwachs. |
| Wiederholungen | 400 neue Sachboni: drei/vier fachliche Aussagen prüfen und genau zwei/drei passende erkennen. Jede falsche Option erfüllt mindestens eine Aussage. Je Fach 80 unterschiedliche Merkmalssätze statt bisher 23–39 verschiedener deutscher Texte; Logik 80 statt zwei Textschablonen. Das Kompass-Paar `geography_01`/`geography_31` und stationsübergreifende Nicht-Mathe-Duplikate sind abgesichert. |
| Fachsprache | Zwölf ursprüngliche Blume/Blüte-Fälle überprüft: drei Grundaufgaben präzisiert, neun alte Boni ersetzt. Bestäubung und Hebel werden erklärt; Industriefertigung von Glas und Flüssigkeitsverlust durch Schwitzen konkretisiert; umständliche Kompassfrage vereinfacht; `SCHILDKRÖTENEI` durch `ENTENEI` ersetzt. Physik-/Biologiematrix berücksichtigt auch die Schraubendreherachse und Wasseraufnahme einer Eiche. |

**Begründete Ausnahmen:** Identische Wortfragen innerhalb derselben Station bleiben zulässig, weil andere Lücken zu lösen sind. Rechenschablonen mit verschiedenen Zahlen sind keine Inhaltsduplikate. Wiederholte Antwort-/Optionsmengen werden separat ausgewiesen und bedeuten bei anderen Fragen nicht automatisch einen Fehler. `biology_32` (lebendig/unbelebt) und `body_29` (Nahrung/Sicherheit) verwenden absichtlich unterschiedliche Kategorien. Ein sinnvolles mathematisches Zwischenresultat ist kein Lösungsverrat; kurze Wörter wie „Ei“ dürfen „Eine/Eigenschaft“ nicht fälschlich beanstanden. Diese Gegenbeispiele werden getestet.

**Schwierigkeitsdiagnostik:** Alle 640 Boni werden ausgewiesen. Mathe zeigt mehr Rechenoperationen als die Grundaufgabe, Sprache mehr Lücken, Logik einen zusätzlichen Verarbeitungsschritt. Sachboni umfassen neun/zwölf mögliche Merkmalszuordnungen plus exakte Anzahl; alle 400 bleiben als fachlich und empirisch zu prüfende Schwierigkeitsindikatoren markiert. Einige Merkmale hängen zusammen und erlauben Abkürzungen; neun/zwölf mögliche Zuordnungen sind keine garantierte Zahl unabhängiger Denkschritte. Auch Rechenoperationen können sich vereinfachen. Mehr Merkmale beweisen weder höheren Lerngewinn noch angemessene Schwierigkeit für jedes Kind.

**Zusätzlich gefundene Darstellungsfehler behoben:** Die Vorprüfung maß zunächst die normale statt der tatsächlich verwendeten fetten Schrift. Die korrigierte Messung fand 43 zu lange Überschriften bei großer Schrift. Hochformat erlaubt jetzt bis zu acht Zeilen; die Illustration gibt bei Bedarf Platz frei, Schrift und Antwortflächen bleiben groß. Eine weitere Prüfung deckte veraltete Texthöhen nach dem ersten Umbruch auf; die Ansicht ordnet sich bei geänderter Mindesthöhe neu an. Die anschließend vollständig wiederholten Prüfungen oben bestanden. Geänderte Fragen und Hinweise sind mit ihren bestehenden Engines tatsächlich neu vertont und vollständig eingebunden; keine alten Aufnahmen umetikettiert.

**Speicher beim Vertonen:** Das von der Plattform festgelegte 32-GiB-Limit ist hier nicht veränderbar. Ein paralleler DE-Lauf wurde durch Speichermangel beendet; Checkpoint-Wiederaufnahme und serielle Erzeugung haben alle drei Sprachbanken vollständig abgeschlossen. TTS-Modelle werden nicht mit der App ausgeliefert.

## Offene manuelle und empirische Freigaben

Zwei Helm-Bildlücken; muttersprachliches Hören der neuen Clips; unabhängiges Fachreview der Unterrichtsmodelle und Formulierungen; Beobachtung von Bedienung, Verständnis und Schwierigkeit mit Kindern; reale Android-Geräte-, Drehungs- und Update-/Spielstandprüfungen. Die Aussagen gelten für die in `science-models.json` genannten Beispiele, nicht unterschiedslos für jede Tierart oder jedes Material. Automatische Konsistenzprüfungen bestätigen keine fachliche Vollständigkeit der Ausgangsmatrix.

Für eine Kinderstudie sind Protokoll, Einwilligung und Datenschutzentscheidung vor jeder personenbezogenen Datenerhebung erforderlich; aktuell werden keine Kinderaufnahmen oder Telemetriedaten gesammelt. Es gibt keine empirisch belegte Lernwirkung oder Google-Play-Uploadfreigabe.

## Dokumentationsregeln

- Ein aktueller Überblick, Anleitungen und begründete langfristige Referenzen im Git; **keine neuen Einzelberichte je Testlauf**.
- Neue Logs/JSONs nach `qa-results/` oder `build/`; CI-Artefakte werden nach sieben Tagen gelöscht. Dauerhafte Freigaben brauchen eine verifizierte versionierte Ablage mit Commit, Datum, Namen und Hashes.
- Historische Dateien erst nach geprüfter Ersatzablage entfernen. [Archiv und vollständiger Index](qa/README.md): 139 Originaldateien unverändert erreichbar; keine Veröffentlichung privater Grafiken oder Zugangsdaten.
- README, CI und Anleitungen müssen dieselben Testkommandos verwenden. `documentation.py` kontrolliert lokale Markdown-Ziele, Archivindex und CI-Dateireferenzen; externe HTTP-Erreichbarkeit wird getrennt ausgewiesen.
