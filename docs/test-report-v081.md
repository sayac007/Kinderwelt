# Tatsächliche Prüfungen und Android-Artefakte – 0.8.1

Stand: 22. Oktober 2026. [Vorheriger Stand 0.8.0](test-report-v080.md). [Getrenntes privates Figurenrepository](family-repository.md), [Figurenherkunft](character-origins.md), [offener Stimmwunsch](voice-v081.md).

## Fertig lokal, extern noch offen

**Zwei tatsächlich gebaute APKs mit den gewünschten Dateinamen**, zwei unsignierte AABs und eine geprüfte gemeinsame Auslieferungsstruktur liegen vor. Der Benutzer hat die Familiengrafiken inzwischen in `sayac007/Kinderwelt-Privat` hochgeladen. Authentifizierter Zugriff bestätigt das Repository als privat; der neue entfernte Commit und sämtliche 14 zugelassenen Dateien wurden geprüft und in die Build-Konfiguration übernommen. Die früheren 401-/Forbidden-Befunde dokumentieren die vorherige Blockade. Vorhandensein und Funktion des Actions-Lesetokens sowie ein erfolgreicher GitHub-Actions-Lauf bleiben offen.

**Die englische Stimme wurde noch nicht für Deutsch/Russisch übernommen.** Ein realer Versuch mit demselben englischen Modell und deutscher/russischer Lautung wurde wegen schlechter Verständlichkeit verworfen. Modellgewichte für eine echte sprachübergreifende Stimmklangübertragung waren nicht abrufbar. Alle ausgelieferten Sprachaufnahmen und ihre Manifeste bleiben bytegleich zu 0.8.0. Ein gespeicherter Netzwerkentwurf hebt die aktuelle Sperre nicht von selbst auf.

## Tatsächlich ausgeführt und bestanden

- Vollständige Suite in Familien- und isolierter neutraler Variante: jeweils **6.085 Godot-Spielprüfungen**, **3.608 Weltprüfungen**, **130 Audiobusprüfungen** (30 + 66 + 34), frischer Import/60-Frame-Start und **74 Python-Tests**.
- Die finalen 74 Python-Tests wurden nach den letzten Import-/Auslieferungsprüfungen in beiden Varianten erneut vollständig bestanden. Nach Ergänzung der Herkunftsnachweise für NPC-, Kulissen- und UI-Grafiken wurden zusätzlich die drei Herkunftstests je Variante erneut bestanden. Diese Ergänzung verändert keine App-Grafik oder Sprachdatei.
- Sämtliche **1.645 verschiedenen Sprachdateien** und **20 Musikstücke** vollständig mit FFmpeg decodiert; Hash, Dauer, Pegel und stille Ränder geprüft. Bestehende Aufgaben-JSON, Musikmanifest und Sprachmanifeste sind bytegleich zu 0.8.0.
- Getrennter echter privater Git-Bestand aus dem festgelegten lokalen Commit geklont und ausschließlich 14 zugelassene, hashgeprüfte Dateien in einen frischen Hauptcode-Schnappschuss importiert. Die daraus berechneten App-Input-Hashes stimmen für **beide Varianten exakt** mit den tatsächlich gebauten Android-Artefakten überein. Die Android-Builds selbst liefen aus dem sauberen Hauptcode-Commit, nicht in GitHub Actions.
- Importtests weisen veränderte Bilder/Manifeste, Originalfoto-Zusätze, Symlinks und veraltete Kostümhashes zurück. Auslieferungstests verhindern manipulierte Dateien, doppelte große APKs, eine falsche Figurenvariante unter dem Familiennamen und eine halb veröffentlichte APK/AAB-Paarung.
- **24 aktuelle PNG-Quellen** sind auf hier erzeugte KI-Ausgaben zurückgeführt; zwölf private Dateien, ein neutraler Atlas und elf gemeinsame Dateien inklusive NPC-/Objektatlanten, Szenen und UI. Aktuelle Bildhashes werden geprüft. Die vier älteren Figurenbilder bleiben gesperrt; kein aktuell verwendetes heruntergeladenes Figurenbild festgestellt. Das ist eine Herkunftsprüfung, keine juristische Freigabe.
- `actionlint 1.7.7` prüfte die endgültigen GitHub-Workflows fehlerfrei. Private Quellen/Token werden ausschließlich für vertrauenswürdige Push-/Dispatch-Läufe verwendet; Pull Requests bauen neutral ohne Zugriff auf das Figurenrepository.

Protokolle und maschinenlesbare Berichte: `docs/qa/v081-*`. Es wurden **keine neuen 383 visuellen Renderings** für 0.8.1 ausgeführt: Figuren, Looks, Aufgaben, sieben Welten, Bewegung, UI-Layout und Sprachdateien wurden unverändert übernommen. Die Einstellungen zeigen 0.8.1; deren Spiel-/Layoutprüfungen sind in der aktuellen Suite enthalten. Die vorherigen echten Renderings bleiben unter `v080-*` nachgewiesen.

## Tatsächlich erzeugte Dateien

Alle folgenden Dateien liegen unter `build/android-v081-delivery/`:

| Datei | Bytes | MB dezimal |
|---|---:|---:|
| `kinderwelt-debug-family.apk` | 185,906,144 | 185.906 |
| `kinderwelt-unsigned-family.aab` | 174,523,181 | 174.523 |
| `kinderwelt-debug-neutral.apk` | 181,035,217 | 181.035 |
| `kinderwelt-unsigned-neutral.aab` | 169,659,794 | 169.660 |

`delivery.json` verbindet die endgültigen Dateinamen mit Paket, Variante, Version, Hash und tatsächlichem App-Input. Große APK-/AAB-Dateien stehen jeweils nur einmal im Ausgabeverzeichnis; die Unterverzeichnisse enthalten nur Nachweise. Der Workflow lädt dieses Verzeichnis als `android-development-artifacts` hoch, sobald die GitHub-Voraussetzungen eingerichtet sind. **Ein solcher Remote-Lauf wurde hier noch nicht ausgeführt oder bestätigt.**

Beide Varianten bestanden den vollständigen Android-Export und die technischen Prüfungen: Version **0.8.1 / Code 12**, Paket/Variante, ZIP-/APK-/Bundle-Format, deklarierte Daten und sämtliche Sprach-/Musik-/Grafikressourcen, API **24–36**, keine Android-Berechtigungen, Backup aus, Drehung `fullUser`, `arm64-v8a` und `x86_64`, 16-KB-ELF- und APK-ZIP-Ausrichtung. APK-v2-Signaturen geprüft; AABs mit Bundletool validiert und unsignierter Zustand bestätigt.

Die APKs tragen temporäre Entwicklungssignaturen, **keine Release-Signaturen**. Beide AABs sind **unsigniert**. Pakete: `org.example.kinderwelt.preview.family.v081` und `org.example.kinderwelt.preview.neutral.v081`. Sie können nebeneinander installiert werden und haben getrennte lokale Spielstände; ältere Testpakete werden nicht ersetzt. Hier wurde keine APK auf einem echten Android-Gerät installiert.

### Quellen und Hashes

Die Builds liefen aus sauberem Git-Quellcommit `4b7ac09` ohne beobachtete Statusänderung während des jeweiligen Builds. Nachfolgende Änderungen ergänzen Nachweise und Herkunftsmetadaten; sie ändern keine App-Datei. Die private Figurenquelle ist in `scripts/ci/family-assets.json` mit vollständigem tatsächlichem Git-Commit und Manifest-SHA festgelegt. Das benannte entfernte Repository ist inzwischen als privat bestätigt; sein manuell hochgeladener Commit und die Grafikdateien sind geprüft. Die GitHub-CI bleibt unbestätigt.

| Datei | SHA256 |
|---|---|
| `kinderwelt-debug-family.apk` | `aa784ea3f4bb994f0e075dc5f82d342fbcba912a8198d301dc91bd72516de4f3` |
| `kinderwelt-unsigned-family.aab` | `19c477247541e79528ba8778e43036b77d6b926ac56a62df2915a62cd82032fd` |
| `kinderwelt-debug-neutral.apk` | `cdf98a357c401ddafcf17fbb55a7261cdb95cb94c670961ec861d272b14ac78b` |
| `kinderwelt-unsigned-neutral.aab` | `4054ea9b37fe04af37a13d2562cd1ba11cb565b053c2fea29956ff313840bae8` |

### Tatsächliche Größenänderung gegenüber 0.8.0

| APK | 0.8.0 Bytes | 0.8.1 Bytes | Differenz |
|---|---:|---:|---:|
| family | 185,906,124 | 185,906,144 | +20 |
| neutral | 181,035,213 | 181,035,217 | +4 |

Archivgröße, nicht installierter Speicher oder Play-Download. Die separaten Quellrepositorys und Prüfnachweise werden nicht als zusätzliche Bildpakete in beide APKs gepackt.

## Offene Stimme und Zugangs-/Netzwerkeinstellungen

Der direkte englische Modellversuch erzeugte je sieben echte DE-/RU-WAV-Dateien. Unabhängiges Whisper-small-Screening ohne Referenzvorgabe: **DE 45,02 %**, **RU 62,91 %** Zeichenabweichung. Keine menschliche Hörfreigabe; der Versuch ist ausdrücklich verworfen. OpenVoice-V2-Dokumentation war erreichbar, benötigte Gewichte von Hugging Face/offiziellem S3 jedoch nicht. **Keine OpenVoice-Konvertierung ausgeführt.** [Details](voice-v081.md).

Die vorhandene Cloud-Konfiguration enthielt eine eingeschränkte Paketquellen-Freigabe. Eine additive Erweiterung wurde erfolgreich als Entwurf gespeichert: bestehende Android-/Google-Ziele erhalten, zusätzlich `api.github.com`, `huggingface.co`, `cdn-lfs.huggingface.co`, `cdn-lfs.hf.co`, `cas-bridge.xethub.hf.co` und der offizielle Modellbucket `myshell-public-repo-host.s3.amazonaws.com`. **Der Entwurf ist nicht automatisch aktiv**: Umgebungseinstellungen prüfen und speichern, anschließend die Umgebung veröffentlichen. Danach müssen die betroffenen Operationen erneut geprüft werden; erfolgreiche Speicherung ist keine bestätigte Verbindung oder Veröffentlichung.

Zusätzlich muss GitHub-Authentifizierung über die Plattform wieder funktionieren. Es wurden native Git-Zugriffe und die vorhandene Bindung geprüft, keine Zugangsdaten ausgegeben oder extrahiert. Fehlgeschlagene Git-Anmeldungen beweisen nicht, dass ein Proxy-Platzhalter ein abgelaufener Roh-Token wäre. Für Actions ist nach Einrichtung des privaten Repositorys ein gesonderter, eng begrenzter Lesetoken als `KINDERWELT_FAMILY_ASSETS_TOKEN` erforderlich; sein Vorhandensein/ seine Funktion wurde noch nicht bestätigt. Kein Token gehört in den Chat oder Git.

## Manuell weiterhin offen

Android-Installation beider Varianten, tatsächliche Lautsprecher-/Bluetooth-Verständlichkeit mit und ohne Musik, Audiofokus/Unterbrechung, Drehung, Wiedereinstieg und reale Bildrate. Muttersprachliche Hörprüfung und freiwillige Kinderbeobachtung bleiben offen. Die separate Figurenablage entfernt keine älteren Familienbilder aus der bestehenden Hauptrepository-Historie. Endgültige App-ID, dauerhafte Signierung, Datenschutz/Families, Altersfreigabe, Store-Eintrag und Play-Freigaben bleiben offen. Keine empirische Lernwirkung oder Google-Play-Uploadbereitschaft behauptet.

## Nachtrag: vorhandenes Figurenrepository verwenden

Konfiguration und Einrichtungsanleitung verweisen jetzt auf `sayac007/Kinderwelt-Privat`; Commit und Manifest-Hash der vorbereiteten Familienbilder sind unverändert. Der lokale Figurenbestand hat dieses Repository als `origin`. Der tatsächliche CI-Quellreproduktionsnachweis unter `v081-ci-reproduction.json` enthält bewusst den damals verwendeten alten Zielnamen; dieser historische Nachweis wird nicht rückwirkend umgeschrieben. Der neue Zielname verändert keine App-Dateien oder gebauten APKs. Vor dem ersten Upload muss die Sichtbarkeit privat und der GitHub-Zugriff funktionsfähig sein.

Für diese reine Zielumstellung wurden alle **74 Python-Tests** erneut bestanden, `actionlint 1.7.7` lief fehlerfrei, und der tatsächliche lokale Import der 14 Dateien wurde gegen den unveränderten Commit/Manifest-Hash erneut erfolgreich ausgeführt. Protokolle: `docs/qa/v081-family-repository-target*`. Keine erneuten Android-Builds oder Godot-Läufe für diese Konfigurations-/Dokumentationsänderung.

## Nachtrag: manueller Upload und wiederhergestellter Repository-Zugriff

GitHub bestätigt das private Figurenrepository und Repository-Lese-/Schreibrechte. Der manuelle Upload-Commit `5a35f7675eb1a0881447005fbe51dc089ef8471f` wurde abgerufen und als Quelle eingetragen. Alle 14 tatsächlich entfernten Familiengrafik-/Katalogdateien stimmen mit dem bisherigen Manifest überein und bestehen den unveränderten Importer. Die oben beschriebenen früheren 401-/Öffentlichkeitsbefunde sind historisch. App-Inhalte und bestehende Android-Artefakte bleiben unverändert. Actions-Secrets können von der vorhandenen Integration nicht gelesen werden (HTTP 403 `Resource not accessible by integration`); Vorhandensein und Funktion des separaten CI-Lesetokens sowie ein erfolgreicher Remote-CI-Lauf sind weiterhin nicht bestätigt.

Nach Übernahme des echten Upload-Commits bestanden erneut alle **74 Python-Tests**, einschließlich Decodierung aller 1.645 Sprachdateien, sowie `actionlint 1.7.7`. Protokoll: `docs/qa/v081-family-upload-pin-tests.log`. Keine App-Datei geändert; keine erneuten Android-Builds oder Godot-Läufe für die reine Commit-Pin-/Dokumentationsänderung.
