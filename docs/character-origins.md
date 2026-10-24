# Herkunft aller aktuell verwendeten Spielfiguren

Scope clarification for 0.9.4: the historical table below concerns **bundled**
project artwork. Optional device-local PNG avatars are user-provided inputs,
not part of the preapproved generation registry or a new project authorship
claim. They are never included in a build or this provenance scan. The
[visual audit](qa/VISUAL_IP_AUDIT.md) and the corrected legacy row below include
the subsequently discovered C2PA evidence. The older description of missing
provenance was incomplete.

Prüfung vom 23. Oktober 2026. Erfasst sind beide Figurenvarianten mit je sieben Figuren und fünf Looks. Die bestehende Gestaltung wird erhalten; es wurden **keine aktuell eingebauten heruntergeladenen Figurenbilder festgestellt**, die jetzt neu ersetzt werden müssten.

| Figurenbestand | Herkunft | Konkreter Nachweis | Behandlung |
|---|---|---|---|
| Wanja/Ivan, Mischa, Du, Mama, George, Katze – Normalbilder und Kostümatlanten | Hier erzeugte KI-Illustrationen anhand der vom Nutzer bereitgestellten Familienreferenzen | Alle zwölf ursprünglichen PNG-Hashes aus Commit `1da98ae` stimmen exakt mit vorhandenen `image_gen`-Ausgaben unter `generated_images/exec-*.png` überein. Die optimierten heutigen Dateien sind separat per SHA256 erfasst. | Im getrennten privaten Figurenrepository; keine Originalfotos. |
| Nova, Lumi, Karo, Tavi, Zora, Flocke – je fünf Looks | Hier erzeugte neue Fantasiefiguren ohne Familienfotoreferenz | Der heutige Atlas hat nach verlustfreier PNG-Neukompression exakt dieselben RGBA-Pixel wie `exec-d2d1573b-7108-429b-911f-52637d4bfad2.png`. 30 Looks aus einer Originaldatei. | Öffentliche Quellen im Hauptrepository bleiben erhalten. |
| Eichhörnchen – Normalbild und vier Kostüme | Hier erzeugte eigene Fantasiefigur | Die ursprünglichen Hashes entsprechen exakt `exec-4a1bdf7f-91ee-4515-af5c-8bd6e8fa5961.png` und `exec-8d673d6a-3470-4d65-a980-0da63e2c7aa1.png`; aktuelle verkleinerte Dateien sind gesondert gehasht. | In beiden Varianten gemeinsam verwendet. |
| Fische, Schildkröten, weitere Objekt-/Tierbilder, Kulissen mit schlafender Katze sowie PNG-Menügrafiken | Hier erzeugte gemeinsame KI-Atlanten und Szenen; Schlossgeister werden im Godot-Code gezeichnet | Auch die neun weiteren aktuellen PNG-Ressourcen sind exakt auf `image_gen`-Ausgaben zurückgeführt, gegebenenfalls über die dokumentierten Originalhashes vor der Größenoptimierung. | Keine heruntergeladenen NPC-Texturen festgestellt; aktuelle Hashes geprüft. |
| Superseded Mina/Leo/Sam/Jule images | Original PNG bytes contain C2PA creation claims naming ChatGPT / gpt-image on 20 October 2026; signatures remain cryptographically unverified | Original Git bytes match the previously recorded hashes and retained outputs. The owner-review ledger records creation, introduction and removal on the same day; see the chronology below. | Remain excluded from current runtime and Android packages. Generation claims do not establish reference rights or legal clearance. |

Insgesamt sind **24 aktuelle PNG-Quellen** erfasst: zwölf private Familienbilder, ein neutraler Atlas und elf gemeinsame PNG-Ressourcen einschließlich Eichhörnchen, Objekten, Szenen und UI.

Maschinenlesbare Herkunft: `art/character-origins.json`. `scripts/qa/character_origins.py` prüft die tatsächlichen aktuellen Bildhashes und den materialisierten Figurenbestand. Android-Exporte führen diese Prüfung vor dem Export aus. Ungeprüfte Austauschdateien oder umbenannte fremde aktive PNGs führen zu einem Fehler. Die Android-Prüfung sperrt weiterhin die vier alten Bildnamen und kontrolliert die gewählte Figurenvariante.

Diese Prüfung unterscheidet **eigene Fantasiegestaltung ohne Bildreferenz** von **neu generierter Familienillustration mit Nutzerreferenz**. „KI-generiert“ bedeutet nicht automatisch „urheberrechtsfrei“. Die nachgewiesene Herkunft ersetzt keine weltweite juristische Freigabe oder Prüfung auf jede denkbare Ähnlichkeit. Vorhandene alte Git-Commits werden durch diese Änderung nicht gelöscht oder umgeschrieben.

## Legacy creation claims: correction of the old description

The existing [owner-review/C2PA ledger](../scripts/qa/visual-ip-owner-review.json)
and [provenance registry](../art/character-origins.json) describe the **original
Git bytes**, not replacements generated during this documentation change.

| Historical source | Original embedded creation timestamp (UTC data) | Europe/Berlin display, 20 October 2026 |
|---|---|---|
| `historical/3909c4c/legacy-1` (Mina) | `2026-10-20T18:12:20.030352106Z` | 20:12:20 CEST |
| `historical/3909c4c/legacy-2` (Leo) | `2026-10-20T18:11:35.473495925Z` | 20:11:35 CEST |
| `historical/3909c4c/legacy-3` (Sam) | `2026-10-20T18:13:15.056545082Z` | 20:13:15 CEST |
| `historical/3909c4c/legacy-4` (Jule) | `2026-10-20T18:13:57.074856783Z` | 20:13:57 CEST |

The manifests name claim generator **OpenAI Media Service API** and creation
software **ChatGPT / gpt-image**, with `trainedAlgorithmicMedia`. These are read
metadata claims. **C2PA signatures, certificate trust and timestamps have not
been cryptographically verified**; they do not by themselves prove the route
of acquisition, reference rights or redistribution permission.

Introduction commit `3909c4cf4e055483b746fcbd89b640b2c97e109e` records
20:34:22 CEST on that same day; removal commit
`daa0df88d472ceae9be91bc1ff50857b2ba9170a` records 22:29:08 CEST. The ledger
already matched each original Git blob to its recorded hash. “Legacy” means the
superseded cast, not images older than October 2026. The old missing-provenance
description was stale. No new image generation, image replacement, extra image
search, history rewrite or legal clearance follows from this correction.

## Neues App-Icon in 0.9.1

Das vorherige Icon wird auf ausdrücklichen Nutzerwunsch durch eine neue, hier ohne Bildreferenz erzeugte Illustration ersetzt: türkisfarbenes Weltraum-Eichhörnchen mit kupferfarbigem Schwanz, violettem Schal, Buch und Stern. Das unveränderte originale `image_gen`-Ergebnis und der Generierungsauftrag liegen unter `art/public/app-icon/`; die App verwendet die auf 512×512 verkleinerte PNG-Datei. Original- und Laufzeitdatei sind separat per SHA256 dokumentiert. Es wurden keine vorhandenen Film-/Spielfiguren oder Fotos als Vorlage übergeben. Das ist ein Herkunftsnachweis, keine pauschale juristische Freigabe.

Die Android-Prüfung vergleicht die mitgepackte PNG-Datei bytegenau und decodiert außerdem das tatsächliche Launcher-Icon, den adaptiven Vordergrund sowie das Startbild aus APK und AAB. Ein Pixelvergleich mit dokumentierter Toleranz für Skalierung/Rekompression verhindert, dass ein altes Android-Ressourcenbild unbemerkt erhalten bleibt.
