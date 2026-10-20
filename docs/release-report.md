# Android release report — 05

Stand: 2026-10-20. **Google Play upload: BLOCKED.** APK und unsigniertes AAB
wurden lokal tatsächlich erzeugt und technisch geprüft. Keine Veröffentlichung,
Release-Signatur, Geräteinstallation oder Store-Freigabe wird behauptet.

Grundlage: vollständig gelesener Upload `05_android_release.yaml` (2484 Bytes).
Branch `feat/android-release` startet von `origin/main` `bfc3108`, dem Merge von
PR #4. Geprüfter Codecommit: `62c56a5702175c42b9a479c80a99b65f60c36c3e`; Build und vollständiger
QA-Lauf erfolgten bei sauberem Arbeitsbaum. Spätere Berichtsänderungen betreffen
nur Dokumentation. Bestehende Module, 36 Aufgaben und tests/run.sh sind gegenüber
main unverändert. Nur Aufgabe 05 wurde implementiert; YAML-Dateien wurden nicht
verändert. Maschinenlesbare Kurzbelege: [android-build-evidence.json](android-build-evidence.json).

## Tatsächliche Artefakte

| Datei relativ zum Repository | Größe | Signatur | Ergebnis |
|---|---:|---|---|
| `build/android/kinderwelt-debug.apk` | 162,757,298 Bytes | Godot-Entwicklungszertifikat, APK v2 verifiziert | PASS, Geräteinstallation offen |
| `build/android/kinderwelt-unsigned.aab` | 52,392,097 Bytes | ausdrücklich UNSIGNIERT | Bundletool-Struktur/Manifest PASS, nicht hochladen |
| `build/android/kinderwelt-release.aab` | nicht erzeugt | kein Release-Schlüssel bereitgestellt | BLOCKED |

SHA256:

```text
12bb92bc2e33bb479622db959385a43a0b2c3d7ea5220ae0b6ad42221e6db03a  kinderwelt-debug.apk
bfc5d044db77a9eb87a0d15dd3fa8c1ef956aca317968cb3d15a7d353b074ec4  kinderwelt-unsigned.aab
```

Absoluter Build-Pfad dieser Sitzung: `/workspace/Kinderwelt/build/android/`.
Dort liegen auch provenance.json, verification.json, vollständige Import-/Export-
Logs, APK-Manifest/Signatur und Bundletool-/jarsigner-Ausgaben. Binärdateien und
lokale Schlüssel werden nicht in Git eingecheckt. GitHub Actions ist für Upload
von APK/AAB und technischen Belegen mit sieben Tagen Aufbewahrung konfiguriert;
eine erfolgreiche Ausführung auf GitHub wurde hier nicht bestätigt.

## Ausgeführte Prüfungen

- Gepinnter Installer einschließlich erneutem Aufruf: PASS. SDK-Archive gegen
  offizielle Repository-Prüfsummen und danach SHA256-Pins geprüft, Godot-Vorlagen
  SHA512, Temurin-JDK SHA256. Java 17.0.16+8 und aapt2 tatsächlich gestartet.
- Frischer isolierter Godot-Import und Gradle-Export beider Formate: PASS.
- ZIP-Integrität, sichere/eindeutige Archiveinträge, Manifest und App-Inhalte: PASS.
  Alle fünf Moduldateien vorhanden, jeweils 68 App-Asset-Dateien geprüft;
  GUT, Tests, Skripte, Studienvorlagen, Dokumentation und Schlüsseldateien fehlen.
- Paket `org.example.kinderwelt` (Platzhalter), Version `0.1.0`, Code `1`,
  minSdk `24`, targetSdk `36`, arm64-v8a + x86_64: PASS gegen Konfiguration.
  Keine angeforderten Android-Berechtigungen; Backup aus. `fullUser` (Manifest-Wert 13)
  erlaubt Hoch-/Querformat unter Beachtung der Rotationssperre. Dies ist ein
  Manifestbefund, kein Rotationstest auf Hardware. Renderer ausdrücklich
  `gl_compatibility`, nicht der implizite mobile Vulkan-Standard.
- APK apksigner verify v2, zipalign mit 16-KB-Seitenausrichtung: PASS.
  Alle nativen ELF-Ladesegmente beider Artefakte auf mindestens 16 KB geprüft.
  Das ersetzt keinen Lauf auf einem Gerät mit 16-KB-Seiten.
- AAB bundletool 1.18.2 validate + Manifest-Dump: PASS.
  jarsigner meldet `jar is unsigned`; keine AAB-Signatureinträge vorhanden.
- Neue Android-Prüferregression: **10 Tests PASS**, einschließlich Ablehnung von
  Berechtigungen, Identitäts-/Versions-/SDK-/Backup-/Orientierungsabweichungen,
  Debug-Release, falschem Alias, fehlenden Modulen, Dev-/Schlüsseldateien und
  nicht geeigneter ELF-Ausrichtung.
- Vollständiger QA-Einstieg: **PASS**, Belege `/tmp/kinderwelt-05-quality-final/`.
  Bestehende Smoke 33, Learning 559, Input 59, Szenarien 585 = **1236 Prüfungen**,
  keine Fehler. Statischer Prüfer **16 Tests PASS**, Quellscan ohne Befund.
  GUT-Qualität **6 Tests / 13.433 Assertions PASS**, alle **144** Kombinationen
  aus 36 Aufgaben und vier Viewports. Gepinnte GUT-Upstream-Auswahl
  **13 Tests / 62 Assertions PASS**. Frischer Import und Start ebenfalls PASS.

Der erste vollständige QA-Versuch bestand alle Tests, wurde aber korrekt als
FAIL gewertet, weil der erstmalige Import des neuen Icons die Quelldateiliste
während des Laufs änderte. Die Import-Metadaten sind nun eingecheckt; der oben
aufgeführte saubere Wiederholungslauf bestand auch die Quellenstabilitätsprüfung.
Vorherige Buildversuche fanden eine Proxykonfiguration für Java, das
schreibgeschützte Home-Verzeichnis und die mobile Renderer-Voreinstellung als
Probleme. Unterstützte Proxy-/CA-Konfiguration und temporäre Java-/Android-
Verzeichnisse beheben den Build. TLS und Prüfsummen wurden nicht abgeschaltet.
Der direkte APK-Exporter erzeugte eine Ressourcenwarnung zum themed icon;
daher verwenden jetzt beide Formate Gradle. Die tatsächlichen finalen Paketlogs
enthalten keine Godot-Fehler. Ein früherer ADB-Aufruf scheiterte am Cloud-Home;
ADB-/Geräteinstallation ist deshalb nicht als bestanden verzeichnet.

## Wiederholbarkeit

Ein zweiter Build aus einer separaten sauberen lokalen Git-Kopie desselben
Codecommits bestand ebenfalls beide Exporte und sämtliche Paketprüfungen.
Befehl nach `git clone --no-hardlinks --single-branch --branch feat/android-release
/workspace/Kinderwelt /tmp/kinderwelt-05-repro-repo`:

```bash
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64   python3 /tmp/kinderwelt-05-repro-repo/scripts/android/build.py   --tools /workspace/tools --output /tmp/kinderwelt-05-repro-artifacts
```

App-Quelldigest beider Läufe:
`b2ed8cd41a97032adbcf4323767e9c4b5018e29ea661336c0dd0d87f9301c5ef`.
Der zweite Lauf verwendete dieselbe geprüfte Toolchain und den bestehenden
Gradle-Abhängigkeitscache, keinen neuen Offline-/Hermetiknachweis. Ergebnisdateien
und eigene SHA256-Werte stehen unter `/tmp/kinderwelt-05-repro-artifacts/` und im
maschinellen Kurzbeleg. Bytegleichheit wird nicht behauptet: Exportzeitstempel,
Gradle-Metadaten und wegwerfbare APK-Zertifikate ändern sich. Die Projektquelle
ist gleich, Paketkonfiguration und Prüfergebnisse stimmen überein.

## Offene Freigaben und Grenzen

1. Dauerhafte Paketkennung, Versionierung, Eigentümer-/Namensrechte festlegen.
2. Realen Upload-Schlüssel sicher bereitstellen, Play App Signing entscheiden,
   signiertes AAB erzeugen und Zertifikat/Fingerprint unabhängig bestätigen.
   [Sicherer Ablauf](android-build.md) vorbereitet, nicht ausgeführt.
3. **Aktuelle** Target-API-, Families-, Zielgruppen-, Altersfreigabe-, Data-Safety-
   und Store-Regeln zum Veröffentlichungszeitpunkt offiziell prüfen. Die beiden
   abgefragten offiziellen Target-API-Seiten lieferten hier HTTP 403. API 36
   ist ein technischer Pin und belegt keine aktuelle Play-Konformität. Der
   offizielle Godot-Gradle-Stand nutzt AGP 8.6.1 mit Warnung zum noch nicht getesteten
   compileSdk 36; Toolchain-Update und reale Gerätekompatibilität vor Release prüfen.
4. Datenschutzentwurf fachlich prüfen, Verantwortlichen/Kontakt und reale
   öffentliche Richtlinien-URL ergänzen; Console-Fragebögen wahrheitsgemäß ausfüllen.
5. Store-Texte und Original-Icon prüfen. Fünf tatsächliche Desktop-Spielansichten
   liegen ausdrücklich als Vorschau vor. Release-Geräteaufnahmen, Feature Graphic
   und sonstige aktuell erforderliche Assets sowie Betreiberangaben bleiben offen.
6. Physische Geräte, AAB-Splitinstallation, offline Start, Touch, Audio, Back,
   Hoch-/Querformat, Safe Areas, Resume, lokaler Speicher, Updates, Barrierefreiheit
   und Performance nach [Geräteprotokoll](google-play-release-checklist.md) prüfen.
   Kein Kindertest, keine Leistungsdaten und kein empirischer Lernwirkungsnachweis.
7. Developer-Account-/Testtrack-Anforderungen und gesonderte Upload-Freigabe fehlen.
   Es erfolgte kein Play-Console-Zugriff und kein Upload.

Cloud-Konfiguration: install_script und start_skill wurden als Entwurf gespeichert,
einschließlich Android-Kommandos und ohne Signaturgeheimnisse. Die zusätzlichen
Domains developer.android.com/support.google.com sind für spätere offizielle
Prüfungen vorgemerkt. Der Entwurf ist nicht automatisch aktiv oder veröffentlicht;
die Umgebungseinstellungen müssen zum dauerhaften Übernehmen gespeichert und die
Umgebung veröffentlicht werden. Wiederherstellung in einer neuen Sitzung ist
nicht geprüft.
