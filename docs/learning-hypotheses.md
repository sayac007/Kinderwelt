# Lernhypothesen und wissenschaftliche Evaluationsvorbereitung

## Strikte Trennung der Aussagen

1. **Technische Evidenz:** Eine definierte Codeversion lädt, eine Aufgabe ist mit
   den implementierten Regeln lösbar, Controls/Speicherung funktionieren in den
   geprüften Abläufen. Das sagen automatisierte Tests aus.
2. **Pädagogische Hypothese:** Ein Spielmechanismus könnte bestimmte Tätigkeiten
   anregen. Dies ist eine prüfbare Annahme, keine nachgewiesene Verbesserung.
3. **Empirische Evidenz:** Beobachtete Verständlichkeit oder ein kontrollierter
   Effekt bei tatsächlich untersuchten Personen, mit beschriebenem Verfahren,
   Unsicherheit und Grenzen. **Solche Daten liegen hier nicht vor.**

App-Abschlussmarkierungen, eine automatisch gelöste Aufgabe, Wiederholen, Likes
oder ein grüner CI-Lauf belegen weder Entwicklungsfortschritt noch Marktreife.
Aktuell gilt für pädagogische Wirksamkeit und realen Transfer: **NOT ESTABLISHED**.
Es wurden keine Effektgrößen, Teilnehmerzahlen oder Leistungsmessungen erfunden.

## Hypothesen zu den fünf Bereichen

| Bereich / Mechanik | Falsifizierbare Arbeitshypothese | Innerhalb des Spiels beobachtbar | Separat zu prüfender Transfer / zentrale Grenze |
| --- | --- | --- | --- |
| Brücken: begrenzte Teile, Undo, alternative Aufteilungen | Wiederholte Exploration könnte Planung und flexible Strategieänderung anregen | Neuversuche, freiwilliges Undo, passende Aufteilung einer bekannten Lücke | Neue materielle/anders dargestellte Planungsaufgabe; bloßes Wiedererkennen derselben Mengen reicht nicht |
| Markt: Abgleich, Vergleich, Sortieren, Teilen | Sichtbare Manipulative könnten Mengenbeziehungen verständlich machen | Zuordnung in vorgegebenen Körben, Hilfe bei Vergleich/Sortieren | Ungeübte Gegenstände und andere Darstellungen; App-Regelwissen ist kein allgemeiner Zahlensinn |
| Bildergeschichte: Bild-/Klangfolge, 3–5 Karten | Bildsequenzen könnten zeitliche Ordnung und eigenes Erzählen anregen | Reihenfolge einer vorgeführten Geschichte, eigene plausible Erzählung | Neue Geschichte unabhängig vom geübten Material; Tonfolgen sind keine natürliche Narration und prüfen kein sprachliches Hörverstehen allein |
| Experimente: reversible Einstellungen, Zielbild | Freie Versuche könnten selbstgewählte Strategieprüfung unterstützen | Einstellungen variieren, Ergebnis ansehen, freiwillig erneut versuchen | Unbekannter Mechanismus außerhalb der App; Spielmodelle sind keine physikalisch exakten Erklärungen und kein Nachweis für Selbstregulationsfähigkeit |
| Dorf: unterschiedliche Bedürfnisse, Ideenbilder | Unterschiedliche Perspektiven könnten Gespräch und Aushandlung anregen | Wunschbilder erkennen, alternative Pläne auswählen, freiwilliges Gespräch | Neue kooperative Situation mit unabhängigen Beobachtenden; Auswahl einer hinterlegten Lösung ist kein Empathie- oder Moraltest |

Erwachsenenhilfe, Lesefähigkeit, Motorik, Sprach-/Symbolvertrautheit, vorherige
Spielerfahrung, Müdigkeit, Motivation und kulturelle Deutungen können Ergebnisse
beeinflussen. Sie dürfen nicht als Defizit eines Kindes interpretiert werden.
Nicht sinnvolle alternative Geschichten oder Dorfideen als „falsch“ voraussetzen;
Abweichungen können ebenso ein Inhalts-/Gestaltungsproblem zeigen.

## Phase A: technische und erwachsene formative Vorprüfung

Alle Gates und Befunde in `quality-system.md`/`test-report.md` prüfen. Erwachsene
gehen zunächst Aufgaben ohne Lesen, ohne Ton, mit reduzierter Bewegung und mit
den vorgesehenen Eingabemitteln durch. Fehler reproduzieren, priorisieren und
Regressionen ergänzen. Kein Kind zum Debuggen eines bekannten kritischen Fehlers
heranziehen. Zugänglichkeit auf realen Geräten bleibt ein eigener Prüfpunkt.

Werkzeugtests nutzen etablierte Verfahren: Godot-Import/Start und GUT 9.7.1 mit
benannten unveränderten Upstream-Tests; technische Assertions sind keine neue
kindliche Entwicklungsnorm. Es wird kein „Kinderwelt-Entwicklungsbenchmark“
gebaut. Für eine spätere freiwillige Erwachsenenbewertung kann ein etabliertes
Usability-Instrument wie **SUS** nach Brooke (1996) erwogen werden: Original-
Instrument und passende validierte Sprachfassung beschaffen, Nutzungsbedingungen
prüfen, unveränderte Auswertung vorab festlegen. Die Standardinterpretation ist
nicht ohne Weiteres auf Kinder oder elterliche Fremdurteile über Kinder
übertragbar. Hier wurde SUS weder durchgeführt noch als eigener Fragebogen
nachgebaut; keine SUS-Werte werden behauptet.

## Phase B: formative Kinder-Usability, nicht Wirksamkeitsstudie

Nur nach gesonderter Entscheidung zu Aufsicht, Schutz, Einwilligung und Daten:
[child-usability-checklist.md](child-usability-checklist.md). Die Teilnahme ist
freiwillig, das Kind stimmt fortlaufend zu und darf jederzeit abbrechen. Eltern
sind Begleitung, keine obligatorischen Mitspieler oder Bewertenden.

Ziel ist das Auffinden von Bedien-/Verständnisproblemen. Primäre Fragen vorab
festlegen, etwa „Ist der erste eigenständige Spielzug ohne Textanweisung möglich?“
oder „Kann eine selbst gewählte Aktion zurückgenommen werden?“. Mehrere kurze,
variierte Aufgaben sind geeigneter als 36 Pflichtaufgaben pro Kind. Beobachtungen
zum Abschluss, Hilfebedarf, sichtbarer Belastung, freiwilliger Rückkehr und
Zugangshürden nur nach freigegebenem Minimalplan erheben. Nichtbeobachtung,
Abbruch, nicht angebotenes Verhalten und technisches Scheitern unterscheiden.

Die optionale Vorlage enthält keine Teilnehmerverknüpfung. Deshalb lässt sich
mit ihr insbesondere keine saubere längsschnittliche Lernkurve schätzen.
Aufgabenversuche sind nicht unabhängige Teilnehmende. Kleine freiwillige Sitzungen
liefern Gestaltungsbefunde, keine normierten Kompetenzwerte und keinen kausalen
Lerneffekt. Auch zufriedene Eltern oder freiwillige Rückkehr belegen keinen
Transfer; Nicht-Rückkehr ist kein Nachweis mangelnden Lernens.

## Phase C: erst separat zu planende kontrollierte Evaluation

Vor Rekrutierung, Datensammlung oder Aussagen über Wirkung benötigt diese Phase
eine eigene Entscheidung und qualifizierte methodische/ethische Begleitung.
Nicht mit Phase-B-Bögen oder Spielständen improvisieren.

1. **Fragestellung/Population:** Einen eng begrenzten, entwicklungsangemessenen
   primären Lernbereich, Einschlusskontext und notwendigen Zugangsvoraussetzungen
   definieren. Keine verdeckte Generalisierung auf alle Kinder. Zugänglichkeit
   verbessern, statt unpraktisch erreichbare Gruppen still auszuschließen.
2. **Vorabplan:** Hypothese, primäres Transfermaß, Vergleich, Auswertungszeitpunkte,
   Umgang mit Abbrüchen/fehlenden Werten und Mehrfachtests präregistrieren.
   Ergebnismaße müssen unabhängig von den eingeübten App-Aufgaben sein.
3. **Vergleich:** Randomisierte Zuweisung, sofern sinnvoll und vertretbar, zu
   aktiver Vergleichsaktivität mit ähnlicher Spielzeit, Aufmerksamkeit und
   Erwachsenenbegleitung. Kein Entzug notwendiger Unterstützung, keine
   erzwungene Bildschirmzeit. Baseline und Exposition transparent erfassen.
4. **Messqualität:** Etablierte, alters-/sprachangemessene Instrumente nur mit
   passender Nutzungsberechtigung und Qualifikation einsetzen. Bei Beobachtungs-
   rubriken unabhängige, möglichst verblindete Bewertende, Training und
   Interrater-Reliabilität vorsehen. Keine neue Normskala aus Spielpunkten ableiten.
5. **Transfer/Zeit:** Geübte Spielaufgabe, ungeübten Nahtransfer und gegebenenfalls
   verzögerten Ferntransfer getrennt operationalisieren. Den Abstand für einen
   verzögerten Termin vorab begründen; aktuell gibt es keine Follow-up-Daten.
6. **Stichprobe:** Erforderliche Größe aus Präzisions-/Powerplanung mit begründeter
   minimal relevanter Differenz und belastbarer Varianzannahme bestimmen. Keine
   frei erfundene Teilnehmerzahl oder erwartete Prozentverbesserung einsetzen.
   Familiäre/klassenbezogene Cluster und wiederholte Aufgaben berücksichtigen.
7. **Analyse:** Analyseeinheit ist in der Regel das Kind, Aufgaben sind darin
   verschachtelt. Gruppendifferenzen, Effektgrößen und Unsicherheitsintervalle
   berichten; Baseline-/Cluster-/Mehrfachtestplan einhalten. Intention-to-treat
   beziehungsweise begründeten Umgang mit Exposition vorab festlegen. Keine
   nachträgliche Auswahl ausschließlich erfolgreicher oder wenig unterstützter
   Durchläufe. Abbrüche nicht als mangelnde Fähigkeit klassifizieren.
8. **Schutz/Daten:** Minimale benötigte Daten, getrennte Einwilligungsorganisation,
   geeignete Rechts-/Ethikprüfung, lokale/gesicherte Verarbeitung, Löschplan und
   Zugriffsrollen festlegen. Gegebenenfalls notwendige Pseudonyme sind keine
   Anonymität und werden nicht mit dieser Implementierung eingeführt.
9. **Bericht:** Null-/negative Ergebnisse, unerwartete Belastung und Grenzen
   veröffentlichen, sofern die dafür nötigen Freigaben vorliegen. Eine Änderung
   des Lernmaterials begrenzt die Übertragbarkeit alter Befunde auf neue Versionen.

Bis dahin zulässige Aussage: „Das Spiel bietet Tätigkeiten an, die diese
Hypothesen motivieren; technische Funktionsfähigkeit ist geprüft.“ Unzulässig
wäre „verbessert nachweislich Sprache/Empathie/Selbstständigkeit“ oder „marktreif“.

## Reale Geräte: etablierte technische Messung, derzeit NOT MEASURED

Es stand kein physisches Zieltelefon/-tablet zur Verfügung. Virtuelles X11,
Cloud-CPU und Headless-Testdauer sind keine Gerätebenchmarks. Gemessen wurden
keine Kaltstartzeit, FPS-/Frametime-Stabilität oder Geräte-Speicherwerte.

Für spätere Messungen mit vorhandenen realen Geräten vorab festlegen:

- Gerätetyp/Modell (keine Seriennummer), OS, Godot-/Buildcommit, Renderer,
  Auflösung, Energie-/Temperaturzustand, Debug-/Release-Einstellungen und
  repräsentative Spielszenen dokumentieren. Aufgabe 05 hier nicht vorwegnehmen.
- **Start:** klar definierten Prozess-Kaltstart bis zur ersten nutzbaren
  Eingabe prüfen. OS-/Dateicachezustand getrennt benennen. Mehrere Wiederholungen,
  Median und Streuung statt eines günstigsten Einzelwertes berichten.
- **Stabilität:** Godot-Profiler/Performance-Monitore auf dem Gerät beziehungsweise
  ein etabliertes Plattformwerkzeug verwenden; dieselbe Spielsituation und
  Aufzeichnungsdauer vorab festlegen, Frametimes/Spitzen statt nur Durchschnitts-FPS
  dokumentieren. Keine Cloudwerte als Telefonleistung ausgeben.
- **Speicher:** benanntes OS-Maß (z.B. RSS/Private Bytes) und Werkzeug konsistent
  verwenden; Idle, repräsentatives Spiel und wiederholte Rückkehr zum Hub prüfen.
  Unterschiedliche Speicherdefinitionen nicht als vergleichbare Werte behandeln.
- Erst nach realer Baseline begründete technische Budgets festlegen. Diese wären
  Produktanforderungen, keine pädagogischen Entwicklungsbenchmarks.

## Bezugspunkte und Grenzen der Quellen

- GUT 9.7.1: [offizieller gepinnter Quellstand und Kompatibilität](https://github.com/bitwes/Gut/tree/v9.7.1),
  [versionsbezogene Dokumentation](https://gut.readthedocs.io/en/v9.7.1/).
  Versionsmatrix und benannte Upstream-Tests wurden tatsächlich geprüft.
- W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/): Orientierung unter anderem an
  Tastaturbedienung, sichtbarem Fokus, Ausrichtung, Farbe, Kontrast und Zielgröße.
  Logische Godot-Pixel sind nicht automatisch CSS-Pixel; die Projektziele sind
  kein WCAG-Zertifikat. Vollständige Konformität wurde nicht geprüft.
- UNICEF Office of Research (2013), **Ethical Research Involving Children (ERIC)**:
  Bezugspunkt für Respekt, Zustimmung und Schutz bei Forschung mit Kindern;
  institutionelle Prüfung und konkrete Rechtsgrundlage bleiben erforderlich.
- Brooke, J. (1996), **SUS: A quick and dirty usability scale**, in Jordan et al.,
  *Usability Evaluation in Industry*: optionaler Erwachsenen-Usability-Bezug,
  kein Kinder-Entwicklungsbenchmark und hier nicht eingesetzt.

Die W3C-/UNICEF-Webseiten waren in dieser Umgebung beim Abruf durch das Netz mit
403 gesperrt. Sie werden als fachliche Bezugspunkte genannt, nicht als hier
vollständig neu gelesene oder angewandte Prüfverfahren. Vor einer Studie sind
aktuelle Originalunterlagen und lokale Vorgaben durch die Verantwortlichen zu
beschaffen. Keine Quelle ersetzt die noch fehlenden empirischen Ergebnisse.
