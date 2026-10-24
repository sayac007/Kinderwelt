# Android bauen

Die Komponenten und Prüfsummen stehen in `scripts/android/toolchain.json`: Godot 4.7.2, Temurin 17.0.16+8, Android API 36, Build Tools 36.1.0, Gradle 8.11.1 und Bundletool 1.18.2.

```sh
python3 scripts/android/install.py --root /workspace/tools --accept-android-sdk-license
# Privater Standardbuild setzt den lokalen privaten Grafikpack voraus:
python3 scripts/android/build.py --tools /workspace/tools --output build/android-current
# Getrennte lokale Test-App je Variante:
python3 scripts/android/build.py --tools /workspace/tools --variant family --preview --output build/android-v091-family
python3 scripts/android/build.py --tools /workspace/tools --variant public --preview --output build/android-v091-public
# Beide Varianten mit den gewünschten Dateinamen, wenn Familienquellen importiert sind:
python3 scripts/android/build_variants.py --tools /workspace/tools --output build/android-delivery-neu
# Ohne Familienquellen ausschließlich neutral:
python3 scripts/android/build_variants.py --variants neutral --tools /workspace/tools --output build/android-neutral-neu
# Optionaler expliziter Bezeichner für einen kontrollierten Testbuild:
python3 scripts/android/build.py --tools /workspace/tools --variant public --package-id de.kinderwelt.test --output build/android-override
```

Die Lizenzoption setzt voraus, dass der Betreiber die Android-SDK-Lizenz akzeptiert. Jedes Ausgabeverzeichnis muss neu sein. Das Skript baut aus einer isolierten Kopie ausschließlich der App-Verzeichnisse; die Varianten-Grafiken werden dort eingesetzt. Beide SDK-Umgebungsvariablen zeigen auf denselben geprüften SDK. Fehlerblöcke aus Godot und Gradle erscheinen direkt im Protokoll; vollständige Logs bleiben im Ausgabeverzeichnis.

## Konfigurierbare, vorläufige Identität

Version **0.9.3 / 16**. `scripts/android/app-config.json` hält ausdrücklich die vorläufige Testkennung `org.example.kinderwelt`. Eine endgültige Paketkennung ist noch nicht entschieden. `--package-id` überschreibt nur den aktuellen Build; `export_presets.cfg` enthält `@KINDERWELT_PACKAGE_ID@`, das der Builder ersetzt. Android-Exporte deshalb über das Skript ausführen. Ungültige Bezeichner und Java-Schlüsselwörter werden vor dem Export abgelehnt; die Prüfung vergleicht anschließend die explizit erwartete Identität.

| Build | Paket bei Standardkonfiguration | Launchername |
|---|---|---|
| Standard, gewählte Variante | `org.example.kinderwelt` | Kinderwelt |
| Private Vorschau | `org.example.kinderwelt.preview.family.v090` | Kinderwelt 0.9.3 Privat Test |
| Öffentliche Vorschau | `org.example.kinderwelt.preview.neutral.v090` | Kinderwelt 0.9.3 Public Test |

Der Testkanal `preview_channel=v090` ist unabhängig von der Versionsnummer, damit spätere Builds mit demselben Zertifikat als Update installierbar bleiben. Die alten 0.8.1-Schlüssel waren flüchtig und sind nicht wiederherstellbar. 0.9.0 wird deshalb parallel installiert; alte Punkte werden nicht automatisch zwischen Paketen übertragen. Für die vollständig gelöste erste Runde gibt es im Elternbereich eine ausdrückliche manuelle Bestätigung zur einmaligen Übernahme der 3200 früher verdienten Punkte. Die alte App nicht deinstallieren, wenn ihre Daten gebraucht werden.

Vorschauen haben eigene lokale Spielstände und können nebeneinander sowie neben früheren Versionen installiert werden. Die stabile Figuren-/Lösungslogik ist identisch; Daten werden nicht zwischen getrennten Android-Paketen kopiert.

## Artefakte und Prüfungen

Die aktuellen tatsächlich gebauten Varianten, Quellcommits und Prüfungen stehen im [Qualitätsüberblick](QUALITY_ASSURANCE.md). Ein früherer Build-Stopp für den damaligen Sprach-/Icon-Quellstand ist historisch; der aktuelle Auftrag umfasst überprüfbare Testpakete.

Jeder Build liefert `kinderwelt-debug.apk`, ein **unsigniertes** `kinderwelt-unsigned.aab`, Prüfberichte, Quellprovenienz, Größenanalyse und Logs. Die APK wird mit einem ausschließlich für Entwicklung vorgesehenen Godot-Schlüssel außerhalb des Repositorys signiert (`tools/preview-signing/debug.keystore`, alternativ `KINDERWELT_DEBUG_KEYSTORE`). Wiederholte lokale Builds verwenden denselben Schlüssel; die Prüfung vergleicht den SHA-256-Fingerabdruck des Zertifikats mit der APK. Vertrauenswürdige CI-Läufe verwenden einen privaten Actions-Cache; PR-Builds einen isolierten Schlüssel. Cache-Verlust oder ein anderer Branch mit eigenem Cache kann eine neue Entwicklungsidentität erzeugen. Für dauerhafte Testupdates muss der Entwicklungsschlüssel gesichert und derselbe Kanal verwendet werden; dies ist keine Release-Signierung. Keine privaten Schlüssel werden eingecheckt. Vorhandene Installationen nicht unbedacht deinstallieren, wenn ihre lokalen Daten erhalten bleiben sollen.

Prüfungen: Paket, Version, API 24–36, keine Berechtigungen, deaktiviertes Backup, Bildschirmrotation, alle acht Fächer, drei Sprachmanifeste und sämtliche tatsächlich spielbaren Sprach-/Musik-/Grafikressourcen, ausgewählte Figurenvariante, zwei ABIs, 16-KB-ELF-Ausrichtung, ZIP-Ausrichtung, APK-Signatur und unsignierter Bundle-Status. Native Bibliotheken sind verlustfrei komprimiert und werden bei Installation entpackt. Neue Buildgrößen und tatsächlich erzeugte Dateien: [Testbericht](test-report.md).

## GitHub Actions

Für vertrauenswürdige Pushes und manuelle Läufe erzeugt der Workflow nach Einrichtung des getrennten privaten Figurenrepositorys beide Varianten. Die Quellbilder werden aus einem festgelegten Commit mit einem gesonderten Lesetoken importiert; Pull Requests erhalten diesen Zugang nicht und bauen nur neutral. [Einrichtung des privaten Figurenrepositorys](family-repository.md). [Android verification builds](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml) öffnen, passenden Branch/Lauf auswählen und unter **Artifacts** `android-development-artifacts` herunterladen. GitHub-Anmeldung ist erforderlich. ZIP entpacken: `kinderwelt-debug-family.apk` und `kinderwelt-debug-neutral.apk` liegen direkt darin, außerdem zwei unsignierte AABs und Prüfberichte. Die Pakete sind getrennte Vorschau-Installationen. Den tatsächlich ausgeführten Lauf und die geprüfte Version dem aktuellen Testbericht entnehmen.

Artefakte werden sieben Tage aufbewahrt und entstehen erst nach erfolgreichem Export/Upload. Ein Push oder lokal bestandener Build beweist keinen erfolgreichen Remote-Lauf. Geräteprüfungen sind separat erforderlich.

## Google Play bleibt offen

[Vorbereitete Play-Entscheidungen und Datenschutz-/Store-Entwürfe](PLAY_READINESS.md). Es gibt keine Release-Signatur und keine Upload-Freigabe. Offen sind endgültige App-ID, dauerhafter Signierschlüssel mit sicherem Schlüsselspeicher/Play App Signing, Datenschutztext, Data-Safety-Angaben, Kinder-Zielgruppe und Families-Regeln, Altersfreigabe, Store-Texte/Screenshots, interne Gerätetests und die zum Veröffentlichungszeitpunkt gültigen Play-Vorgaben. Keine Uploadbereitschaft wird behauptet.

Öffentliche Quellschnappschüsse lassen sich auch ohne Git-Historie bauen. Provenienzformat 2 meldet dann `source_tracking=unversioned-snapshot`, `source_commit=null`, `source_dirty=null`; der Inhalts-Hash der materialisierten App bleibt vorhanden. Ein übergeordnetes Repository wird nicht als Identität des Schnappschusses übernommen.
