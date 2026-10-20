# Wiederverwendbare Qualitätssicherung · Aufgabe 04

Dieses System prüft Softwareeigenschaften. Ein grüner Lauf genehmigt weder eine
Studie mit Kindern noch eine Veröffentlichung und weist keine Lernwirkung nach.
Android-Export und Aufgabe 05 sind ausdrücklich nicht Teil dieser Arbeit.

## Verbindliche Gates und Evidenzklassen

Grundlage ist die vollständig gelesene `04_quality_research.yaml`. Die Zustände
sind **PASS**, **FAIL**, **NOT RUN**, **NOT MEASURED** beziehungsweise bei Wirkung
**NOT ESTABLISHED**. Ein nicht ausgeführter Test wird nie als bestanden gewertet.

| Gate | Automatisch prüfbar | Verbleibende Prüfung |
| --- | --- | --- |
| Q01 Import/Start | Gepinnte Engine, frischer Importcache und Anwendungsstart | Physische Plattformen |
| Q02 Bestand | Alle vier vorhandenen Suiten mit nichtleerer Ergebniszahl | Keine Ersetzung durch Syntax-/Nulltests |
| Q03 Inhalte | Jede registrierte Aufgabe: Schema, Lösungsweg über Controls, gespeicherter Abschluss | Verständlichkeit der konkreten Bilder/Regeln mit Kindern |
| Q04 Lebenszyklus | Drei Retries, Undo nach Abschluss, Mute, Save/Reload, Schreibfehler, Back, abgebrochene Beispiele | Echtes Betriebssystem-/Geräteverhalten |
| Q05 Bedienfläche | 320×568, 360×800, 768×1024, 1024×768; Mindestziele 96×72 logische Pixel, horizontale Grenzen, Scroll-Erreichbarkeit | DPI, Kontrast aller Zustände, reale Hände/Assistenztechnik |
| Q06 Tastatur | Fokus bleibt beim Einstieg und nach Aktionen/Undo im Spiel | Vollständige Reihenfolge, sichtbarer Fokus, Screenreader auf Zielsystemen |
| Q07 Statische Risiken | Muster für Netzwerk, Tracking, Prozessstarts, Berechtigungen, native SDKs und mögliche Schlüssel | Keine Sicherheitszertifizierung; Paket-/Store-Prüfung später |
| Q08 Reproduzierbarkeit | GUT/Engine/Actions gepinnt, isolierte Daten, Ergebnisintegrität, Logs/JUnit/Inventar | Tatsächliches GitHub-CI-Ergebnis gesondert bestätigen |
| Q09 Gerätebenchmark | Keine Messung auf virtueller Cloud-Hardware als Gerätewert ausgeben | Start, Frametimes, Speicher auf benannten realen Geräten |
| Q10 Evaluation | Protokoll/Beobachtungsvorlage/Hypothesen vorbereitet, keine Sammlung eingebaut | Schutz-/Einwilligungsentscheidung, Usability- und kontrollierte Wirkungsstudien |

Eine Aufgabe erfüllt Q03–Q06 nur bezüglich der konkret ausgeführten synthetischen
Abläufe. Bedienbarkeit ohne Lesen und altersgerechte Interpretation sind
Gestaltungshypothesen, keine aus Lösbarkeit abgeleiteten Befunde.

## Ausführen

Voraussetzungen: Linux x86_64, Bash, Python 3.10+, Git, curl, unzip, awk,
sha512sum, rg, timeout; die im Repository gepinnte Godot-Version 4.7.2.

```bash
bash scripts/install-godot.sh
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/run.sh
```

Optional `--output /absoluter/neuer/pfad`; vorhandene Verzeichnisse werden
abgelehnt, damit alte Ergebnisse nicht für einen neuen Lauf gehalten werden.
`bash tests/run.sh` bleibt als bisheriger Einstieg unverändert nutzbar.
Der QA-Einstieg ruft ihn vollständig auf und ergänzt die neuen Gates.

GUT **9.7.1**, Commit **aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605**, ist laut
[offizieller Versionsmatrix](https://github.com/bitwes/Gut/tree/v9.7.1) für Godot
4.7.x geeignet. `scripts/install-gut.sh` beschafft exakt diesen Commit über das
bestehende HTTPS-Git-Verfahren und prüft HEAD sowie Änderungen an verfolgten
Dateien. Es ersetzt keine fremde Installation. Der MIT-lizenzierte Quellstand
bleibt im ignorierten Entwicklungscache `.godot/qa-tools/gut`; `addons/gut` ist
ein ignorierter Symlink. Der Editor-Plugin wird nicht aktiviert. Die Tests unter
`tests/qa` sind über `.gdignore` vom normalen Spielimport getrennt und werden
explizit durch GUT geladen. Es wird kein Framework aus einem beweglichen Branch
oder durch Abschalten der TLS-/Checksum-Prüfung installiert.

Aus dem unveränderten GUT-Stand laufen zusätzlich dessen bestehende Suiten
`test/unit/test_version_numbers.gd` und `test/unit/test_parameter_factory.gd`.
Das ist eine benannte Kompatibilitätsstichprobe, nicht die gesamte Upstream-Suite.
Die eigene Suite verwendet die normalen GUT-Assertions und den GUT-JUnit-Export.
Nulltests, Pending/Skipped, widersprüchliche Zählungen, Tests ohne Assertions
oder Fehler im Godot-Log machen den QA-Lauf rot, auch bei Prozess-Exit 0.

Die Abhängigkeit ist **nur ein Entwicklungswerkzeug**. Sie ist kein Tracking-SDK
im Spiel. Vor einem späteren Release muss die Trennung von Entwicklungsdateien
im ausgelieferten Paket eigens geprüft werden; hier werden keine Exportpresets
angelegt und keine Aussage über ein fertiges Android-Paket getroffen.

## Inventar und Erweiterung

`tests/qa/policy.json` ist die überprüfbare Projektkonfiguration: Mindestanzahl je
Bereich, Viewports, große Zielbereiche, Wiederholungen und Framework-Pin.
`content/modules.json` und die geladenen `levels.json` bestimmen das tatsächliche
Inventar. Aktuell sind es 9 + 9 + 6 + 6 + 6 = **36** Aufgaben. Neue Aufgaben werden
automatisch in die Matrix aufgenommen; fehlende/duplizierte IDs, ungültige
Sammlungen und nicht unterstützte Spielverträge scheitern sichtbar.

Für einen neuen Spieltyp:

1. Registrierung und Schema-/Lösbarkeitsvalidator ergänzen, eindeutige IDs und
   lokale Datenschnittstelle erhalten.
2. Den Kontrolladapter in `tests/qa/test_quality.gd::solve` ergänzen, falls der
   Typ nicht den bestehenden Array-/Dictionary-Hinweisvertrag nutzt. Keine
   unbekannten Aktionen überspringen; das begrenzte Schrittbudget muss scheitern.
3. `model.complete`, reversible Aktionen, persistierten Abschluss, freie
   Navigation, Mute und zugängliche Controls nachweisen.
4. Menschliche Prüfung ergänzen: Bildverständnis, alternative Deutungen,
   Eingaben/Assistenztechnik. Ein automatischer Pfad ersetzt sie nicht.

Die 36 Aufgaben werden an vier Viewports geprüft: **144 Matrixfälle**. Jeder
Fall prüft auch Wiederholung, Controls, Scrollen, vollständigen Abschluss,
Save/Load, Undo und Rückkehr. Framework-Testmethoden, Assertions, Matrixfälle
und menschliche Beobachtungen sind unterschiedliche Einheiten; sie werden
nicht zu einer irreführenden „Anzahl getesteter Kinder“ zusammengerechnet.

## Optionale synthetische Sichtprüfung

Mit einem vorhandenen Grafikdisplay kann zusätzlich
`GODOT=... bash tests/qa/render.sh /absoluter/neuer/ausgabepfad` ausgeführt werden.
Ohne Display lautet das Ergebnis NOT RUN (Exit 2), keine fingierte Sichtprüfung.
Die Anwendung rendert alle registrierten Aufgaben an 320×568 und 768×1024,
einschließlich Scrollseiten. `render.json` ordnet PNGs Aufgaben, Viewports und
realen Scrollpositionen zu; die Bildabmessungen werden geprüft. Es werden
keine Kamera-/Kinderbilder aufgenommen. Mute ist aktiv; ein Dummy-Audiotreiber
verhindert eine unbeabsichtigte Hörmessung. Fokusfolgen sind für kontrollierte
Reviewseiten ausschließlich im Capture-Prozess deaktiviert, nicht im Spiel.
Die Bilder müssen separat angesehen werden; ein erfolgreicher Capture ist
weder menschliche Sichtprüfung noch Geräte-/Kindertest.

## Ergebnisdateien und CI

Jeder Lauf erzeugt `qa-results/<UTC-Laufkennung>/` mit `report.json`, `static.json`,
`coverage.json`, getrennten Logs und `upstream.xml`/`quality.xml` (JUnit).
Der Bericht enthält Quellcommit, Dirty-Status, SHA-256 der relevanten Quellen,
Werkzeug-Pins, Befehle und Prozessstatus. Quelländerungen während eines Laufs
machen dessen Evidenz ungültig. Die Ausgangsrevision allein ist bei einem Dirty-
Lauf kein Nachweis für einen identischen Commit; dafür dient zusätzlich der Digest.
Die Berichte erfassen ausschließlich synthetische technische Prüfungen.

Spielstände liegen in einem neu erzeugten temporären XDG-Verzeichnis. Ein
zweites frisches Projekt mit leerem Importcache und denselben Anwendungsquellen
prüft frischen Import/Start. Persönliche Saves werden weder gelöscht noch
zurückgesetzt. Die GUT-Suite verweigert außerhalb der isolierten QA-Umgebung
ihre Ausführung. Ergebnisverzeichnisse werden nicht wiederverwendet.

Die vorhandene GitHub-Workflowdatei ruft den QA-Einstieg auf Ubuntu 24.04 auf.
Checkout v4.2.2 und Upload v4.6.2 sind auf vollständige Commits gepinnt;
Repository-Berechtigung bleibt `contents: read`. Auch bei Fehlern werden nur
technische `qa-results/` für sieben Tage aufgehoben. Keine Beobachtungsbögen,
Kinderangaben, Aufnahmen oder Studienrohdaten gehören in CI-Artefakte/GitHub.
Ein lokaler Erfolg ist kein Beleg für einen tatsächlich gelaufenen Remote-Job.

## Statische Prüfung: bewusst begrenzter Geltungsbereich

`scripts/qa/static_audit.py` untersucht verfolgte sowie nicht ignorierte eigene
Quellen. Laufzeitdateien werden auf bekannte Netzwerk-/Tracking-APIs, externe
URLs, Prozessstarts, aktivierte Berechtigungen und prüfbedürftige native Dateien
untersucht. Textdateien werden auf definierte credentialartige Muster geprüft.
Ein Fund meldet **nur Pfad, Zeile und Regel**, nie einen gefundenen Schlüsselwert.
Negative Fixtures prüfen unter anderem Netzwerk, SDK, Berechtigung und die
Nichtausgabe synthetischer Schlüssel. Diese Musterprüfung beweist weder die
Abwesenheit jeder möglichen Datenübertragung noch die Sicherheit aller Dateien.

GUT-Cache, QA-Artefakte und Werkzeugcode sind keine Anwendungs-Laufzeitquellen.
Neue Binärabhängigkeiten sind prüfpflichtig. Eine Ausnahme benötigt in der Policy
einen exakten Pfad, eine bekannte Regel und eine Begründung; keine Wildcard-
Freigabe. Werden Treffer nicht aufgelöst, starten die Laufzeittests nicht.
Ohne Manifest/Exportpreset lautet der Befund „kein solches Quellartefakt“, nicht
„Android-Berechtigungen geprüft“. Aufgabe 05 bleibt offen.

## Schweregrad und menschliche Freigabe

- **Kritisch:** reproduzierbarer Crash, irreversibler Saveverlust, nicht verlassbare
  Spielsituation oder unzulässige Datenübertragung. Blockiert jede Nutzung mit
  Kindern bis zur Behebung und Regression.
- **Erheblich:** nicht erreichbares Ziel, fehlende Eingabemöglichkeit oder
  missverständliche zentrale Anleitung. Beheben oder Nutzungskontext ausdrücklich
  begrenzen und erneut prüfen; kein stilles PASS.
- **Gering:** nicht blockierende Darstellungs-/Textprobleme. Mit Pfad, Zustand,
  Gerät/Viewport, Reproduktion und erwarteter Wirkung protokollieren.
- **Unbekannt/NOT RUN:** fehlende empirische oder manuelle Evidenz. Kein kleiner
  Fehler und kein bestandenes Gate; vor einem betreffenden Einsatz nachholen.

Vor beaufsichtigten Kindertests gelten zusätzlich die
[Usability- und Schutzprotokolle](child-usability-checklist.md). Aktuelle Befunde
stehen in [test-report.md](test-report.md); pädagogische Hypothesen und
Transfergrenzen in [learning-hypotheses.md](learning-hypotheses.md).
