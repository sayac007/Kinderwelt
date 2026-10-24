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

Version **0.9.4 / 17**. `project.godot` is the single editable version source (`config/version` and `config/version_code`); the builder fills both export presets from it. `scripts/android/app-config.json` hält ausdrücklich die vorläufige Testkennung `org.example.kinderwelt`. Eine endgültige Paketkennung ist noch nicht entschieden. `--package-id` überschreibt nur den aktuellen Build; `export_presets.cfg` enthält `@KINDERWELT_PACKAGE_ID@` und Versionsplatzhalter, die der Builder ersetzt. Android-Exporte deshalb über das Skript ausführen. Ungültige Bezeichner und Java-Schlüsselwörter werden vor dem Export abgelehnt; die Prüfung vergleicht anschließend die explizit erwartete Identität.

| Build | Paket bei Standardkonfiguration | Launchername |
|---|---|---|
| Standard, gewählte Variante | `org.example.kinderwelt` | Kinderwelt |
| Private Vorschau | `org.example.kinderwelt.preview.family.v090` | Kinderwelt 0.9.4 Privat Test |
| Öffentliche Vorschau | `org.example.kinderwelt.preview.neutral.v090` | Kinderwelt 0.9.4 Public Test |

Der Testkanal `preview_channel=v090` ist unabhängig von der Versionsnummer, damit spätere Builds mit demselben Zertifikat als Update installierbar bleiben. Die alten 0.8.1-Schlüssel waren flüchtig und sind nicht wiederherstellbar. 0.9.0 wird deshalb parallel installiert; alte Punkte werden nicht automatisch zwischen Paketen übertragen. Für die vollständig gelöste erste Runde gibt es im Elternbereich eine ausdrückliche manuelle Bestätigung zur einmaligen Übernahme der 3200 früher verdienten Punkte. Die alte App nicht deinstallieren, wenn ihre Daten gebraucht werden.

Vorschauen haben eigene lokale Spielstände und können nebeneinander sowie neben früheren Versionen installiert werden. Die stabile Figuren-/Lösungslogik ist identisch; Daten werden nicht zwischen getrennten Android-Paketen kopiert.

## Artefakte und Prüfungen

Die aktuellen tatsächlich gebauten Varianten, Quellcommits und Prüfungen stehen im [Qualitätsüberblick](QUALITY_ASSURANCE.md). Ein früherer Build-Stopp für den damaligen Sprach-/Icon-Quellstand ist historisch; der aktuelle Auftrag umfasst überprüfbare Testpakete.

Jeder Entwicklungsbuild liefert `kinderwelt-debug.apk`, ein **unsigniertes** `kinderwelt-unsigned.aab`, Prüfberichte, Quellprovenienz, Größenanalyse und Logs. Die APK wird mit einem ausschließlich für Entwicklung vorgesehenen Godot-Schlüssel außerhalb des Repositorys signiert (`tools/preview-signing/debug.keystore`, alternativ `KINDERWELT_DEBUG_KEYSTORE`). Wiederholte lokale Builds verwenden denselben Schlüssel; die Prüfung vergleicht den SHA-256-Fingerabdruck des Zertifikats mit der APK. Vertrauenswürdige CI-Läufe verwenden einen privaten Actions-Cache; PR-Builds einen isolierten Schlüssel. Cache-Verlust oder ein anderer Branch mit eigenem Cache kann eine neue Entwicklungsidentität erzeugen. Für dauerhafte Testupdates muss der Entwicklungsschlüssel gesichert und derselbe Kanal verwendet werden; dies ist keine Release-Signierung. Keine privaten Schlüssel werden eingecheckt. Vorhandene Installationen nicht unbedacht deinstallieren, wenn ihre lokalen Daten erhalten bleiben sollen.

Prüfungen: Paket, Version, API 24–36, keine Berechtigungen, deaktiviertes Backup, Bildschirmrotation, alle acht Fächer, drei Sprachmanifeste und sämtliche tatsächlich spielbaren Sprach-/Musik-/Grafikressourcen, ausgewählte Figurenvariante, zwei ABIs, 16-KB-ELF-Ausrichtung, ZIP-Ausrichtung, APK-Signatur und unsignierter Bundle-Status. Native Bibliotheken sind verlustfrei komprimiert und werden bei Installation entpackt. Neue Buildgrößen und tatsächlich erzeugte Dateien: [Testbericht](test-report.md).

## GitHub Actions

Für vertrauenswürdige Pushes und manuelle Läufe erzeugt der Workflow nach Einrichtung des getrennten privaten Figurenrepositorys beide Varianten. Die Quellbilder werden aus einem festgelegten Commit mit einem gesonderten Lesetoken importiert; Pull Requests erhalten diesen Zugang nicht und bauen nur neutral. [Einrichtung des privaten Figurenrepositorys](family-repository.md). [Android verification builds](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml) öffnen, passenden Branch/Lauf auswählen und unter **Artifacts** `android-development-artifacts` herunterladen. GitHub-Anmeldung ist erforderlich. ZIP entpacken: `kinderwelt-debug-family.apk` und `kinderwelt-debug-neutral.apk` liegen direkt darin, außerdem zwei unsignierte AABs und Prüfberichte. Die Pakete sind getrennte Vorschau-Installationen. Den tatsächlich ausgeführten Lauf und die geprüfte Version dem aktuellen Testbericht entnehmen.

Artefakte werden sieben Tage aufbewahrt und entstehen erst nach erfolgreichem Export/Upload. Ein Push oder lokal bestandener Build beweist keinen erfolgreichen Remote-Lauf. Geräteprüfungen sind separat erforderlich.

For a family-only device test, run `android.yml` manually with `variant=family`:

```sh
gh workflow run android.yml --ref YOUR_BRANCH -f variant=family
```

This manual selection builds only the family cast. Its private Actions artifact
`kinderwelt-family-test` contains `kinderwelt-debug-family.apk` and technical
evidence, without the neutral APK or an unsigned bundle download. Push builds
still build both variants; pull requests still build only neutral without family
secrets. Existing signing-cache and pinned family-source rules are preserved.

[Device-local PNG avatar import](AVATAR_IMPORT_FEASIBILITY.md) is implemented
for 0.9.4. Only the parents area adds/replaces/removes images; chooser Help is
read-only. The build still rejects every permission and additionally verifies
compiled cloud/device-transfer backup exclusions. Native device checks remain open.

Current **0.9.4 / 17** family-only download (2026-10-24):
[kinderwelt-family-test](https://github.com/sayac007/Kinderwelt/actions/runs/40105564671/artifacts/12564507418),
from [successful manual run 40105564671](https://github.com/sayac007/Kinderwelt/actions/runs/40105564671),
commit `f892418ac23a4d79a3e442082fd92c5c5117f343`. One private artifact,
**322,605,725 bytes**, expires 2026-10-31. Unzip and install
`kinderwelt-debug-family.apk`; neutral APK and unsigned AAB are not included.
The run passed actual APK/AAB resource, identity, signing/alignment, zero-permission
and backup checks. Failed runs are now explicitly named diagnostic artifacts;
unverified raw binaries in variant subdirectories are excluded from uploads.

Previous family-only test download (0.9.3, 2026-10-24):
[kinderwelt-family-test](https://github.com/sayac007/Kinderwelt/actions/runs/40096417060/artifacts/12561253077),
from [successful manual run 40096417060](https://github.com/sayac007/Kinderwelt/actions/runs/40096417060)
at commit `8153f919454e05a962e4d04d8b5d56a55b3b4009`. Version remains **0.9.3 / 16**;
the game sources are unchanged. The ZIP contains the installable family APK and
technical reports; the ordinary multi-variant upload was skipped. GitHub login
is required. This is a seven-day CI artifact, not permanent archival storage.

## Google Play bleibt offen

### Package 1: operator-configured neutral upload signing

Development exports above retain their debug APK and unsigned AAB. A separate
`--release` mode builds **only the neutral AAB**, never the private family cast.
It does not publish or upload to Play. A technically verified signature does
not replace the remaining licensing, privacy, store or device approvals.

The operator must decide the final package, publisher, support contact and asset
licence. No such facts or permissions are invented here. Release export fails
before tool access when the package or required environment variables are absent.
It also rejects unfilled entries in
`scripts/android/release-metadata.json`; the corresponding environment variables
override those placeholders without committing personal contact information.
The package must pass the existing lowercase Android/Java identifier checks and
must not contain `example`, `test` or `debug`. `--preview` and family release
exports are rejected.

Required configuration (supply real values securely; these are names, not credentials):

| Variable | Purpose |
|---|---|
| `KINDERWELT_PACKAGE_ID` | Final package; alternatively `--package-id` |
| `KINDERWELT_UPLOAD_KEYSTORE` | Existing keystore path **outside the repository**, or `base64:` followed by its Base64 bytes; at most 1 MiB |
| `KINDERWELT_UPLOAD_ALIAS` | Upload key alias |
| `KINDERWELT_UPLOAD_STORE_PASSWORD` | Keystore password |
| `KINDERWELT_UPLOAD_KEY_PASSWORD` | Private key password |
| `KINDERWELT_PUBLISHER` | Operator-confirmed publisher |
| `KINDERWELT_SUPPORT_EMAIL` | Operator-confirmed support contact |
| `KINDERWELT_ASSET_LICENSE` | Operator's asset licensing decision; this check is not legal approval |

With these values already loaded into the environment:

```sh
python3 scripts/android/build.py --release --variant public \
  --tools /workspace/tools --output build/android-release-new
```

Output: `kinderwelt-release-neutral.aab`, `provenance.json`, `verification.json`
and sanitized technical evidence. No debug key is loaded/created by this path.
Godot/Gradle export the unsigned bundle without upload credentials; JDK jarsigner
then signs it using password environment variables, with tool output withheld.
The temporary decoded keystore is private (0600), outside source, and removed
on success or failure. The intermediate unsigned bundle is removed after signing.
Verification checks every payload entry's actual JAR signature against the
expected upload certificate, certificate validity, package/version, resources,
zero permissions, disabled backup and the existing native packaging requirements.
Unsigned, modified, partially unsigned and wrong-signer bundles fail verification.
The technical report still marks Play upload readiness **BLOCKED**.

To create an operator-owned upload key, the following is **documentation only**;
Codex has not run it for a real upload/release identity. Run it locally in a
trusted terminal, choose the prompted identity/passwords yourself, and keep the
keystore out of the checkout and shared folders:

```sh
keytool -genkeypair -storetype JKS -keystore /secure/offline/kinderwelt-upload.jks \
  -alias upload -keyalg RSA -keysize 3072 -validity 10000
```

Keep an encrypted offline backup of the key, alias and passwords in the operator's
password/key management system; do not put them in Git, chat, shell history,
Actions logs or artifacts. In Play Console the operator enables **Play App
Signing** and retains the upload key separately from Google's app signing key.
An upload-signed AAB is not an installable APK and cannot update the development
APK by itself. Changing package/signing identity must be planned before testing
with existing local progress.

The separate `.github/workflows/android-release.yml` has only `workflow_dispatch`
and read-only repository access. Its signing job runs only at `refs/heads/main`
and declares the GitHub Environment **`release`**. Before storing any real upload
credentials, the operator must configure that Environment in repository Settings:
require an explicit reviewer approval, restrict deployment branches to **main**,
and check that the repository's GitHub plan supports and enforces those rules.
The YAML references the Environment; it cannot create or guarantee its reviewer
protection settings. Those settings remain **NOT VERIFIED** until the operator
checks them. Do not store real upload credentials in an unprotected Environment.

Store the four `KINDERWELT_UPLOAD_*` secrets **in the protected release Environment**,
not as repository/organization-wide secrets (use the Base64 representation for
the keystore). Remove/migrate any old repository-level copies so other workflows
cannot read them. Configure the three operator metadata variables there as well.
Supply the final package in the manual input. Environment approval applies even
to the first missing-secrets test; after approval it should visibly skip signing.
With missing configuration it reports **Release signing SKIPPED** and succeeds
without building. Only a fully verified neutral bundle and its technical reports
are uploaded. Decoded signing material stays in a private directory below
`RUNNER_TEMP/kinderwelt-release`. In addition to per-process finally cleanup, an
`always()` job step deletes that directory, including after export failure; no
signing-directory cache or artifact is configured. Hosted-runner teardown covers
forcible runner termination. The workflow receives no family-repository token, never checks out
family assets and does not change the production Android verification workflow.

Regression tests use only an isolated, short-lived **disposable test key**, as
explicitly required by package 1 acceptance. That fixture is destroyed after
testing, never retained in Git/artifacts and never represents the operator.

[Vorbereitete Play-Entscheidungen und Datenschutz-/Store-Entwürfe](PLAY_READINESS.md). Es gibt keine Release-Signatur und keine Upload-Freigabe. Offen sind endgültige App-ID, dauerhafter Signierschlüssel mit sicherem Schlüsselspeicher/Play App Signing, Datenschutztext, Data-Safety-Angaben, Kinder-Zielgruppe und Families-Regeln, Altersfreigabe, Store-Texte/Screenshots, interne Gerätetests und die zum Veröffentlichungszeitpunkt gültigen Play-Vorgaben. Keine Uploadbereitschaft wird behauptet.

Öffentliche Quellschnappschüsse lassen sich auch ohne Git-Historie bauen. Provenienzformat 2 meldet dann `source_tracking=unversioned-snapshot`, `source_commit=null`, `source_dirty=null`; der Inhalts-Hash der materialisierten App bleibt vorhanden. Ein übergeordnetes Repository wird nicht als Identität des Schnappschusses übernommen.
