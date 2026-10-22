# Herkunft aller aktuell verwendeten Spielfiguren

Prüfung vom 22. Oktober 2026. Erfasst sind beide Figurenvarianten mit je sieben Figuren und fünf Looks. Die bestehende Gestaltung wird erhalten; es wurden **keine aktuell eingebauten heruntergeladenen Figurenbilder festgestellt**, die jetzt neu ersetzt werden müssten.

| Figurenbestand | Herkunft | Konkreter Nachweis | Behandlung |
|---|---|---|---|
| Wanja/Ivan, Mischa, Du, Mama, George, Katze – Normalbilder und Kostümatlanten | Hier erzeugte KI-Illustrationen anhand der vom Nutzer bereitgestellten Familienreferenzen | Alle zwölf ursprünglichen PNG-Hashes aus Commit `1da98ae` stimmen exakt mit vorhandenen `image_gen`-Ausgaben unter `generated_images/exec-*.png` überein. Die optimierten heutigen Dateien sind separat per SHA256 erfasst. | Im getrennten privaten Figurenrepository; keine Originalfotos. |
| Nova, Lumi, Karo, Tavi, Zora, Flocke – je fünf Looks | Hier erzeugte neue Fantasiefiguren ohne Familienfotoreferenz | Der heutige Atlas hat nach verlustfreier PNG-Neukompression exakt dieselben RGBA-Pixel wie `exec-d2d1573b-7108-429b-911f-52637d4bfad2.png`. 30 Looks aus einer Originaldatei. | Öffentliche Quellen im Hauptrepository bleiben erhalten. |
| Eichhörnchen – Normalbild und vier Kostüme | Hier erzeugte eigene Fantasiefigur | Die ursprünglichen Hashes entsprechen exakt `exec-4a1bdf7f-91ee-4515-af5c-8bd6e8fa5961.png` und `exec-8d673d6a-3470-4d65-a980-0da63e2c7aa1.png`; aktuelle verkleinerte Dateien sind gesondert gehasht. | In beiden Varianten gemeinsam verwendet. |
| Frühere Mina/Leo/Sam/Jule-Bilder | Herkunft in den untersuchten historischen Dateien nicht hinreichend belegt | Historische PNG-Hashes aus Commit `3909c4c` erfasst; diese vier Bilder sind bereits seit dem Austausch gegen Familienfiguren nicht mehr eingebaut. | Aktive Ressourcen und Android-Pakete dürfen sie nicht enthalten. Keine rechtliche Bewertung der alten Dateien behauptet. |

Maschinenlesbare Herkunft: `art/character-origins.json`. `scripts/qa/character_origins.py` prüft die tatsächlichen aktuellen Bildhashes und den materialisierten Figurenbestand. Android-Exporte führen diese Prüfung vor dem Export aus. Ungeprüfte Austauschdateien oder umbenannte fremde aktive PNGs führen zu einem Fehler. Die Android-Prüfung sperrt weiterhin die vier alten Bildnamen und kontrolliert die gewählte Figurenvariante.

Diese Prüfung unterscheidet **eigene Fantasiegestaltung ohne Bildreferenz** von **neu generierter Familienillustration mit Nutzerreferenz**. „KI-generiert“ bedeutet nicht automatisch „urheberrechtsfrei“. Die nachgewiesene Herkunft ersetzt keine weltweite juristische Freigabe oder Prüfung auf jede denkbare Ähnlichkeit. Vorhandene alte Git-Commits werden durch diese Änderung nicht gelöscht oder umgeschrieben.
