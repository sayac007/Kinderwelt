# Android bauen

Die Komponenten und Prüfsummen stehen in `scripts/android/toolchain.json`: Godot 4.7.2, Temurin 17.0.16+8, Android API 36, Build Tools 36.1.0, Gradle 8.11.1 und Bundletool 1.18.2.

```sh
python3 scripts/android/install.py --root /workspace/tools --accept-android-sdk-license
# Privater Standardbuild setzt den lokalen privaten Grafikpack voraus:
python3 scripts/android/build.py --tools /workspace/tools --output build/android-current
# Getrennte lokale Test-App je Variante:
python3 scripts/android/build.py --tools /workspace/tools --variant family --preview --output build/android-v072-family
python3 scripts/android/build.py --tools /workspace/tools --variant public --preview --output build/android-v072-public
# Optionaler expliziter Bezeichner für einen kontrollierten Testbuild:
python3 scripts/android/build.py --tools /workspace/tools --variant public --package-id de.kinderwelt.test --output build/android-override
```

Die Lizenzoption setzt voraus, dass der Betreiber die Android-SDK-Lizenz akzeptiert. Jedes Ausgabeverzeichnis muss neu sein. Das Skript baut aus einer isolierten Kopie ausschließlich der App-Verzeichnisse; die Varianten-Grafiken werden dort eingesetzt. Beide SDK-Umgebungsvariablen zeigen auf denselben geprüften SDK. Fehlerblöcke aus Godot und Gradle erscheinen direkt im Protokoll; vollständige Logs bleiben im Ausgabeverzeichnis.

## Konfigurierbare, vorläufige Identität

Version **0.7.2 / 9**. `scripts/android/app-config.json` hält ausdrücklich die vorläufige Testkennung `org.example.kinderwelt`. Eine endgültige Paketkennung ist noch nicht entschieden. `--package-id` überschreibt nur den aktuellen Build; `export_presets.cfg` enthält `@KINDERWELT_PACKAGE_ID@`, das der Builder ersetzt. Android-Exporte deshalb über das Skript ausführen. Ungültige Bezeichner und Java-Schlüsselwörter werden vor dem Export abgelehnt; die Prüfung vergleicht anschließend die explizit erwartete Identität.

| Build | Paket bei Standardkonfiguration | Launchername |
|---|---|---|
| Standard, gewählte Variante | `org.example.kinderwelt` | Kinderwelt |
| Private Vorschau | `org.example.kinderwelt.preview.family.v072` | Kinderwelt 0.7.2 Privat Test |
| Öffentliche Vorschau | `org.example.kinderwelt.preview.neutral.v072` | Kinderwelt 0.7.2 Public Test |

Vorschauen haben eigene lokale Spielstände und können nebeneinander sowie neben früheren Versionen installiert werden. Die stabile Figuren-/Lösungslogik ist identisch; Daten werden nicht zwischen getrennten Android-Paketen kopiert.

## Artefakte und Prüfungen

Jeder Build liefert `kinderwelt-debug.apk`, ein **unsigniertes** `kinderwelt-unsigned.aab`, Prüfberichte, Quellprovenienz, Größenanalyse und Logs. Die APK wird nur mit einem temporären Godot-Entwicklungsschlüssel signiert. Dieser ist keine dauerhafte Update-Identität; ein APK-Update benötigt denselben Schlüssel wie die installierte App. Keine privaten Schlüssel werden eingecheckt. Vorhandene Installationen nicht unbedacht deinstallieren, wenn ihre lokalen Daten erhalten bleiben sollen.

Prüfungen: Paket, Version, API 24–36, keine Berechtigungen, deaktiviertes Backup, Bildschirmrotation, alle acht Fächer, drei Sprachmanifeste und sämtliche tatsächlich spielbaren Sprach-/Musik-/Grafikressourcen, ausgewählte Figurenvariante, zwei ABIs, 16-KB-ELF-Ausrichtung, ZIP-Ausrichtung, APK-Signatur und unsignierter Bundle-Status. Native Bibliotheken sind verlustfrei komprimiert und werden bei Installation entpackt. Neue Buildgrößen und tatsächlich erzeugte Dateien: [Testbericht](test-report.md).

## GitHub Actions

Die Workflows wählen ausdrücklich **public**, weil private Grafikpacks nicht im Repository liegen. [Android verification builds](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml) öffnen, passenden Branch/Lauf auswählen und unter **Artifacts** `android-development-artifacts` herunterladen. GitHub-Anmeldung ist erforderlich. ZIP entpacken und `kinderwelt-debug.apk` entnehmen. Dieser CI-Build verwendet die vorläufige Standardkennung; private APKs werden lokal gebaut.

Artefakte werden sieben Tage aufbewahrt und entstehen erst nach erfolgreichem Export/Upload. Ein Push oder lokal bestandener Build beweist keinen erfolgreichen Remote-Lauf. Geräteprüfungen sind separat erforderlich.

## Google Play bleibt offen

Es gibt keine Release-Signatur und keine Upload-Freigabe. Offen sind endgültige App-ID, dauerhafter Signierschlüssel mit sicherem Schlüsselspeicher/Play App Signing, Datenschutztext, Data-Safety-Angaben, Kinder-Zielgruppe und Families-Regeln, Altersfreigabe, Store-Texte/Screenshots, interne Gerätetests und die zum Veröffentlichungszeitpunkt gültigen Play-Vorgaben. Keine Uploadbereitschaft wird behauptet.
