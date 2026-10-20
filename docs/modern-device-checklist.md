# 0.4: noch auszuführender Smartphone-Test

Status: **NICHT AUSGEFÜHRT**. Desktop-Softwaregrafik, synthetische Touch-Ereignisse und
Paketprüfungen sind keine Installation auf einem Android-Telefon.

## Erst Erwachsene, dann freiwillig das Kind

- Endgültige APK aus `build/android-0.4-final/` und deren Hash aus dem Prüfbericht verwenden.
  Gerätetyp und Android-Version als technische Angaben reichen; keine Seriennummern oder
  personenbezogenen Kinderangaben erfassen.
- Eine alte APK kann anders debug-signiert sein. Ein Update wird dann abgewiesen.
  **Nicht einfach deinstallieren: Dabei gehen lokale Spielstände verloren.** Vorzugsweise
  ein separates Testgerät verwenden. Ein Update-/Migrationsnachweis fehlt ohne den alten
  Entwicklungsschlüssel; zukünftige stabile Entwicklungssignierung sicher außerhalb des
  Repositorys einrichten. Es wurde kein Release-Schlüssel verwendet.
- Installation, Offline-Start im Flugmodus, tatsächliche Startzeit und belegten Speicher
  prüfen. Die ZIP-Kompression reduziert die APK, native Bibliotheken werden jedoch entpackt.
- Alle fünf alten Orte öffnen und vorhandenen Fortschritt prüfen, sofern ein reguläres
  Update mit passendem Schlüssel möglich ist. Speicherformat bleibt kompatibel; das ist
  kein Nachweis einer gelungenen Geräteinstallation.

## Bedienung und Referenzmission

- Karte kurz antippen und langsam/schnell wischen; kein unbeabsichtigtes Öffnen beim Wischen.
  Scrollbalken und alle Orte, Figur, Musik, Klang und Eltern sollen erreichbar sein.
- Vier Figuren wählen, App vollständig beenden und neu öffnen. Auswahl und Animationen
  prüfen, auch mit reduzierter Bewegung. Unterschiedliche Figuren müssen gleich lernen können.
- Pflanzenmission: Aufgabenstart hören, Hören erneut antippen, Automatik ausschalten und
  gezielt wiederholen. Standard-Autoplay, Stumm und drei getrennte Lautstärken prüfen.
- Rohre mit kurzen Bewegungen antippen, über weite Strecken ziehen, am Bildschirmrand und
  außerhalb loslassen. „Legen“ als Alternative ohne Ziehen prüfen. Mehrere Finger und eine
  während des Ziehens unterbrochene App dürfen keinen unerwarteten Zug auslösen.
- Alle drei Varianten lösen. Offene Enden und falsche Anschlüsse erkennen lassen, Undo
  verwenden. Im Expertenmodus auch ein zusätzlich leckendes T-Stück testen: Beide Pflanzen
  erreichbar, aber Budget reicht nicht. Erfolg bei sechs benötigten Tropfen ohne Leck.
- Nach Erfolg den Hahn schließen: Die Pflanzen sollen gewachsen bleiben. App beenden und
  wiederaufnehmen. „Neu versuchen“ darf nur diese Variante zurücksetzen.
- Hoch-/Querformat, kleine Displays, hohe DPI, große Schrift, Gestenleiste und Notch prüfen.
  Das Spielfeld darf keine Wischbewegung benötigen. Längere Menüs dürfen erkennbar scrollen.
- Im Hintergrund warten, zurückkehren, Telefon sperren/entsperren. Fortschritt und Audio
  dürfen nicht verloren gehen oder doppelt anlaufen. Wärme, Ruckler und Abstürze beobachten.

## Audio und subjektive Qualität

- Alle zehn Cover anhören, Auswahl wechseln, vorher/nachher, Zufall und Merken prüfen.
  Favorit muss bei Ortswechsel bleiben, ohne Merken sollen passende Situationen wechseln.
- Auf Telefonlautsprechern und optional Kopfhörern: Melodie, Bass, Rhythmus, Übergänge,
  hörbare Loopstellen, Clipping und angenehme Lautstärke prüfen.
- Während Sprache muss Musik leiser sein; nach Ende, Abbruch, Stumm oder App-Wechsel darf
  keine dauerhafte Absenkung bleiben. Synthetische Stimme auf verständliche Aussprache prüfen.
- Natürliche deutsche Sprachaufnahmen und professionelle Musik-/Illustrationsabnahme fehlen.
  Die vorhandene Stimme bewusst als Prototyp bewerten, nicht als Veröffentlichungston.

## Freiwillige Beobachtung mit dem Kind

Erst nach dem technischen Erwachsenentest. Beteiligung und Begleitung sind freiwillig;
das Kind kann jederzeit aufhören. Keine Fotos, Videos, Stimmen, Namen oder Nutzungsprofile
aufnehmen. Ohne gesonderte Entscheidung und Schutzmaßnahmen keine personenbezogenen Daten
sammeln. Keine Cloud-TTS, kein Mikrofon und keine Telemetrie werden dafür eingesetzt.

Beobachten: Findet das Kind die Werkstatt, versteht es den gesprochenen Auftrag und das
Drehen/Versetzen? Helfen Wasserfluss und Lecks? Ist Einstieg sinnvoll, bleibt Experte
fachlich interessant? Lassen sich Fehler ohne Frust beheben? Sind Musik und Figuren
ansprechend? Rückmeldungen als freiwillige allgemeine Hinweise beschreiben. Ein gelöstes
Rätsel belegt weder Lernwirkung noch langfristige Motivation oder Altersangemessenheit.

Datenschutz, Zielgruppe Kinder, Altersfreigabe, Store-Eintrag und sämtliche Play-Freigaben
bleiben separate offene Schritte der bestehenden Release-Checkliste.
