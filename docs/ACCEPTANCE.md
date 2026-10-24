# Manuelle Abnahme und Evaluation

Aktueller technischer Stand und Nachweise: [Qualitätsüberblick](QUALITY_ASSURANCE.md). Diese Anleitung beschreibt **noch auszuführende** menschliche Prüfungen. Ein bestandenes Skript, eine ASR-Transkription oder eine angekreuzte Selbstauskunft ersetzt keine unabhängige Fachprüfung und keinen Nachweis einer Lernwirkung.

## Erwachsene: vollständige Hörprüfung

Die bisherigen weiblichen Stimmen bleiben erhalten. Bei jedem Clip zuerst ohne Text hören, dann mit Text vergleichen: Wortanfang, Wortende, Zahlen/Rechenzeichen, Verneinung, Verständlichkeit und Betonung. In RU besonders Kasusformen und reduzierte Vokale; in DE zusammengesetzte Wörter; in EN unter anderem *th*, Endkonsonanten und zusammengesetzte Wörter. Die englische Schreibweise *stalk* kann im gewählten Akzent ähnlich wie *stork* klingen; ASR allein entscheidet solche Fälle nicht. Für jede Sprache eine Person mit sicheren muttersprachlichen Kenntnissen einsetzen.

```sh
python3 scripts/qa/review_pack.py prepare --output build/listening-acceptance
# index.html öffnen; falls der Browser lokale Medien blockiert:
python3 -m http.server 8765 --bind 127.0.0.1 --directory build/listening-acceptance
# Dann http://127.0.0.1:8765 öffnen. Nur auf dem eigenen Rechner erreichbar.
python3 scripts/qa/review_pack.py verify --receipt /pfad/kinderwelt-listening-review.json --locale ru
```

Der Quality-Actionslauf stellt es separat als `kinderwelt-full-listening-review` bereit; sieben Tage Aufbewahrung, kein dauerhaftes Freigabearchiv. ZIP entpacken und `index.html` öffnen.

Das Paket enthält **jede unterschiedliche tatsächlich ausgelieferte Sprachaufnahme**, mit allen verwendenden Aufgaben-/Hinweis-IDs und SHA-256. Gleiche Aufnahmen müssen nicht mehrfach gehört werden. Die Seite enthält keine Familienbilder, Modelle, Zugangsdaten oder Aufnahmefunktion. Erwarteter Text ist zunächst verborgen; Markierungen sind eigene Erklärungen des prüfenden Erwachsenen. Kein automatisches Speichern: Ergebnisse freiwillig als lokale JSON-Datei exportieren. Exportierte Ergebnisse können über „Frühere Ergebnisse fortsetzen“ wieder eingelesen werden, sofern die Hashes noch stimmen. Teilprüfungen bleiben `INCOMPLETE`; auffällige Aufnahmen `ISSUES`. `DECLARED_REVIEW_COMPLETE` bedeutet nur vollständig vorliegende, an aktuelle Text-/Audiohashes gebundene Selbstauskünfte. Das Werkzeug bezeugt weder die Person noch das tatsächliche Hören. Dateien aus verschiedenen Inhaltsständen dürfen nicht vermischt werden. Kein Personenname oder freier Kommentar ist im Format vorgesehen.

Die kompakte `kinderwelt-listening.html` im Android-Artefakt eignet sich für erste Stichproben. Sie ersetzt die vollständige Abnahme nicht. Auffälligkeiten anhand der Aufgaben-ID und einer Fehlerkategorie melden, ohne Angaben zu Kindern. Bei Änderungen an Aufnahme, Pegel oder Aufgabenkontext alte Freigaben erneut prüfen. Für langfristige Freigaben gelten die verifizierten Ablageregeln aus dem Qualitätsüberblick.

## Android: praktische Geräteprüfung

Ausgabe nach `qa-results/` oder private Testablage; keine neuen Einzelprotokolle im Git. Ergebnis je Schritt: **bestanden / fehlgeschlagen / nicht ausgeführt**, dazu App-Commit, APK-SHA, Version, Paket, Geräteklasse/Androidversion und konkrete reproduzierbare Schritte. Keine Seriennummer, Konto-, Kinder- oder Standortdaten erfassen.

| Prüfung | Ablauf | Erwartung |
|---|---|---|
| Erststart | Je eine neutrale und eine Familien-Test-APK installieren; offline starten | Richtiger Figurensatz; kein Login, Netzwerkzwang oder Berechtigungsdialog |
| Bedienung | In DE/EN/RU alle acht Fächer, letzte Station, beide Boni, Überspringen, sieben Kulissen, Figuren und Looks bedienen | Alles erreichbar; keine Antwort hinter Navigation/Punkteanzeige; Überspringen ohne Strafe |
| Rotation | Offene Aufgabe und Bonus mehrfach Hoch-/Querformat drehen, auch bei großer Schrift; kleine und große Displays | Aufgabe, Auswahl und Gesamtpunkte bleiben erhalten; keine Verzerrung, Überdeckung oder unbedienbare Ziele |
| Audio | Lautsprecher, kabelgebundene/Bluetooth-Kopfhörer; niedrige und normale Lautstärke; Musik an/aus; Frage früh beantworten | Ganze Frage vor Lob, klare Wörter; Musik abgesenkt; kein hörbarer Schnitt, Übersteuern oder unerwarteter Sprachwechsel |
| Unterbrechung | Während Frage, Lob und Musik jeweils Home/Appwechsel, Bildschirm aus/an; danach zurückkehren | Kein Hintergrundton; keine fortlaufende Wischgeste; Fortsetzung ohne doppelte Punkte oder verlorene Aufgabe |
| Prozessneustart | Punkte verdienen, App verlassen und Prozess beenden, neu starten | Gleiche Gesamtpunkte, Sprache, Kulissen und Looks; Wiederholung vergibt keine neuen Punkte |
| Update | Auf **derselben** Paketkennung und demselben Entwicklungszertifikat Vorgänger installieren, Punkte/Einstellungen notieren, neue APK darüber installieren | Keine Deinstallation; Einstellungen/Punkte erhalten. Bei Zertifikatsabweichung stoppen, nicht Daten löschen |
| Randfälle | Flugmodus, voller/knapper Speicher, mehrere schnelle Antworten, häufige Rotation, Android-Zurück | Kein Absturz; Speichermeldung verständlich; endliche, korrekte Punkte |

Nur für das eigene autorisierte Testgerät: `adb install -r DATEI.apk` aktualisiert bei passender Signatur. Ein `INSTALL_FAILED_UPDATE_INCOMPATIBLE` ist ein Abbruchgrund; kein automatisches Deinstallieren. Für die Abnahme mindestens ein kleines, leistungsschwaches Gerät und ein weiteres Displayformat wählen. Emulatorergebnisse getrennt kennzeichnen. Desktop-Godot-Notifications und Fenstergrößenänderungen sind keine Android-Geräteprüfung.

## Unabhängige Inhaltsprüfung

Je Fach und Sprache alle 50 Grundaufgaben und beide Boni ansehen/hören. Referenzquellen: [Redaktionsquellen](CONTENT_AUTHORING.md), `science-properties.tsv`, `science-models.json`, `pedagogy-base.tsv` und aktuelle generierte Aufgaben. Prüfen: sachlich richtige und eindeutige Lösung, plausible falsche Optionen, Bild-/Begriffsübereinstimmung, kurze verständliche Sprache, Hinweis mit Denkschritt ohne Lösung, Bonus tatsächlich anspruchsvoller und freiwillig, Zahlraum/Lesebelastung passend. Konkrete Gegenbeispiele sind wichtiger als Kategorienübereinstimmung.

Besonders: Fahrradhelm gegenüber weichen Mützen; Pilze gegenüber Pflanzen; erwachsene Tiere gegenüber Entwicklungsstadien; Eisen gegenüber beliebigen Metallen; Baumwolle gegenüber beliebigem Stoff; Wärmezustände bei zwanzig Grad; sichtbarer Nebel gegenüber unsichtbarem Wasserdampf; Symbolbild gegenüber tatsächlicher Form eines Sterns. Aussagen gelten für die genannten Unterrichtsmodelle. Die Entwicklerdurchsicht und automatische Konsistenzprüfung sind **keine unabhängige fachpädagogische Freigabe**. Die Quellenrecherche ist hier teilweise durch HTTP 403 blockiert; daraus wird kein erfolgter Quellenabgleich abgeleitet.

## Kindgerechte Beobachtung – keine Datenerhebung als Standard

Zunächst kann ein vertrauter Erwachsener die App mit dem Kind freiwillig ausprobieren, ohne Aufzeichnung oder personenbezogenes Protokoll. Kind entscheidet selbst über Figur, Sprache, Fach, Bonus und Pause. Keine Zeitlimits, Noten oder Aufforderung, trotz Unbehagen fortzufahren. Keine Kamera-/Mikrofonaufnahme oder Telemetrie aktivieren. Nur reproduzierbare Appfehler ohne Angaben zum Kind dokumentieren.

Praktischer Ablauf, etwa zehn bis fünfzehn Minuten: Figur wählen → ein vertrautes Fach → ein Sachrätsel → Hinweis → freiwilliger Bonus oder Überspringen → Kulisse wechseln → App schließen/neustarten. Erwachsene helfen erst auf Wunsch und beobachten: erkennt das Kind die nächste Aktion, versteht es die Frage ohne sichtbaren Text, helfen Hinweise beim Denken, bleibt eine falsche Antwort respektvoll, funktioniert das Überspringen? Unverständnis ist ein Verbesserungshinweis für die App.

Eine **wissenschaftliche Untersuchung** benötigt vorher eine gesonderte Entscheidung: Forschungsfrage, verantwortliche Stelle, Rechtsgrundlage/Datenschutzkonzept, Einwilligung der Sorgeberechtigten und Zustimmung des Kindes, Abbruch-/Löschverfahren, Datenminimierung und Zugriffsschutz. Eine Kennnummer macht Daten nicht automatisch anonym. Bis dahin keine personenbezogenen Forschungsdaten erfassen.

Vor einer Wirksamkeitsstudie Hypothesen und Auswertung festlegen: primäres Ergebnis z.B. Übertragung auf neue, nicht in der App geübte Aufgaben; parallele Vor-/Nachtests und geeignete Vergleichsbedingung; Zuteilung/Gegenbalancierung, Vorwissen, Unterstützung und Abbrüche berücksichtigen; Stichprobenumfang begründet planen; verzögerter Test zur Behaltensleistung. Punktegewinn, Zufriedenheit und erfolgreich gelöste bekannte Bilder sind keine Lernwirkungsnachweise. Usability-Beobachtungen zunächst formativ auswerten; keine kausalen Aussagen aus einer kleinen Gelegenheitsstichprobe.
