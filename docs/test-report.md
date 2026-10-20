# Qualitätsbericht · Aufgabe 04

Der nachfolgende Bericht hält den Stand von Aufgabe 04 fest. Aktuelle Android-
Builds und erneut ausgeführte Qualitätstests aus Aufgabe 05 stehen im
[Release-Bericht](release-report.md).

Stand: 20.10.2026. Grundlage `04_quality_research.yaml`, vollständig gelesen und
mit dem Upload bytegleich. Branch `feat/quality-research` basiert auf `origin/main`
`6c10c24`, einschließlich Merge von PR #3. Aufgabe 05, alle YAML-Dateien und die
36 Inhaltsdefinitionen bleiben unverändert. Historische Berichte:
[Fundament](foundation-test-report.md), [Logik/Mathematik](logic-math-test-report.md),
[Sprache/Selbstständigkeit/Dorf](scenario-test-report.md).

## Ergebnis und Reichweite

Die technische Baseline und der erweiterte QA-Lauf bestehen lokal. Innerhalb der
geprüften Pfade sind keine kritischen Crashes oder nicht verlassbaren Aufgaben
bekannt. Das ist kein Beweis für alle Eingaben/Geräte und **keine Marktreife- oder
Studienfreigabe**. Physische Zugänglichkeit, Verständlichkeit für Kinder und
pädagogische Wirkung bleiben offen. Es wurden keine Kinder untersucht.

| Ausgeführt | Status | Tatsächliches Ergebnis |
| --- | --- | --- |
| Baseline vor Änderungen | PASS | bisherige vier Suiten, 1.236 Checks |
| Bisherige vollständige Suite nach Änderungen | PASS | 33 Fundament + 559 Lernspiel + 59 Eingabe + 585 Szenarien = 1.236 Checks, 0 Fehler |
| Exakte Godot-Version | PASS | 4.7.2.stable.official.ed1daf0bf, Linux x86_64 |
| Frisches Projekt ohne Importcache und eigene synthetische Daten | PASS | Import und `--quit-after 60`, Exit 0 |
| GUT-Kompatibilität | PASS | 9.7.1, Commit aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605, offiziell Godot 4.7.x |
| Bestehende Upstream-GUT-Tests | PASS | 13 Testmethoden / 62 Assertions; Versions- und Parameter-Factory-Suiten |
| Eigene GUT-Qualitätsprüfungen | PASS | 6 Testmethoden, 13.433 in JUnit erfasste Assertions, 0 failed/skipped |
| Aufgaben-/Viewport-Matrix | PASS | 36 Aufgaben × 4 Profile = 144 tatsächlich dokumentierte Fälle |
| Checker-/Ergebnisintegrität | PASS | 16 Python-Unittests, inklusive negativer Fixtures und Null-/Pending-/Fehler-Ergebnissen |
| Statische Quellprüfung | PASS (begrenzt) | 0 offene Musterfunde; keine Ausnahmen |
| Renderlauf | PASS | alle 36 Aufgaben an 320×568 und 768×1024, 112 erfasste Scrollseiten, Bildabmessungen geprüft |
| Sichtprüfung | TEILWEISE | synthetische Übersichten aller Telefon-Aufgaben sowie Einzelansichten; kein vollständiger Zustands-/Kontrast-/Gerätetest |
| `git diff --check` | PASS | keine Whitespacefehler |
| Sauberer Checkout mit neuer Installation | PASS | Codecommit `86d8b45`, alle Gates erneut bestanden; SHA-512 und GUT-Pin geprüft |
| GitHub-CI für diesen Branch | NOT RUN / NICHT BESTÄTIGT | Workflow vorhanden; lokaler Erfolg ist kein Remote-Nachweis |
| Physische Geräte / Screenreader / Hörtest | NOT RUN | manuelle Checkliste vorbereitet |
| Geräte-Kaltstart, Frametimes, Speicher | NOT MEASURED | kein physisches Zielgerät verfügbar, keine Cloudwerte umgedeutet |
| Kinder-Usability | NOT RUN | Protokoll und freiwillige leere Vorlage, keine Datensammlung aktiviert |
| Empirische Lernwirkung / Transfer | NOT ESTABLISHED | Hypothesen und kontrollierter Evaluationsplan, keine Wirkungsdaten |

Framework-Methoden, Assertions und Matrixfälle sind unterschiedliche Einheiten;
sie werden nicht als Zahl beobachteter Kinder oder normierter Entwicklungswerte
zusammengezählt. In frühen Entwicklungslogs enthielt GUT eine zusätzliche
Assertion im `after_all`-Hook; im finalen Stand ist die Berichtserzeugung ein
separates Integritätsgate und keine nicht in JUnit zuordenbare Testassertion.

## Befehle und Nachweise

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/qa/run.sh
```

Der QA-Einstieg protokolliert alle konkreten Unterbefehle. Er ruft den bestehenden
Runner vollständig auf; installiert GUT auf immutablem Commit; importiert die
Frameworkklassen; startet `addons/gut/gut_cmdln.gd` mit `tests/qa/gut.json` und
expliziten Testpfaden; prüft die neu erzeugten JUnit-Dateien und `coverage.json`.
Die originale GUT-Versionstabelle und deren 13 tatsächlich ausgeführten
Testmethoden sind kein Nachweis für die gesamte Upstream-Suite.

Ergebnisverzeichnisse sind pro Lauf neu. `report.json` enthält Commit, Dirty-Status,
relevanten Quell-Digest, Versionen, Befehle und Prozessstatus; `static.json` und
`coverage.json` erklären die Grenzen. Synthetische Saves liegen nur in
`/tmp/kinderwelt-quality.*`; ein frischer Importcache liegt in einem separaten
temporären Projekt. Echte Spielstände werden nicht gelesen/zurückgesetzt.
Fehler, Timeouts, Parsefehler trotz Exit 0, Nulltests oder übersprungene Tests
verhindern ein PASS. Eingefrorene/alte Ergebnisdateien werden nicht übernommen.

Der abschließende Arbeitsbaum-Lauf liegt in dieser Sitzung unter
`/tmp/kinderwelt-quality-final-report`; die CLI gibt bei weiteren Läufen das neue
Verzeichnis aus. Ein zusätzlicher sauberer Checkout von Codecommit `86d8b45` wurde
unter `/tmp/kinderwelt-quality-repro.waDQId/repo` erstellt. Der vorhandene vorbereitete Cache wurde nicht
übernommen: Godot wurde neu installiert (offizielle SHA-512-Prüfung PASS),
GUT neu auf den gepinnten Commit geholt und derselbe QA-Einstieg ausgeführt.
Gesamtstatus PASS, Dirty-Status false, 144/144 Matrixfälle und alle oben genannten
Suiten erneut erfolgreich. Laufkennung `20261020T081907Z-75dc9879`; Originalartefakte unter
`/tmp/kinderwelt-quality-repro.waDQId/repo/qa-results/20261020T081907Z-75dc9879`. Der relevante Quelldigest ist
`ca8fa97891cc519a2a810f53cf00860981de2c8af53a7c426c9c3decd0aba0a5`.
Diese lokale Linux-Reproduktion ist kein bestätigter GitHub-Job und keine
Messung auf einem physischen Zielgerät. Eine nachfolgende Änderung ausschließlich
an Berichten/Protokolltexten verändert den getesteten Spiel-/QA-Code nicht.
Die [kompakte technische Evidenz](quality-evidence.json) und
[alle 36 Aufgabenstatus](quality-task-audit.md) sind versioniert. CI verwendet denselben
Einstieg und archiviert ausschließlich synthetische technische Artefakte.

## Was für alle 36 Aufgaben abgedeckt ist

Die Matrix übernimmt das dynamische registrierte Inventar: `bridge_01`–`bridge_09`,
`market_01`–`market_09`, sechs Geschichten, sechs Experimente und sechs Dorfszenarien.
Es werden keine Inhalte nur aufgrund ihrer ID als bestanden gewertet.

Je Aufgabe und Profil: tatsächliches Laden/Validieren, drei neue Starts ohne
Restaktionen, existierende große/fokussierbare Controls mit ergänzenden deutschen
Labels, horizontale Grenzen, Scrollen zu Anfang/Ende, Lösung über Spielcontrols,
persistierter konkreter Abschluss mit Reload, rücknehmbarer Erfolg, Mute und
Rückkehr zum Hub. Profile: **320×568, 360×800, 768×1024, 1024×768**.
Zusätzlich: frische Installation, simuliert fehlgeschlagener atomarer Schreibzugriff
unter Erhalt des alten Saves, kaputte optionale Felder, Tastaturfokus, Abbruch
animierter Beispiele, Retry sowie System-Back-Handler in allen Bereichen.
Die vorhandenen synthetischen Touchprüfungen bleiben Bestandteil der vollen Suite.

Die Ergebnismatrix ist softwaretechnisch, keine Beobachtung von Kindern. Sie
ersetzt weder echte Touch-/Tastaturhardware noch die komplette manuelle
Barrierefreiheitsprüfung. 96×72 logische Pixel sind ein Projektziel, kein
automatischer Nachweis physischer Zielgröße oder WCAG-Konformität.

## Gefundene und behobene Probleme

1. **Fokusverlust in Aufgabe-03-Modulen:** Beim Einstieg und nach einem Umbau
   konnte kein aktives Spielelement mehr fokussiert sein. Die erste erweiterte
   Prüfung scheiterte an acht Fokusassertions. Einstieg, Aktionen, Undo und
   freiwillige Elternansicht erhalten jetzt einen passenden Fokus. Die gezielte
   Regression besteht (15 Assertions über alle fünf Bereiche).
2. **Einstiegsorientierung bei langen Telefonansichten:** Vorratsfokus konnte
   den Anfang aus dem sichtbaren Bereich bewegen. Ein neuer Durchlauf setzt die
   Scrollposition zurück und fokussiert zunächst die Navigation; spätere
   Spielaktionen behalten ihren sinnvollen Quell-/Zielfokus. Zwei zusätzliche
   Einstiegsassertions waren vor der Behebung rot; danach besteht die
   Bereichsregression mit zehn Assertions.
3. **Ergebnisintegrität des Werkzeugs:** Ein früher GUT-Parsefehler konnte als
   Prozess-Exit 0 mit null Tests enden. Der Launcher prüft daher zusätzlich Log,
   JUnit, positive Assertions und vollständige aktuelle Fallmatrix. Negative
   Unittests verhindern, dass so ein Lauf künftig grün wird.

Es wurden keine vorhandenen Tests entfernt, deaktiviert oder in Nulltests
umgewandelt. Die Änderungen an Spielcode beschränken sich auf Fokus-/Scroll-
Lebenszyklus; Inhalte, Regeln, lokale Speicherung und alle fünf Bereiche bleiben
bestehen.

## Inhalts-/Gestaltungsprüfung und Grenzen

| Bereich | Technisch geprüft | Inhaltlicher Review / verbleibende Unsicherheit |
| --- | --- | --- |
| Brücke, 9 | alle Aufgaben und Profile | Formen/Punkte statt reinem Farbcode, reversible Wege; Bedeutung der kleinen Piktogramme und langes Scrollen mit Kindern offen |
| Markt, 9 | alle Aufgaben und Profile | Apfel/Birne durch Form unterschieden, keine Fruchtstrafe; Mengenvergleich/Teilen ohne Lesen empirisch ungeprüft |
| Sprache, 6 | alle Aufgaben und Profile | 3–5 Karten, Replay/Blättern, alternative Ordnungen technisch definierbar; Klang ist keine natürliche Narration, Hörverstehen nicht nachgewiesen |
| Selbstständigkeit, 6 | alle Aufgaben und Profile | reversible Versuche, mehrere Lösungen wo vorgesehen; physikalisch vereinfachte Regeln, Ziel-/Reglerbilder mit Kindern noch prüfen |
| Dorf, 6 | alle Aufgaben und Profile | unterschiedliche Bedürfnisse, freundliche Figuren, keine Moralpunkte, optionale Impulse; kulturelle/soziale Deutungen nicht auf Codebedürfnisse reduzieren |

Im Quell-/Inhaltsreview keine Pflichtleseeingabe, Zeitstrafe, verpflichtende
Erwachsenenaktion, Kauf-/Trackingmechanik oder beschämende Rangliste gefunden.
Das ist ein begrenzter Review der vorliegenden Version, kein Gütesiegel.
Insbesondere Screenreader-Semantik, reale DPI, alle Kontrast-/Fokuszustände und
Verständlichkeit der Symbole bleiben manuell zu prüfen.

## Rendernachweis

```bash
DISPLAY=:99 GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 \
  bash tests/qa/render.sh /tmp/kinderwelt-quality-renders-checked
```

Virtuelles X11, Mesa llvmpipe, Audio-Dummy. Alle 72 Aufgabe/Viewport-Paare wurden
aufgenommen, insgesamt 112 Scrollseiten. Kontaktübersichten/Einzelbilder wurden
zur technischen Sichtprüfung verwendet. Kontrollierte Captureseiten deaktivieren
Fokus-Nachscrollen nur im Aufnahmeprozess und verwenden den effektiven Scrollbar-
Bereich; das ist keine veränderte Spieleinstellung. Der virtuelle Treiber warnt
lediglich, dass V-Sync nicht umschaltbar ist; keine Skript-/Renderingfehler.
Dies sind keine Bilder echter Kinder/Geräte, keine FPS-Messung und kein Hörtest.

## Offene Freigaben

Die [Checkliste](child-usability-checklist.md) nennt Erwachsenen-Vorprüfung,
kindgesteuerte kurze Sitzungen, Stopregeln, echte Geräte und Assistenztechnik.
Die [leere lokale Vorlage](observation-sheet.md) ist freiwillig und standardmäßig
nicht aktiv. Keine Personendaten, Cloudexporte oder Rekrutierung wurden eingeführt.
Die [Lernhypothesen](learning-hypotheses.md) trennen In-game-Mastery, Usability und
kontrolliert zu prüfenden Transfer. Für alle empirischen Aussagen bleiben
Daten/geeignete Verfahren und eine separate Schutzentscheidung erforderlich.
