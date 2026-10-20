## Erste testbare Adventure-Mission

Kinderwelt 0.2 ist gemergt. Diese Iteration ergänzt ausschließlich „Picos Kraftwerk“:
eine steuerbare Figur mit Tap-to-walk, Pico, drei verbundene Räume, ein Ressourcenrätsel
mit drei Varianten (Standard Tüftler), mehreren Lösungen und freigeschalteter Sternwarte.
Der Prototyp ist oben im Hauptmenü erreichbar. Die fünf bisherigen Spiele bleiben erhalten.

Simulation, Bewegung, Welt, Interaktionen, validierter lokaler Fortschritt und Musikregister
sind getrennt. Zwei eigene elektronische Titel mit Melodie, Bass und Rhythmus sind real
enthalten und auswählbar; Lautstärken und globales Stumm bleiben nutzbar. Version 0.3.0/3.

Validiert: 1236 bisherige + 679 neue Checks; vollständige QA inklusive 144 Aufgaben/Viewport-
Fällen und beider bestehenden GUT-Suiten; 21 Android-/Audio-Python-Tests; 45 Adventure-,
146 bestehende Aufgaben- und 44 Experience-Renderframes. Debug-APK und unsigniertes AAB
wurden lokal mit gepinntem Werkzeugstand gebaut und technisch verifiziert. CI erhält den
Adventure-Renderlauf. Keine Release-Schlüssel oder Play-Freigaben geändert.

[Regeln und Gerätetest](docs/adventure-mission.md), [tatsächliche Nachweise und APK-Pfade](docs/adventure-test-report.md),
[maschinenlesbare Ergebnisse](docs/adventure-evidence.json), [Screenshots](docs/adventure-screenshots).

Offen: echte Android-Installation, physischer Touch, Performance, Update mit konsistenter
Debug-Signatur, menschliche Hör-/Spielprüfung und freiwilliger Kindertest. Grafik und Audio
bleiben Prototypen; keine behauptete Lernwirkung, Konsolenqualität oder Marktreife.
Manche Menüs benötigen auf kleinen/quer gehaltenen Geräten oder mit großer Schrift Scrollen;
die Welt selbst nicht. Bekannte Zwei-Audioobjekt-Warnung beim harten headless Boot-Ende bleibt.
Weitere Missionen erst nach dem ersten Gerätetest.
