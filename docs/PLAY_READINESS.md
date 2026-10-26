# Google Play: vorbereitete Entscheidungen, keine Uploadfreigabe

Die App ist ein lokales Lernabenteuer für Klasse 1–2. Der Betreiber hat eine endgültige Paketkennung noch nicht entschieden. Testkennung und stabiler Vorschaukanal bleiben erhalten. Es wurden **keine Release-Schlüssel erzeugt**, keine Play-Daten eingetragen und keine Freigaben erteilt. [Android bauen](android.md) · [technischer Prüfstand](QUALITY_ASSURANCE.md) · [Geräte- und Erwachsenenabnahme](ACCEPTANCE.md).

## Vor einer Veröffentlichung entscheiden und erledigen

| Voraussetzung | Stand / konkrete nächste Entscheidung |
|---|---|
| Herausgeber und Kontakt | Offen: verantwortlicher Name/Firma, erreichbare Supportadresse und dauerhafte Datenschutz-URL. Keine erfundenen Kontaktdaten verwenden. |
| Endgültige Paketkennung | Offen; bisherige Testkennung ausdrücklich nur für Entwicklung. Mit `--package-id` technisch konfigurierbar. Nach erster Veröffentlichung lässt sich die Paketkennung nicht als normales Update austauschen. |
| Release-Signierung | Offen: Play App Signing und separaten Uploadschlüssel kontrolliert einrichten. Privaten Schlüssel ausschließlich in einem gesicherten Schlüsselspeicher/CI-Secret, mit geschützter Sicherung und dokumentiertem Wiederherstellungsweg verwahren. Kein Schlüssel im Git, PR, öffentlichen Artefakt oder Chat. Entwicklungszertifikat ist keine Release-Freigabe. |
| Zielgruppe und Families | Voraussichtlich Kinder im Grundschulalter; Auswahl der Play-Altersgruppen durch Betreiber. Aktuelle Families-/Zielgruppenrichtlinien prüfen, ebenso Darstellung/Ansprache und alle verwendeten Komponenten. Keine Werbung oder Käufe integriert. |
| Datenschutz / Data Safety | Technischer Ausgangspunkt unten; Betreiber muss Angaben zu App, Vertriebsweg und eigener Supportverarbeitung überprüfen und rechtsverbindlich freigeben. |
| Inhalts-/Altersfreigabe | Play-Fragebogen vollständig und wahrheitsgemäß beantworten. Freundliche Gespenster, Figuren und Aufgaben tatsächlich ansehen; keine Altersfreigabe erfinden. |
| Medien und Stimmen | Herkunft/Notices vorhanden; vor öffentlicher Nutzung Nutzungsrechte, Namens-/Persönlichkeitsrechte und konkrete Lizenzpflichten prüfen. Qwen veröffentlicht keine separate Datasetlizenz. Keine pauschale weltweite Rechtefreiheit behaupten. Private Familienbilder/-figuren bedürfen einer eigenständigen Veröffentlichungsentscheidung. |
| Geräte, Hören, Fachprüfung | Vollständige Abnahme nach `ACCEPTANCE.md` weiterhin erforderlich. Technische Tests und ASR ersetzen sie nicht. |
| Store-Eintrag | Titel, Kurz-/Langtext, Kategorie, Kontakt, Icon, Featuregrafik und ausschließlich passende Screenshots vorbereiten. Originales KI-generiertes App-Icon vorhanden; Gestaltung allein ist keine Rechtefreigabe. Familienansichten nicht ohne Entscheidung öffentlich verwenden. |
| Kontospezifische Vorgaben | Aktuelle Play-Console-Vorgaben, ggf. interne/geschlossene Tests und Anforderungen an neue Entwicklerkonten prüfen. Keine angeblich bereits erfüllten Teilnehmer-/Zeitvorgaben behaupten. |
| Bundle / Auslieferung | Vorliegende AABs sind unsigniert; technisch geprüftes Entwicklungsartefakt. Vor Release Ziel-API, Größen-/Gerätedownloadgrenzen, Signierung und Play-Vorprüfung mit den dann geltenden Vorgaben prüfen. Keine Uploadbereitschaft. |

## Technische Grundlage für den Datenschutztext – Entwurf

Kinderwelt benötigt kein Konto und enthält keine Werbung, Käufe, Analytik oder Mikrofon-/Kameraaufnahme. Fragen, Sprachclips, Musik und Bilder liegen lokal. Gesamtpunkte, gelöste Aufgaben, Sprache, Figur/Look, Kulisse und Lautstärkeeinstellungen werden im privaten App-Speicher auf dem Gerät gespeichert. Es werden keine Kinderprofile angelegt. Der aktuelle geprüfte Android-Manifeststand fordert keine Berechtigungen an und deaktiviert Android-Backup. Die Elternfunktion zum Zurücksetzen löscht den lokalen Spielstand; eine Deinstallation löscht üblicherweise ebenfalls diese Daten.

Die App übermittelt diese Spielstände nicht an einen Server. Angaben zu Google Play, Betriebssystem, vom Benutzer selbst exportierten Dateien und Kontaktaufnahme beim Herausgeber müssen gesondert korrekt beschrieben werden; die Abwesenheit eigener Telemetrie ist keine Aussage über alle Dienste des Geräts. Supportnachrichten können personenbezogene Daten enthalten. Eine verpflichtende Datenschutz-Erklärung benötigt noch Herausgeber, Kontakt, zutreffende Rechtsgrundlagen und dauerhafte Bereitstellung. Dieser Entwurf ist keine veröffentlichte Datenschutzerklärung oder abschließende Rechtsprüfung.

Für Data Safety ist „nur lokal verarbeitet“ von „erhoben/weitergegeben“ zu trennen. Die Auswahl in der Console anhand des **finalen signierten Builds** und der dann geltenden Definitionen prüfen. Keine automatisch erzeugte Freigabe aus dem Quelltextaudit ableiten.

## Store-Textentwürfe

Keine Aussagen zu nachgewiesener Lernwirkung, Garantien oder angeblicher pädagogischer Zertifizierung.

| Sprache | Titel | Kurzbeschreibung |
|---|---|---|
| DE | Kinderwelt – Lernen entdecken | Rätsel in acht Fächern, eigene Figuren und freiwillige Bonusaufgaben. |
| EN | Kinderwelt – Learning Adventure | Explore eight subjects with characters, puzzles and optional bonus challenges. |
| RU | Мир знаний — приключения | Восемь предметов, герои, загадки и необязательные бонусные задания. |

Langtextgrundlage: 50 Stationen pro Fach mit je zwei freiwilligen Boni; Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch und Geografie. Sprachaufgaben mit eigenem Wortschatz in Deutsch, Englisch oder Russisch. Sieben wählbare Kulissen, Punktefortschritt auf dem Gerät und anpassbare Audioeinstellungen. Keine Konten oder Werbung. Zahlen/Features vor Veröffentlichung mit dem tatsächlich freigegebenen Paket erneut abgleichen. Einträge und Screenshots erst nach den offenen Entscheidungen finalisieren.

## Optional device-local avatar processing (0.9.5)

The parent area can select JPEG, PNG or static WebP through the system document
picker, orient and crop a portrait, or retain a transparent full figure. This optionally processes personal image content **on the device**; it is
not accurate to claim that no personal image is ever processed. Only normalized,
re-encoded pixels are retained in private app storage. No original copy, source
URI or EXIF/GPS/camera metadata is retained, and no image is transmitted by the
app. Backup exclusions apply to this private app copy; the original gallery/cloud
file and system provider behaviour remain outside the app’s control. The original device file remains untouched. Parent removal and reset delete
the private normalized copy and pending file.

The manifest still declares zero permissions and disables backup. Explicit cloud
and device-transfer exclusion rules are additionally verified in the compiled
APK. Synthetic GPS/camera fixtures in all three formats exercise all eight EXIF
orientations, actual runtime re-encoding, restart and deleted-copy behavior. These technical checks do not substitute for native-device
picker/lifecycle/backup tests. See the [implementation and test boundaries](AVATAR_IMPORT_FEASIBILITY.md).

Before approving Data Safety statements, the operator must distinguish local
image processing from off-device collection under the current Play definitions
and check the actual distributed build/SDKs. No console declarations, privacy
publication, target-audience decision or Google Play/Families approval was changed.

## Store and privacy preparation

The [upload checklist and reproducible neutral Store tools](play/README.md) now
provide DE/EN/RU privacy and listing drafts, Data Safety/IARC worksheets and an
inactive Pages template. These are operator-review materials, not published
policies or Console approvals. `--final` refuses unfilled privacy placeholders.
