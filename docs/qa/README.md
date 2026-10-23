# QA-Nachweise: Einstieg und Archiv

Der aktuelle Einstieg ist [QUALITY_ASSURANCE.md](../QUALITY_ASSURANCE.md). Dieser Ordner enthält nur diesen Wegweiser und den einmalig erstellten, redaktionell geprüften [Archivindex](ARCHIVE_INDEX.tsv). Neue Testläufe schreiben nach `qa-results/` beziehungsweise `build/`, nicht hierher.

## Vollständig erhaltene Historie

Vor KW-QA-01: **139 Dateien, 7.383.943 Bytes** (7,04 MiB reine Dateiinhalte; `du` meldete rund 7,4 MiB inklusive Dateisystembelegung). Es waren maschinelle Logs, Android-/ASR-/Größenberichte und Provenienzen, keine handgepflegten Anleitungen.

Die Originalbytes liegen unverändert im selben **privaten** Repository unter dem festen Tag [`qa-evidence/2026-10-23-v091`](https://github.com/sayac007/Kinderwelt/tree/qa-evidence/2026-10-23-v091/docs/qa), Commit [`a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`](https://github.com/sayac007/Kinderwelt/tree/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa). Tag und Zielcommit wurden über die GitHub-API geprüft; alle 139 Git-Blob-IDs vor der Entfernung gegen die Originaldateien abgeglichen. SHA-256, Größe, erste Versionierung, letzte Änderung, Zweck und damalige Einzelreferenzen stehen pro Datei im Index. Die Datumsfelder sind Git-Zeitpunkte; ein nicht aufgezeichneter genauer Laufzeitpunkt wird nicht erfunden.

Der Archivtag ist eine dauerhafte Git-Referenz, kein temporärer Downloadlink. Nicht löschen oder neu setzen. Eine frühere Datei lässt sich ohne Checkout zurückholen:

```sh
git fetch origin refs/tags/qa-evidence/2026-10-23-v091:refs/tags/qa-evidence/2026-10-23-v091
git show qa-evidence/2026-10-23-v091:docs/qa/phase2.log > /tmp/kinderwelt-phase2.log
```

Keine neue öffentliche Veröffentlichung: Der Zugangskreis des privaten Repositorys bleibt erhalten. Historische Logs können lokale Pfade und Variantenbezeichnungen enthalten; sie gehören nicht ungeprüft in öffentliche Anhänge. Keine Fotos, Familiengrafiken oder Schlüssel werden diesem Archiv neu hinzugefügt. Eine Bereinigung älterer Git-Historie ist nicht Teil dieser Aufgabe.

## Warum keine Release-Anhänge oder alleinigen CI-Artefakte?

- CI-Artefakte eignen sich für neue Laufzeitberichte, laufen hier aber nach sieben Tagen ab. Sie sind kein Langzeitarchiv.
- Release-Anhänge können langfristig geeignet sein, wären hier eine zusätzliche Kopie mit zusätzlichem Zugriffs-/Uploadnachweis. Historische Zugriffsprobleme und Familien-Metadaten sprechen gegen eine ungeprüfte Veröffentlichung. Es wurde kein neuer Release erzeugt.
- Die bereits auf GitHub vorhandenen, verifizierten Git-Objekte bieten ohne Umkopieren eine versionsfeste Ersatzablage. Kein Befund wurde vernichtet. Die noch notwendige ASR-Untermenge von 24 Fachansagen liegt zusätzlich als begründete Regressionstest-Referenz unter `tests/fixtures/voice/subject-recognition.json`; sie ist kein neuer Laufbericht.
