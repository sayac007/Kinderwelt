# Testbericht · Sprache, Selbstständigkeit, soziales Lernen

Stand: 20.10.2026. Ausgangspunkt `origin/main` bei
`ba759f9` (Merge von PR #2), Branch `feat/language-autonomy-social`.
Die hochgeladene `03_language_autonomy_social.yaml` wurde vollständig gelesen
und per Bytevergleich als identisch mit der Repository-Datei bestätigt.
Implementiert wurden ausschließlich Aufgabe 03 und ihre Integration/Prüfungen.
Alle YAML-Dateien, die Brücken-/Marktlevel und die Android-Konfiguration bleiben
unverändert. Aufgaben 04/05 sind nicht umgesetzt.

## Tatsächlich ausgeführt

Linux x86_64, Godot **4.7.2.stable.official.ed1daf0bf**:

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
```

| Prüfung | Ergebnis |
| --- | --- |
| Baseline auf aktuellem main vor Änderungen | PASS: 651 Prüfungen |
| Finaler Runner | PASS, Exit 0, 1.236 Prüfungen |
| Headless Editor-Import | PASS, keine Skript-/Parse-Fehler |
| `tests/smoke.gd` | PASS: 33 Prüfungen, 0 Fehler |
| `tests/learning.gd` | PASS: 559 Prüfungen, 0 Fehler |
| `tests/input.gd` | PASS: 59 Prüfungen, 0 Fehler |
| Neue `tests/scenarios.gd` | PASS: 585 Prüfungen, 0 Fehler |
| Projektstart `--headless --quit-after 60` | PASS, Exit 0 |
| `git diff --check` | PASS |
| Virtuelles X11-Display / OpenGL Compatibility / Mesa llvmpipe | Alle drei Module gerendert und Screenshots visuell geprüft |
| Physische Geräte, Hörtest, Beobachtung mit Kindern | NICHT AUSGEFÜHRT |
| GitHub Actions für diesen Branch | Hier noch kein Remote-Ergebnis bestätigt |

Die vorhandenen 651 Prüfungen bleiben erhalten. Die Fundament-Suite lädt ihre
ursprünglichen drei Tap-Demos jetzt explizit über den weiterhin unterstützten
Fallback ohne `runtime`, anstatt die neuen Spiele als Tap-Demos zu behandeln.
Keine der 33 Assertions wurde entfernt oder deaktiviert. Im ersten
Integrationslauf machte eine alte Tap-Erwartung den geänderten Spieleinstieg
sichtbar (`play_button` war im echten neuen Runtime nicht vorhanden). Der
Testvertrag wurde entsprechend getrennt: alte Demo-Kompatibilität dort,
registrierte neue Spiele mit vollständigen Spielzügen in der neuen Suite.
Der Runner begrenzt jeden Prozess auf 120 Sekunden und wertet zusätzlich zum
Prozessstatus Godots Fehlerausgaben aus. Jeder Lauf isoliert seine Daten in
temporären XDG-Verzeichnissen; persönliche Spielstände wurden nicht getestet
oder zum Bestehen der Tests verändert.

## Abdeckung der neuen Suite

- Alle fünf Hub-Einträge besitzen spielbare Runtimes; jede neue Sammlung enthält
  mindestens sechs gültige, erreichbar abschließbare Szenarien.
- Alle 18 Szenarien werden über die UI-Steuerung allein abgeschlossen. Offene
  Elternimpulse blockieren keinen Schritt; nach Neustart ohne Elternansicht
  sind ebenfalls Hinweise und vollständige Lösungsbeispiele spielbar.
- Abschluss, freie Szenarienfolge, Rückgängig auch nach Abschluss, Retry,
  Abschluss höchstens einmal pro Durchlauf und jederzeitige Hub-Rückkehr.
- Unabhängige Endzustände: tatsächliche Kartenreihenfolge gegen erlaubte
  Datenfolge; ausgeführter Versuch gegen Zielbild; Mengenbedürfnisse beider
  Figuren gegen die ausgewählte Zuteilung.
- Hinweisleiter: erster Zeigegestus verändert nichts, zweite Hilfe macht einen
  Schritt, dritte Hilfe kann jedes Szenario lösen. Auch falsch begonnene
  Geschichten können über Rückgängig wieder zu einer Lösung gelangen.
- Geschichten: Grenzen, Karten herausnehmen und das Herausnehmen rückgängig
  machen; ungültige Kartenpermutationen und unvollständige Lösungen ablehnen.
- Experimente: **alle** Einstellungen der sechs kleinen Zustandsräume
  durchprobieren, Existenz passender Ergebnisse und einen Hinweisweg aus jedem
  Zustand prüfen; ungültige Einstellungen und unerreichbare Ziele ablehnen.
- Dorf: jede Idee ausprobieren/undo, auch wenn noch Bedürfnisse offen sind;
  ungültige Indizes, überbuchte Ressourcen und nicht erfüllbare Bedürfnisse
  ablehnen. Keine Moralpunkte, Timer, Erfolgsserien oder versteckte Rangstufen
  für die neuen Bereiche.
- Gültige Übersetzungsschlüssel, doppelte Szenario-IDs, fehlende Übersetzungen
  und deutscher Fallback bei fehlender englischer Datei.
- Lokale Speicherung aller neuen Abschlussmarkierungen mit Reload; vorheriger
  Mathematikfortschritt bleibt erhalten; Reset entfernt die neuen Markierungen.
  Stummschaltung verhindert auch Story-Klänge.
- Vollständiger Abschluss eines Szenarios **je neuem Modul** über echte
  `InputEventScreenTouch`-Ereignisse durch Godots Input-System. Enter aktiviert
  Rückgängig bei offener Elternansicht. Diese Eingaben sind synthetisch und
  ersetzen keinen Test mit realer Hand, Maus oder Tastatur.
- Portrait/Landscape bei 360×800 und 1024×600, große Zielbereiche,
  Szenarienwahl im Portrait; die Kartenansicht und Auswahl verwenden passende
  getrennte Spaltenzahlen, damit die Auswahl nicht horizontal überläuft.
- Replay, manuelles Blättern, Neustart und Hub während laufender Bild-/Klang-
  beziehungsweise Hinweisfolgen. Alte Timer dürfen den neuen Zustand nicht ändern.

## Sichtprüfung und ihre Grenzen

Auf einem virtuellen X11-Display wurden eine Geschichte, die Kugelbahn und ein
Dorfszenario bei 900×900 beziehungsweise 900×1000 gerendert, dazu Geschichten und
Dorf bei 360×800. Die tatsächlich erzeugten Screenshots wurden angesehen.
Dabei wurden kompaktere Geschichtenkarten, klare Nullmengen, eine verdeutlichte
Kanal-Zielposition und unterscheidbare Ideenbilder (Kopfhörer/Raumtrennung/
Absprache) ergänzt. Nach den Änderungen besteht der komplette Runner erneut.

Es gab keine Skript-/Renderingfehler. Der virtuelle Grafiktreiber meldet nur,
dass V-Sync nicht umschaltbar ist. Audio lief beim Rendern über den Dummy-Treiber;
die Sichtprüfung ist kein Hörtest. Zusätzlich wurden alle 18 initialen Szenarien auf dem virtuellen Display
gerendert und als Screenshots erfasst (Renderlauf Exit 0, keine Skript-/
Renderingfehler). Beispiele wurden visuell angesehen; nicht jedes einzelne
Motiv wurde separat als manuelle Abnahme bewertet.

## Offene manuelle Abnahme

- Alle 18 Szenarien auf Telefon und Tablet spielen: echtes Touch, DPI,
  Hoch-/Querformat, Scrollen, sichtbare Auswahl und erreichbare Navigation.
- Mit Kindern von 6–8 Jahren ohne sichere Lesekenntnisse beobachten: Werden
  Kartenfolge, Rückgängig, Fahnenziel, Experimentregler und Bedürfnisumrisse
  ohne Erklärung verstanden? Reihenfolge und Symbole ggf. anhand dieser
  Beobachtungen überarbeiten; Softwaretests belegen das nicht.
- Klangfolgen mit realer Ausgabe anhören; Mute und reduzierte Bewegung prüfen.
  Es gibt **keine Sprachausgabe**, keine Sprachaufnahme und keine behauptete
  semantische Verständlichkeit der Töne allein. Narrations-Slots sind dokumentiert.
- Mit physischer Tastatur Tab/Pfeiltasten/Enter sowie Fokus und Scroll-Verhalten
  durch vollständige Abläufe prüfen. Screenreader- und Plattform-DPI-Abnahme
  wurden nicht durchgeführt.
- Dorfideen und Elternimpulse mit Familien auf respektvolle, unterschiedliche
  Deutungen prüfen. Die vereinfachten Ressourcenregeln ersetzen kein Gespräch
  über reale Gefühle, Aushandlung oder Bedürfnisse. Erwachsene sind freiwillig.
- Keine Lernwirkungs-/Geräteleistungswerte erhoben. Keine Umsetzung der
  Qualitäts-/Forschungsaufgabe 04 oder Android-Release-Aufgabe 05 behauptet.

Vollständige Bedienungs- und Autorenhinweise: [scenario-authoring.md](scenario-authoring.md).

Beim abschließenden Review wurde zusätzlich ein Modell-Randfall korrigiert:
`remove(-1)` darf keine unbenutzte Karte als vermeintlich gefüllten Platz
behandeln. Negative/zu große Indizes werden jetzt ohne Zustandsänderung abgelehnt;
alle sechs Geschichten haben dafür eine Regression. Ein eingeklapptes Segel
wird ohne degeneriertes Dreieck gezeichnet.
