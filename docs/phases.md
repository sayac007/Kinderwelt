# Umsetzungsphasen und tatsächliche Prüfungen

## Phase 1 – Varianten

Privater Standardbuild mit lokalem ignoriertem Grafikpack; öffentliche Fantasiefiguren mit allen fünf Looks; sechs neue neutrale Figuren plus gemeinsamem Eichhörnchen. Gleiche Speicherkennungen und Migration, kein Eingriff in die Mechanik oder Speicherbereinigung. Generische gesprochene Begrüßung in drei Sprachen. Public-Snapshots enthalten keine privaten Figurenressourcen oder Git-Historie. GitHub Actions wählt public.

Ausgeführt: vollständiges `tests/run.sh` für family und ein getrenntes public-Projekt ohne privaten Pack; jeweils **6.085 Spielprüfungen, 30 Audiobusprüfungen und damals 39 Python-Tests bestanden**. Nach Ergänzung des Quellschnappschuss-Tests nochmals alle **40 Python-Tests** und anschließend die vier Variantenprüfungen bestanden. **343 echte öffentliche Renderings bestanden**, Auswahl und maximale Header stichprobenartig angesehen.

Gefundener und behobener Fehler: Nach erneutem Varianten-Materialisieren fehlten Importdeskriptoren für den Renderer. Der Renderer importiert die vorbereiteten Quellen nun ausdrücklich neu und bricht bei Importfehlern ab.

Teständerungen: Figurenquellen werden anhand des gewählten Variantenmanifests und tatsächlicher Hashes geprüft; private Originalbytes bleiben abgesichert. Öffentliche Normaloutfits sind absichtlich AtlasTexture-Rahmen. Speicher-ID-/Kleider-/Lösungsregressionen kamen hinzu. Es wurden keine Tests entfernt oder akzeptierte falsche Antworten eingeführt.

Rohprotokolle: `docs/qa/phase1-family.log`, `phase1-public.log`, `phase1-python.log`, `phase1-variants.log`, `phase1-public-render.log`. Echte Geräte-/Hörabnahme und Kinderbeobachtung offen. Private Grafiken in früherer Git-Historie wurden nicht rückwirkend entfernt; siehe `variants.md`.

## Phase 2 – Antwortalternativen

93 Aufgaben über TSV-Quellen und Generator überarbeitet. Alle 200 bestehenden Sachantworten und Fachzuordnungen bleiben durch eine unabhängige Referenzdatei abgesichert. `biology_32` hatte eine lebendige Pflanze als falsche Lebewesen-Antwort; jetzt stehen Maus, Papier und Glas zur Wahl. Präzisierungen in allen drei Sprachen vermeiden mehrere richtige Antworten. Kein neues Bild, keine Umsortierung, keine neue Spielmechanik.

Die dokumentierte Kategorienheuristik markierte am Ausgangsstand 83, jetzt 33 Aufgaben. Dies ist keine fachliche Zertifizierung. Unveränderte Aufgaben mit Bildbedarf, mögliche Fachzuordnungen und alle Änderungen stehen in `distractor-review.md`.

Ausgeführt: `tests/run.sh` einschließlich **6.085 Spielprüfungen, 30 Audiobusprüfungen, frischem Import/Start, allen 45 Python-Tests**, Quellaudit und reproduzierbarem Ablenkerbericht: **bestanden**. Rohprotokoll: `docs/qa/phase2.log`. Alle geänderten Sprachaufnahmen wurden mit den bisherigen lizenzierten Modellen erzeugt und tatsächlich decodiert. Fünf neue Tests sichern Antworten, Fachzuordnung, lebendige Pflanze, bewusst unveränderte Aufgaben und Bericht-Reproduktion. Keine bestehende Prüfung entfernt. Fachliche, muttersprachliche und kindliche Abnahme bleiben offen.

## Phase 3 – Sprachfassungen

Alle 320 Fragen/Hinweise in drei Sprachen abgeglichen. 199 Textfelder in 60 Aufgaben präzisiert; jedes geänderte Feld ist mit Vorher/Nachher in `localization-review.md` und maschinenlesbar protokolliert. Fehlende Gegenstände, Zahlen, Lernwörter, Buchstaben und Klatsch-Silben ergänzt. Deutsche Zielwörter werden weiterhin ausschließlich durch die deutsche Folgeaufnahme vermittelt; die EN/RU-Voraufnahme erklärt die Aktion. Kein Eingriff in Antworten, Bilder, Fachzuordnung oder Mechanik; ursprüngliche deutsche 24 Aufgaben bleiben erhalten.

Ausgeführt: `tests/run.sh`, **6.085 Spielprüfungen, 30 tatsächliche Audiobusprüfungen, frischer Import/Start, alle 49 Python-Tests**, Inhalts-/Ablenker-/Lokalisierungsberichte: **bestanden**. Vier neue Regressionen prüfen konkrete Informationsverluste und Sprachrouting; bestehende Prüfungen bleiben unverändert. Rohprotokoll: `docs/qa/phase3.log`. Fachbegriffe und kindliche Verständlichkeit sind als offene muttersprachliche Prüfungen aufgeführt.

## Phase 4 – Deutsche Stimme

Vorhandenen tatsächlichen Stand geprüft: Thorsten high statt des veralteten Kerstin-low-Verweises. Lokal vorliegende Thorsten-medium/high-Karten, Modellkonfigurationen und ONNX-Hashes geprüft; beide Datensätze CC0/22.050 Hz. Empfehlung: high beibehalten. Die widersprüchliche Qualitätszeile der originalen High-Karte ist dokumentiert, nicht verändert. Kein Modellwechsel; Lizenzdateien bleiben unverändert.

Ausgeführt: unabhängiges ASR-Screening 31 Dateien je Sprache, ohne Referenzvorgabe; Zeichenabweichungen DE 4,189 %, EN 3,617 %, RU 7,464 %. Vollständige Rohbefunde in `docs/qa/phase4-asr.json`; tatsächliche lokale Modellprüfung in `phase4-models.json`. Kein Nachweis vollständiger Hörverständlichkeit. Hörprotokoll und auffällige Fälle in `voice.md`.

`tests/run.sh` einschließlich **6.085 Spielprüfungen, 30 Audiobusprüfungen, frischem Start/Import und allen 51 Python-Tests**: **bestanden**. Zwei neue Provenienz-/Qualitätsregressionen; keine vorhandene Prüfung entfernt. Alle 1.633 unterschiedlichen Sprachdateien vollständig decodiert. Rohprotokoll: `docs/qa/phase4.log`. Muttersprachliche und kindliche Hörabnahme sowie Audio auf echten Geräten bleiben offen.
