# Freiwillige Usability-Prüfung mit Kind und Begleitung

**Vorbereitetes Protokoll, noch nicht ausgeführt.** Es wurden keine Kinder
rekrutiert, beobachtet oder vermessen. Die App erhält keinen Studienmodus,
keine Telemetrie, keine Cloud-Exporte und keine Erfassung personenbezogener Daten.
Ein grüner Softwaretest ist keine Freigabe für eine Untersuchung.

Die vorhandenen lokalen Spielstände speichern Aufgabenmarkierungen und
Einstellungen. Auch solche Daten können auf einem gemeinsam bekannten Gerät
indirekt zuordenbar sein. Sie werden hier nicht als Forschungsdaten ausgelesen
oder exportiert; die automatisierten Prüfungen verwenden ausschließlich eigene
synthetische Daten. Eine tatsächliche Studie benötigt ihr separat festgelegtes
Vorgehen auch für diese lokalen Spielstände.

## 0. Vor jeder Datenerfassung gesondert entscheiden

- [ ] Zweck, verantwortliche Stelle, zuständige Aufsicht und geeignete ethische/
  datenschutzrechtliche Prüfung festlegen. Dieses Dokument ersetzt sie nicht.
- [ ] Datenerfassung separat autorisieren; verständliche Information und passende
  Sorgeberechtigten-Einwilligung sowie die fortlaufende Zustimmung des Kindes
  organisieren. Ein Nein oder Stoppen ist jederzeit ohne Nachteil möglich.
- [ ] Standard ist **kein Beobachtungsbogen und keine Speicherung**. Nur wenn
  eigens freigegeben, die minimale lokale Vorlage verwenden; kein automatischer
  Start und keine Cloud-Synchronisation.
- [ ] Keine Namen, Geburtstage/Altersangaben, Schule, Anschrift, Kontaktdaten,
  Diagnosen, Teilnehmerkennungen, präzisen Sitzungszeiten, Foto-/Ton-/Video-
  aufnahmen oder Freitext-Zitate erfassen. Auch vermeintlich anonyme
  Verhaltensangaben können im kleinen Kontext zuordenbar sein.
- [ ] Einwilligungs-/Organisationsdaten gegebenenfalls getrennt und geschützt
  halten. Nicht mit der lokalen Vorlage verknüpfen. Für eine Längsschnittstudie
  nötige Kennungen wären eine neue, gesondert zu prüfende Entscheidung.
- [ ] Falls überhaupt Daten erhoben werden: minimaler Zugriff, Aufbewahrungs- und
  Löschfrist vorab festlegen; Papier verschlossen oder freigegebene lokale
  Verschlüsselung. Keine privaten Cloudordner, E-Mail, Git oder CI-Artefakte.
  Kleine/seltene Beobachtungskombinationen nicht als „anonym“ veröffentlichen.

## 1. Erwachsenen- und Gerätevorprüfung, bevor ein Kind spielt

- [ ] Vollständigen QA-Bericht für die richtige Codeversion prüfen; bekannte
  kritische Fehler beheben. Nicht getestete Aspekte ausdrücklich offen lassen.
- [ ] Auf dem **tatsächlich verwendeten Gerät** Hub, alle fünf Bereiche, Zurück,
  Wiederholung, Hilfen und die Erwachsenenansicht selbst durchspielen.
- [ ] Gerät stabil halten, angenehme Lautstärke zuerst leise testen, Pause und
  Exit erklären. Kopfhörer nicht voraussetzen; kein plötzliches lautes Signal.
- [ ] Aufgaben ohne Ton sowie mit reduzierter Bewegung bedienen. Es gibt keine
  Sprachausgabe; Bilder müssen die Bedeutung tragen. Klangfolgen allein sind
  kein belegter Ersatz für natürliche Erzählung.
- [ ] Touch-/Mausziele ohne Präzision treffen, Fehl-Tipps korrigieren und mit
  Tab/Pfeiltasten/Enter vollständig navigieren. Fokus muss sichtbar und die
  Reihenfolge sinnvoll sein; lange Ansichten müssen erreichbar scrollen.
- [ ] Kleine/Tablet-Ansichten, Hoch-/Querformat, DPI und Systemschrift prüfen.
  Keine abgeschnittenen Ziele, verdeckten Controls oder zwingende Texteingabe.
- [ ] Text-/Symbolkontrast, aktiv/ausgewählt/deaktiviert sowie Hinweise prüfen.
  Formen müssen auch ohne Farberkennung unterscheidbar bleiben. Prüfung ist
  kein bereits erbrachter WCAG- oder Screenreader-Konformitätsnachweis.
- [ ] Benötigte Assistenztechnik am Zielsystem tatsächlich testen. Nicht
  voraussetzen, dass die prozeduralen Bilder durch Tooltips vollständig
  screenreaderzugänglich sind. Bei unzureichender Zugänglichkeit erst anpassen,
  nicht das Kind als gescheitert einordnen.
- [ ] Keine reale Familien-/Schulerfahrung, sensible Geschichte oder belastende
  Situation als Pflichtbeispiel abfragen. Dorf-Regeln als vereinfachte Spielwelt
  behandeln, nicht als moralisches Urteil über das Kind.

## 2. Kurze, kindgesteuerte Sitzung

Plan: etwa 10–15 Minuten als **obere Orientierung**, keine Mindestspieldauer.
Ein Kind wählt selbst Reihenfolge und Umfang; 3–5 kurze Aufgaben reichen oft.
Nicht alle 36 Aufgaben in einer Sitzung verlangen. Über mehrere freiwillige
Durchläufe können die Bereiche und unterschiedliche Aufgaben abgedeckt werden.
Die Reihenfolge zwischen Durchläufen variieren; daraus ohne Teilnehmenden-
zuordnung keine unabhängigen Stichprobenzahlen oder Wirkungsanalysen ableiten.

Einstieg in einfacher Sprache: „Du kannst etwas ausprobieren. Es ist kein Test,
bei dem du gut sein musst. Du darfst Hilfe nehmen, etwas anderes wählen oder
aufhören.“ Die begleitende Person darf auf Wunsch mitdenken; sie hat keine
exklusiven Spielaktionen. Keine Belohnung für das Fertigspielen und kein Drängen.

| Schritt | Neutrale Anleitung | Beobachtbares, sofern separat freigegeben |
| --- | --- | --- |
| Hub erkunden | „Welches Bild möchtest du ausprobieren?“ | Eingang gefunden / Hilfe gesucht / andere Wahl |
| Erstversuch | „Was möchtest du hier versuchen?“ | Aktion, Fehl-Tipp, selbstständige Korrektur |
| Hinweis | „Du darfst Hilfe nehmen.“ | Selbst angefordert oder angeboten; welche Stufe |
| Rückgängig/Exit | „Du kannst etwas ändern oder zurückgehen.“ | Undo, Retry, Hub erreichbar |
| Freies Weitergehen | „Du darfst weiterspielen oder aufhören.“ | freiwillig anderes Spiel / freiwillige Rückkehr / Stop |
| Erwachsenenimpuls | Nur auf Wunsch die Sprechblase öffnen | Blockiert die Ansicht? Übernimmt jemand unfreiwillig? |

Nicht jede Stille, Pause oder falsche Anordnung bedeutet Frustration. Falls eine
Beobachtung genehmigt ist, nur beobachtbare Signale markieren: ausdrücklich um
Pause/Stop gebeten, wiederholt nach Hilfe gefragt oder dasselbe Ziel nicht
getroffen. Keine Diagnose und keine Zuschreibung „unmotiviert/ungeduldig“.
Auch ein vom Erwachsenen übernommener Abschluss ist kein Solo-Erfolg des Kindes.

## 3. Bereichsspezifische Prüfaufgaben

- **Brücke (9):** Punkte/Längen und Restlücke ohne Zahlen erklären lassen;
  alternative Aufteilungen, Sackgasse, Hilfe/Rückgängig und Überquerung beobachten.
  Eine andere Idee darf ausprobiert werden; keine Strafsprache.
- **Markt (9):** Formen/Mengen sehen, Sortieren, Vergleichen, Teilen und neutrale
  Plätze für gemischte Früchte erkennen. „Fair“ nicht aus gleicher Menge ableiten.
- **Bildergeschichte (6):** Bild-/Klangfolge und manuelle Pfeile verstehen,
  3–5 Karten legen/entnehmen; eigene Erzählung zulassen. Eine alternative plausible
  Erzählung als Inhaltsfrage notieren, nicht als Sprachdefizit des Kindes werten.
- **Experimente (6):** Fahne als Ziel, Regler, Versuch und Ergebnis unterscheiden;
  eigene Reihenfolge/mehrere Versuche zulassen. Die Modelle sind Spielregeln,
  keine präzisen naturwissenschaftlichen Modelle.
- **Dorf (6):** zwei unterschiedliche Wünsche und offene Umrisse verstehen;
  passende Alternativen und andere soziale Deutungen zulassen. Nicht fragen,
  „welches Kind ist gut/schlecht“. Erwachsene unterstützen nur freiwillig.

Für eine vollständige Inhaltsabnahme eine Aufgabenmatrix aus dem technischen
Inventar verwenden und jede der 36 Aufgaben manuell kennzeichnen: nicht gesehen,
Erwachsenen-Walkthrough, Kind freiwillig gewählt, ungeklärtes Problem. Diese
Abdeckungsplanung ist kein Grund, Kinder zum Abarbeiten aller Aufgaben zu drängen.

## 4. Stoppen und nachbereiten

Sofort Pause/Ende anbieten bei Stopwunsch, erkennbarer Belastung, wiederholtem
Feststecken oder unerwarteter Geräte-/Datenschutzsituation. Kein Nachfragen nach
persönlichen Gründen nötig. Bei technischem Soft-lock nur Erwachsene den Zustand
sichern/beenden lassen; keine Rohdaten/Identitäten an GitHub hängen.

Am Ende optional: „Was möchtest du ändern?“ Keine Lernverbesserung nahelegen.
Abbruch/Überspringen ist ein legitimer Ausgang und kein Misserfolg. Lokale Saves
auf einem gemeinsam verwendeten Gerät vor der nächsten Sitzung nach dem
vereinbarten Vorgehen zurücksetzen; Forschungsbögen liegen nie im Spielstand.

Freigegebene Beobachtungen nur beschreibend zusammenfassen: Aufgabenversuche,
Hilfebedarf, Zugänglichkeitsprobleme und beobachtbare Stop-/Rückkehrentscheidungen.
Wiederholte Versuche desselben Kindes sind keine unabhängigen Teilnehmenden.
Keine Aussagen über Aufmerksamkeit, Intelligenz, Empathie oder Lernwirkung aus
kleinen freiwilligen Sitzungen ableiten.

Optionale, leere [lokale Beobachtungsvorlage](observation-sheet.md). Hypothesen und
kontrollierte Untersuchung: [learning-hypotheses.md](learning-hypotheses.md).
