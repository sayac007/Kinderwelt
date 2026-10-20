## Ergebnis

Kinderwelt hatte noch keine Android-Exportkonfiguration. Diese Änderung ergänzt eine prüfsummengepinnte Linux-Toolchain, isolierte Gradle-Builds für Debug-APK und unsigniertes AAB sowie strikte Paketprüfungen und einen GitHub-Actions-Workflow. Alle 36 Spielaufgaben bleiben unverändert.

Zwei saubere Builds desselben Codecommits wurden lokal ausgeführt; APK und AAB liegen unter `/workspace/Kinderwelt/build/android/`, Wiederholungsartefakte unter `/tmp/kinderwelt-05-repro-artifacts/`. Dateigrößen, SHA256, Herkunft und tatsächliche Prüfungen sind in `docs/release-report.md` und `docs/android-build-evidence.json` festgehalten. Binärdateien und private Schlüssel werden nicht eingecheckt.

## Validierung

- Vollständiger QA-Einstieg PASS: 1236 bestehende Prüfungen, 16 Python-Prüferregressionen, GUT-Qualität 6 Tests / 13433 Assertions, 144 Aufgaben-/Viewport-Kombinationen sowie die GUT-Upstream-Auswahl 13 Tests / 62 Assertions.
- 10 neue Android-Verifikationsregressionen PASS.
- APK: apksigner v2, ZIP/ELF-16-KB-Ausrichtung, Manifest/Paket/Version/API, leere Berechtigungsliste, Backup aus und alle fünf Moduldateien PASS.
- AAB: bundletool validate/Manifest, ELF-Ausrichtung und unsigned-Status PASS. Keine Entwicklungs-/Studien-/Schlüsseldateien im App-Paket.
- Installer zweimal erfolgreich; eigener sauberer Git-Clone bestätigt den identischen App-Quelldigest und bestandene Paketprüfungen. Keine Behauptung byteidentischer/hermetischer Builds.

## Freigabegrenzen

**Google Play upload BLOCKED.** Kein Release-Schlüssel bereitgestellt, kein signiertes Release-AAB erzeugt, kein Upload. Die Paketkennung `org.example.kinderwelt` ist ein Platzhalter. Aktuelle Target-API-/Families-/Datenschutz-/Altersfreigabe-/Store-Regeln müssen offiziell geprüft werden; die abgefragten Google-Policy-Seiten lieferten in dieser Umgebung HTTP 403. Gerätelauf, AAB-Splitinstallation, Rotation, Barrierefreiheit und Performance sind offen.

Store-/Datenschutzentwürfe, Original-Icon, echte Desktop-Spielansichten als ausdrücklich markierte Vorschauen und sichere optionale Signaturanleitung sind vorbereitet. Betreiberangaben, Geräteaufnahmen, Feature Graphic, Console-Erklärungen und separate Upload-Freigabe fehlen. GitHub-Actions-Ausführung ist konfiguriert, aber nicht als erfolgreich bestätigt. Keine Aussage über nachgewiesene Lernwirkung oder Marktreife.
