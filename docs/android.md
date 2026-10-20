# Android bauen

Die Komponenten und Prüfsummen stehen in `scripts/android/toolchain.json`: Godot 4.7.2, Temurin 17.0.16+8, Android API 36, Build Tools 36.1.0, Gradle 8.11.1 und Bundletool 1.18.2.

```sh
python3 scripts/android/install.py --root /workspace/tools --accept-android-sdk-license
python3 scripts/android/build.py --tools /workspace/tools --output build/android-current
# Separates Testpaket, wenn eine vorhandene Installation nicht aktualisiert werden kann:
python3 scripts/android/build.py --tools /workspace/tools --preview --output build/android-test
```

Die Lizenzoption setzt voraus, dass der Betreiber die Android-SDK-Lizenz akzeptiert. Jedes Ausgabeverzeichnis muss neu sein. Das Skript baut aus einer isolierten Kopie ausschließlich der App-Verzeichnisse. Beide Android-SDK-Umgebungsvariablen zeigen auf dasselbe geprüfte SDK. Fehlerblöcke aus Godot und Gradle werden direkt ausgegeben; vollständige Logs bleiben im Ausgabeverzeichnis.

Standardpaket: `org.example.kinderwelt`, Version **0.6.0 / 6**. Testvariante: `org.example.kinderwelt.preview`, Launchername **Kinderwelt 0.6 Test**, eigener lokaler Spielstand. Sie enthält dieselbe neue App und kann neben einer vorhandenen Installation stehen.

Jeder Build liefert `kinderwelt-debug.apk`, ein **unsigniertes** `kinderwelt-unsigned.aab`, Prüfberichte, Quellprovenienz, Größenanalyse und Logs. Die APK wird nur mit einem temporären Godot-Entwicklungsschlüssel signiert. Dieser ist keine dauerhafte Update-Identität; normale APK-Updates benötigen denselben Schlüssel wie die installierte App. Keine privaten Schlüssel werden eingecheckt. Eine vorhandene App nicht unbedacht deinstallieren, wenn deren lokale Daten erhalten bleiben sollen.

Die Prüfung kontrolliert Paket, Version, API 24–36, Berechtigungsfreiheit, deaktiviertes Backup, Bildschirmrotation, alle acht Fächer, drei Sprachmanifeste und sämtliche tatsächlich spielbaren Sprach-/Musik- und Grafikressourcen, zwei ABIs, 16-KB-ELF-Ausrichtung, ZIP-Ausrichtung, APK-Signatur und unsignierten Bundle-Status. Native Bibliotheken sind verlustfrei komprimiert und werden bei Installation entpackt.

GitHub Actions führt die aktuelle Testsuite, echte Software-Renderings und Android-Exporte aus. Das ist keine Geräteprüfung.

## Google Play bleibt offen

Es gibt weder eine Release-Signatur noch eine Upload-Freigabe. Eine Betreiberentscheidung zu App-ID und dauerhaftem Signierschlüssel, sicherer Schlüsselspeicher/Play App Signing, Datenschutztext, Data-Safety-Angaben, Kinder-Zielgruppe und Families-Regeln, Altersfreigabe, Store-Texte und aktuelle Screenshots, interne Gerätetests und die zum Veröffentlichungszeitpunkt gültigen Play-Vorgaben sind erforderlich. Es wird keine Uploadbereitschaft behauptet.
