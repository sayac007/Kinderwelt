# Kinderwelt 0.4: tatsächliche Testlieferung

Stand: 20.10.2026. Anwendungscode: **`e69bb70`**, Basis `origin/main` mit gemergtem PR #7.
Der Build entstand mit sauberem Arbeitsbaum (`source_dirty: false`). Spätere Änderungen
betreffen Mess-/Renderhilfen und Dokumentation, nicht den gelieferten Anwendungscode.
[Maschinenlesbare Belege](modern-evidence.json), [Bedienung und Architektur](modern-experience-v04.md).

## Erzeugte Artefakte

Im Cloud-Arbeitsbereich: `/workspace/Kinderwelt/build/android-0.4-final/`.

| Datei | Bytes | Tatsächlich geprüfter Status |
|---|---:|---|
| `kinderwelt-debug.apk` | **65764990** | gültige Entwicklungssignatur v2 |
| `kinderwelt-unsigned.aab` | **55406003** | Bundletool-validiert, bewusst unsigniert |

APK SHA-256: `1108a8203646d6847d7854c33369a8962d503288829f19dcb50225bfa66d1ea8`.

AAB SHA-256: `6b2a7ee1713aa8eb153478c0d35140a0f3c831f8528076068c02395889b05034`.

Daneben liegen `provenance.json`, `verification.json`, `size-analysis.json`, vollständige
Import-/Exportlogs und die tatsächlichen Manifest-, Signatur- und Bundletool-Ausgaben.
Verifiziert: ZIP-Integrität, **208 Anwendungsassets**, alle alten Module, neue Mission,
Musik-/Sprachimporte, Paket `org.example.kinderwelt`, **Version 0.4.0 / Code 4**, min SDK 24,
Target SDK 36, `arm64-v8a` + `x86_64`, keine Android-Berechtigungen, Backup aus, `fullUser`,
16-KB-ELF-Kompatibilität, APK-Signatur/ZIP-Ausrichtung und komprimierte native Libraries
mit `extractNativeLibs=true`. Keine privaten Schlüssel oder Entwicklungsdateien gepackt.

Die APK ist **65,76 MB statt 164,12 MB** groß: rund **59,93 % weniger**, trotz der neuen
Inhalte. Der 120-MB-Zielwert ist erreicht. Verlustfrei komprimierte native Bibliotheken
sind die Hauptmaßnahme; ihr entpackter Inhalt ist hashgleich zur alten APK. Installierter
Speicher und Play-Gerätedownload sind nicht gemessen. [Vollständige Größenanalyse](apk-size-v04.md).
Es wurde kein Release-Schlüssel benutzt, kein Play-Upload und keine Freigabe durchgeführt.

## Tatsächlich ausgeführte Tests

| Prüfung | Ergebnis |
|---|---|
| Vollständige QA | **PASS**, `/tmp/kinderwelt-04-qa-final/report.json` |
| Vier bisherige Spieltestsuiten | **1236 Checks**, 0 Fehler: 33 + 559 + 59 + 585 |
| Bestehendes Adventure | **679 Checks**, 0 Fehler; alle drei bisherigen Varianten bleiben spielbar |
| Neue Plattform/Referenzmission | **285 Checks**, 0 Fehler; Karten-Touch, nativer ScrollContainer im Touch-Emulationsmodus, keine versehentliche Ortsöffnung, Figurenwahl/Persistenz, Rohrgraph, alle Varianten, Inventar, Drag-and-drop, Rand-Abbruch, Zustand/Wiederaufnahme, Wachstumsnachweis nach Wasserstopp, beschädigte/fremde Nachweise, zehn Player-Inhalte, Favorit/Zufall, Sprache und Ducking |
| Statischer QA-Prüfer | 16 Python-Tests bestanden, statischer Audit ohne Befunde |
| Gepinntes GUT-Upstream | 13 Tests, 62 Assertions, 0 Fehler/Skips |
| Bisherige Aufgabenqualität | 6 GUT-Tests, **13001 Assertions**, 0 Fehler/Skips |
| Bisherige Experience-Qualität | 6 GUT-Tests, **22909 Assertions**, 0 Fehler/Skips |
| Vollständigkeit | Alle **36 Aufgaben × 4 Viewports = 144 Fälle**, PASS |
| Android-/Medien-Python | **24 Tests bestanden**, `/tmp/kinderwelt-04-android-final.log`; einschließlich Decoderprüfung realer Audiodaten, eindeutiger Notenfolgen, negativer Paket-/Manifestfälle und Größenbilanzierung |
| Neue Oberflächen | **70 echte Godot-Renderframes**, fünf Profile einschließlich großer Schrift und simulierter hoher DPI; alle vier Hero-Posen erzeugen unterschiedliche Bilder |
| Bestandsaufgaben-Grafik | **146 Frames**, alle 36 Aufgaben auf zwei Viewports, PASS |
| Bisherige Experience-Grafik | **44 Frames**, einschließlich Dichtesimulation, PASS |
| Bisheriger Pico-Prototyp | **45 Frames**, fünf Profile, PASS |
| Android-Export | Import, APK-Export, AAB-Export und finale technische Paketprüfung jeweils PASS |
| Desktop-Ressourcenmessungen | Headless und X11/llvmpipe mit Dummy-Audio gemessen, keine Android-Prognose |

Die bisherigen Assertions bleiben erhalten. Die alte Erwartung „zwei Audio-Regler“ wurde
wegen des verlangten dritten Sprachreglers zu drei erweitert; Musik-/Effektpersistenz
wird weiterhin geprüft. Der bisherige WAV-Loop-Test berücksichtigt zusätzlich den neuen
Vorbis-Codec. Neue Suiten müssen getrennte nichtleere, erfolgreiche Resultatzeilen liefern.
Fehlende/neutrale Läufe werden nicht als PASS interpretiert.

Der Start-Smoke-Test öffnet weiterhin die echte Hauptszene für 60 Frames. Er verwendet
jetzt anschließend den regulären Produktions-Schließpfad: Narration und Audiostreams
stoppen, Mixer darf freigeben, dann beendet sich die Engine. Das vorherige harte
`--quit-after` umgeht diesen Pfad und meldete bei aktiven Vorbis-Streams Ressourcen am
Engine-Ende. Fehler wurden nicht aus Logs herausgefiltert; die endgültigen Läufe enthalten
keine solchen Engine-Fehler. Der Produktions-Fensterabschluss benutzt denselben Abbau.

GitHub Actions wurde um neue Render-/Messläufe und explizite FFmpeg-Installation für die
Decoderprüfungen erweitert. Das ist **kein Nachweis eines hier beobachteten grünen Remote-Laufs**;
die obigen Ausführungen fanden tatsächlich lokal in dieser Cloud-Umgebung statt.

## Performance: Messbereich ausdrücklich begrenzt

Gemessen bei 360×800, isoliertem lokalen Zustand und frischem XDG-Cache. Der Dateisystemcache
wurde nicht systemweit geleert. Audioausgabe: Dummy, **keine Hardware-Latenzmessung**.

| Messgröße | Headless | Software-OpenGL/X11 (llvmpipe) |
|---|---:|---:|
| Prozessstart bis zwei fertige Projektframes | 0,17 s | **9,77 s** |
| Szenenaufbau innerhalb bereits gestarteter Engine, erster Projektaufbau | 91 ms | ca. 381 ms |
| Gesamter Messprozess, einschließlich Szenenwechsel, Animation und Abbau | 1,45 s | 12,18 s |
| Maximaler Linux-Prozess-RSS | 128312 KiB | 263796 KiB |
| Gleichzeitig geladene Musikslots | höchstens 2 | höchstens 2 |

Die genaue Szenen-/Audio-/Frameverteilung steht im JSON. **Der Softwaregrafik-Kaltstart ist
langsam** und wird nicht mit der wesentlich kürzeren Szenenaufbauzeit verwechselt. Seine
Einzelursachen innerhalb der Engine-/Grafikinitialisierung wurden nicht weiter isoliert.
Diese Zahlen belegen weder Android-Startzeiten noch Android-RAM, Akkuverbrauch oder
ruckelfreies Verhalten auf günstigen Telefonen. Dafür ist ein echter Geräte-Lauf offen.
Es wird kein Vorher-Nachher-Performancegewinn aus der APK-Kompression abgeleitet.

## Screenshots und dokumentierte Sichtprüfung

Die Bilder sind unveränderte Godot-Ausgabe aus dem Xorg-Dummy-/Mesa-Backend, kein Mockup:

- [Karte oben](modern-screenshots/small_map.png), [Kartenverlauf](modern-screenshots/phone_map-bottom.png).
- [Vier Kinder](modern-screenshots/phone_heroes.png), [Bewegen](modern-screenshots/phone_heroes-move.png), [Denken](modern-screenshots/phone_heroes-think.png), [Erfolg](modern-screenshots/phone_heroes-success.png).
- [Musikbox](modern-screenshots/phone_musicbox.png).
- [Einstieg](modern-screenshots/small_water-0.png), [Fortgeschritten](modern-screenshots/phone_water-1.png), [Experte gelöst](modern-screenshots/phone_water-solved-2.png).
- [Querformat](modern-screenshots/landscape_water-solved-2.png), [hohe Dichte](modern-screenshots/dense_water-solved-0.png), [große Schrift](modern-screenshots/large-text_water-2.png).

Sichtgeprüft wurden ausgewählte reale Ansichten von Karte, Figuren, Posen, Musikbox und
allen Missionstufen auf kleinem Telefon, Querformat und hoher Dichte. Befunde führten zu
kürzeren Beschriftungen, einheitlichen eigenen Vektorsymbolen statt uneinheitlicher Emoji-
Menüs, korrigiertem Kartenabstand, klaren Rohr-/Pflanzenebenen und passender Querformat-
Anordnung. Der Pflanzenfortschritt wurde zusätzlich nach Schließen des Hahns abgesichert.
Nicht jedes der 305 erzeugten Bilder wurde manuell vollständig abgenommen. Die drei
Bestands-Renderläufe verwenden Laufzeitstand `c74e7fa`; danach änderte sich nur die
Pflanzenmission. Deren 70 Bilder und vollständige Funktionstests wurden erneut mit dem
gelieferten Stand ausgeführt. Die spätere Messhilfe `72d2424` wurde separat tatsächlich
ausgeführt und verändert keine exportierten Anwendungsdateien.

Zwischenprüfungen fanden außerdem Timer-Callbacks auf bereits entfernte Figuren,
zu lange Beschriftungen, eine falsche Button-Icon-Property und ein nach Wasserstopp
zurückgenommenes Wachstum. Diese Befunde wurden mit WeakRefs, kurzen Beschriftungen,
eigenen korrekt eingebundenen SVG-Symbolen und geprüften lokalen Erfolgsnachweisen behoben.
Die Tabelle enthält ausschließlich die erfolgreichen abschließenden Läufe.

## Offene Prüfungen und nicht erreichte Qualitätsziele

- **Kein reales Android-Gerät und kein Emulator installiert/getestet.** Installation,
  Update, Systemleisten, Notches, echte Finger, Audioausgabe, App-Unterbrechung, Startzeit,
  Wärme und langfristige Speicherstabilität bleiben offen.
- **Keine menschliche Hör-/Spielprüfung und kein Kindertest.** Keine nachgewiesene
  Kinderfreundlichkeit, Motivation, Altersangemessenheit oder Lernwirkung behauptet.
- Deutsche Sprache ist ein **synthetischer Prototyp**; natürliche Sprecheraufnahmen fehlen.
  Musik und Original-Comicgrafik sind implementiert, aber nicht als professionelle
  Illustrations-/Konsolenproduktion abgenommen. [Audioquellen und Codecvergleich](audio-v04.md).
- 80-MB-Play-Gerätedownload und installierte App-Größe sind nicht gemessen. Die kompakte
  Universal-APK ist kein Ersatz für diese Werte.
- Alte Bestandsaufgaben wurden erhalten, nicht alle fachlich/illustrativ neu gestaltet
  oder jeweils mit neuen Sprachaufnahmen versehen.
- Bei neuer Debug-Signatur kann ein Update einer bestehenden 0.3-Installation scheitern.
  **Deinstallation löscht lokale Spielstände.** Die kompatible Speicherlogik ist kein
  Beleg einer erfolgreichen Gerätemigration. Vorzugsweise ein separates Testgerät nutzen.
- Veröffentlichung bleibt blockiert: dauerhafte sichere Signatur, Paketidentität,
  Datenschutz-/Familien-/Zielgruppenangaben, Altersfreigabe, Store-Eintrag und manuelle
  Gerätefreigabe. Bestehende Play-Checklisten bleiben offen und unverändert verbindlich.

[Praktisches freiwilliges Gerätetestprotokoll](modern-device-checklist.md).
