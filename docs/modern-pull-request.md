## Kinderwelt 0.4: gemeinsame Plattform statt weiterer Adventure-Regeln

Reale 0.3-Tests zeigten eine zu statische, textlastige Oberfläche und eine zu komplexe
Referenzaufgabe. Diese Änderung ergänzt eine illustrierte Abenteuerkarte für die fünf
bestehenden Bereiche, vier auswählbare animierte Kinder, eine gemeinsame Offline-Narration
und die tatsächlich spielbare Pflanzenmission mit drei fachlichen Stufen. Rohre werden
angetippt oder gezogen; Quelle, Anschlüsse, Lecks und Wasserbudget werden simuliert.
Gewachsene Pflanzen bleiben nach Wasserstopp und Wiederaufnahme erhalten. Picos Kraftwerk
und die bisherigen 36 Aufgaben bleiben verfügbar; virtuelle Raumpfeile entfallen.

Die Musikbox enthält zehn unterschiedliche reale Stücke, Cover, Vorschau, Transport,
Zufall und Merken. Sprache, Musik und Effekte sind getrennt regelbar; Sprache senkt die
Musik ab. Die deutsche eSpeak-Stimme ist ausdrücklich ein synthetischer Prototyp.

Die APK-Analyse isolierte unkomprimierte native Libraries als Hauptursache: Verlustfreie
ZIP-Kompression bei beiden ABIs senkt die Universal-Debug-APK von 164,12 auf **65,76 MB**.
Entpackte native Inhalte sind hashgleich. AAB **55,41 MB**, unsigned und technisch geprüft.
Version 0.4.0/4. Keine Release-Schlüssel und keine Play-Freigaben verwendet.

Validiert: 1236 ursprüngliche + 679 Adventure- + 285 neue Checks; vollständige QA mit
144 Aufgaben/Viewport-Fällen und beiden bisherigen GUT-Suiten; 24 Android-/Audio-Python-
Tests; 70 neue + 146 Aufgaben- + 44 Experience- + 45 Pico-Renderframes. Desktop-Messungen
unterscheiden Prozessstart von Szenenaufbau und erfassen RSS sowie begrenzte Audio-Ladeslots.
CI erhält neue Render-/Messschritte, FFmpeg-Decoderinstallation und Größenberichte.

[Prüfbericht und tatsächliche APK-/AAB-Pfade](docs/modern-test-report.md),
[Bedienung und Architektur](docs/modern-experience-v04.md),
[Größenanalyse](docs/apk-size-v04.md), [Screenshots](docs/modern-screenshots).

Offen: reale Android-Installation/Updates, Systemleisten, Leistung und Hör-/Kindertest.
Software-OpenGL-Prozessstart war im frischen virtuellen Grafikcache 9,77 s; keine Android-
Prognose. Natürliche Sprachaufnahmen, professionelle Medienabnahme, tatsächliche Play-
Downloadgröße und sämtliche Veröffentlichungsfreigaben bleiben offen. Keine behauptete
pädagogische Wirksamkeit oder Marktreife.
