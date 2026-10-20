# Datenschutzhinweise — Entwurf, nicht zur Veröffentlichung freigegeben

Stand: 20.10.2026. Gilt als Prüfvorlage für den vorliegenden Kinderwelt-Build.
Vor Veröffentlichung müssen verantwortliche Stelle, erreichbarer Kontakt,
Rechtsgrundlagen, Rechte und öffentlich erreichbare Richtlinien-URL durch den
Betreiber passend zur tatsächlichen Veröffentlichung ergänzt und geprüft werden.
Diese Angaben sind derzeit **nicht festgelegt**; es werden keine Kontaktdaten erfunden.

Kinderwelt bietet fünf Spielbereiche mit 36 Aufgaben. Die vorliegende App benötigt
kein Konto. Sie enthält keine Werbung, Käufe, Analyse- oder Trackingintegration.
Die technische Paketprüfung muss für jeden finalen Build erneut bestätigen,
dass keine zusätzlichen Berechtigungen/SDKs oder Datenübertragungen hinzukamen.

Spielstände (erledigte Aufgaben, interne Empfehlungen in Logik/Mathematik) und
Einstellungen für Ton und Bewegung werden lokal im privaten App-Speicher
abgelegt. Es werden keine Namen, Geburtsdaten, E-Mail-Adressen oder
Gesprächsantworten abgefragt. Trotzdem können lokale Spielstände in einem
konkreten Nutzungskontext einer Person zugeordnet werden. Sie sind deshalb
nicht pauschal als anonym zu bezeichnen. Android-App-Backup ist ausgeschaltet.
Andere Nutzer desselben entsperrten Geräts können Spielstände unter Umständen
sehen. Es gibt keine separate Kontentrennung.

Der vorliegende Quellstand enthält keinen Upload von Spielständen und keine
automatische Forschungsdatenerhebung. Erwachsene können freiwillig mitsprechen;
die App zeichnet Gespräche nicht auf. Beobachtungsbögen im Repository sind
inaktive Vorlagen und werden nicht in die Android-App gepackt. Eine spätere
Untersuchung benötigt eine gesonderte Entscheidung, geeignete Schutzmaßnahmen
und altersgerechte, freiwillige Beteiligung.

Lokale Daten bleiben bis zum Zurücksetzen in der App, Löschen der App-Daten oder
Deinstallation bestehen; ein System- oder Gerätesicherungsvorgang außerhalb der
App ist separat zu beurteilen. Die App hat keinen serverseitigen Datenbestand,
auf den diese Vorlage eine Auskunft oder Löschung beziehen könnte. Support,
Store-Nutzung und die Datenverarbeitung durch Google/Android sind gesondert zu
bewerten; dieser Entwurf macht keine Zusagen über deren Verarbeitung.

## Play Data Safety — auszufüllende Prüfvorlage, nicht abgesendet

| Frage/Kategorie | Vorläufige technische Grundlage | Owner-Prüfung |
|---|---|---|
| Erhebung/Weitergabe außerhalb des Geräts? | Kein app-eigener Netzwerkpfad/keine Berechtigungen vorgesehen; statische Prüfung und konkrete Paketprüfung separat ansehen. | Definitionen der aktuellen Console und sämtlicher finaler SDKs prüfen. |
| Personenkennungen, Kontakt, Standort, Finanzen, Gesundheit? | Keine entsprechenden App-Eingaben/SDKs vorgesehen. | Jede Console-Kategorie einzeln bestätigen. |
| Fotos, Dateien, Audio, Nachrichten? | Keine Aufnahme/Abfrage; Tonhinweise werden lokal erzeugt. | Finale Manifest-/SDK-Prüfung bestätigen. |
| App-Aktivität/Leistung/Diagnostik/Geräte-IDs? | Spielstände lokal; keine App-Analyse/Crash-Uploadintegration. | Prüfen, ob finale Abhängigkeiten oder Distributionsdienste zusätzliche Angaben erfordern. |
| Verschlüsselung/Löschung? | Kein App-Upload; Android-Sandbox, lokales Zurücksetzen. | Nicht ungeprüft Netzwerkverschlüsselung versprechen; aktuelle Console-Fragen passend beantworten. |
| Kinder/Zielgruppe? | Kindgerechte Spielinhalte, kein Konto, keine Werbung. | Tatsächliche Altersgruppen, Families und Datenschutzrecht fachlich prüfen. |

Keine personenbezogenen Daten oder Kinderbeobachtungen wurden für diese
Build-Arbeit erhoben. Diese Vorlage ersetzt keine Betreiberprüfung.
