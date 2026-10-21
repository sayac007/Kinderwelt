# Umsetzungsphasen und tatsächliche Prüfungen

## Phase 1 – Varianten

Privater Standardbuild mit lokalem ignoriertem Grafikpack; öffentliche Fantasiefiguren mit allen fünf Looks; sechs neue neutrale Figuren plus gemeinsamem Eichhörnchen. Gleiche Speicherkennungen und Migration, kein Eingriff in die Mechanik oder Speicherbereinigung. Generische gesprochene Begrüßung in drei Sprachen. Public-Snapshots enthalten keine privaten Figurenressourcen oder Git-Historie. GitHub Actions wählt public.

Ausgeführt: vollständiges `tests/run.sh` für family und ein getrenntes public-Projekt ohne privaten Pack; jeweils **6.085 Spielprüfungen, 30 Audiobusprüfungen und damals 39 Python-Tests bestanden**. Nach Ergänzung des Quellschnappschuss-Tests nochmals alle **40 Python-Tests** und anschließend die vier Variantenprüfungen bestanden. **343 echte öffentliche Renderings bestanden**, Auswahl und maximale Header stichprobenartig angesehen.

Gefundener und behobener Fehler: Nach erneutem Varianten-Materialisieren fehlten Importdeskriptoren für den Renderer. Der Renderer importiert die vorbereiteten Quellen nun ausdrücklich neu und bricht bei Importfehlern ab.

Teständerungen: Figurenquellen werden anhand des gewählten Variantenmanifests und tatsächlicher Hashes geprüft; private Originalbytes bleiben abgesichert. Öffentliche Normaloutfits sind absichtlich AtlasTexture-Rahmen. Speicher-ID-/Kleider-/Lösungsregressionen kamen hinzu. Es wurden keine Tests entfernt oder akzeptierte falsche Antworten eingeführt.

Rohprotokolle: `docs/qa/phase1-family.log`, `phase1-public.log`, `phase1-python.log`, `phase1-variants.log`, `phase1-public-render.log`. Echte Geräte-/Hörabnahme und Kinderbeobachtung offen. Private Grafiken in früherer Git-Historie wurden nicht rückwirkend entfernt; siehe `variants.md`.
