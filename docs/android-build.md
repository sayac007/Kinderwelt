# Reproducible Android verification builds

Linux x86_64, Python >=3.12, curl, unzip, git. From the repository root:

```bash
GODOT_INSTALL_DIR=/workspace/tools/godot-4.7.2 bash scripts/install-godot.sh
# Read https://developer.android.com/studio/terms before accepting the SDK licence.
python3 scripts/android/install.py --root /workspace/tools --accept-android-sdk-license
export GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64
python3 -m unittest discover -s tests/android -v
bash tests/qa/run.sh
python3 scripts/android/build.py --tools /workspace/tools
python3 scripts/android/verify.py --tools /workspace/tools --output build/android
```

Output must not already exist; choose `--output build/android-another-run` for a
repeat build. This prevents stale bundles being reported as success. Installation
is repeatable and verifies cached archives again. No service is needed to build.
No cloud worktree is required; use the existing checkout.

`toolchain.json` pins Godot 4.7.2 (`ed1daf0bf`), official matching export templates,
Temurin JDK 17.0.16+8, commandline-tools 19.0 (13114758), platform API 36 revision 2,
Build Tools 36.1.0, platform-tools 37.0.1, Gradle 8.11.1 and bundletool 1.18.2.
Engine/templates use official release SHA512; JDK checksum is from the Adoptium
release. SDK SHA256 pins were recorded after verification against Google's
repository XML SHA1 checksums over verified HTTPS. Bundletool SHA256 pins the
actual official GitHub release download; upstream did not supply an independently
retrieved signature. Gradle's wrapper verifies the official distribution SHA256.

The official template's Gradle/Maven dependency versions are retained. This is a
repeatable version-pinned build, not a claim of byte-identical output or fully
hermetic dependency resolution: Maven repositories and HTTPS trust remain
external inputs; timestamps and ephemeral development certificates vary. Record
`provenance.json`, hashes and `verification.json` with each build. Private signing
material is never generated as a production identity. Godot creates its standard
throwaway development key inside an isolated temporary configuration for the APK;
it is removed with that directory. Thus subsequent APKs may need uninstalling
before reinstalling; that can erase local progress. No key is in the output.

The build copies only core, games, content, assets and project/export settings
into a temporary project, imports afresh and builds both architectures arm64-v8a
and x86_64. Export filters additionally exclude development files. Verification
checks packaged JSON for all five modules, no GUT/tests/docs/key files, ZIP
integrity, manifest identity/version/API, zero permissions, backup disabled,
fullUser orientation, APK v2 signature and 16 KB ZIP/native ELF alignment.
Bundletool validates the AAB and dumps the manifest; jarsigner confirms it is
unsigned. These are technical checks, not installation or store acceptance.

Proxy environments: build.py converts an existing unauthenticated HTTPS_PROXY
host/port into Java proxy options. When present, it uses the system Java CA store
at `/etc/ssl/certs/java/cacerts`. TLS verification stays enabled. Authenticated
proxies require separate secure configuration; credentials are never copied.
Godot may try starting ADB during export even without devices; a cloud ADB home
error does not constitute an app device test. Use a writable Android developer
account for actual ADB installation.

## Secure optional release signing

First approve a permanent application ID, version sequence, release-time target
API and all release checklist items. Rebuild after changing the presets and
corresponding verifier expectations. The current unsigned artifact is named
`kinderwelt-unsigned.aab`; the release filename is reserved for a successfully
signed bundle. There are no release credentials in this repository or CI.

An owner controls a real upload keystore outside the checkout and stores a secure
backup. Use a protected CI environment or a trusted local session; never run
signing on untrusted pull requests. Obtain passwords via the platform's secure
secret injection (not chat, command arguments, source files, or shell history).
With `UPLOAD_KEYSTORE`, `UPLOAD_ALIAS`, `UPLOAD_STORE_PASSWORD` and
`UPLOAD_KEY_PASSWORD` supplied securely:

```bash
# Do not enable shell tracing. These are variable references, never password values.
/workspace/tools/android-jdk/bin/jarsigner \
  -keystore "$UPLOAD_KEYSTORE" -storepass:env UPLOAD_STORE_PASSWORD \
  -keypass:env UPLOAD_KEY_PASSWORD -sigalg SHA256withRSA -digestalg SHA-256 \
  -signedjar build/android/kinderwelt-release.aab \
  build/android/kinderwelt-unsigned.aab "$UPLOAD_ALIAS"
/workspace/tools/android-jdk/bin/jarsigner -verify -verbose -certs build/android/kinderwelt-release.aab
/workspace/tools/android-jdk/bin/keytool -printcert -jarfile build/android/kinderwelt-release.aab
/workspace/tools/android-jdk/bin/java -jar /workspace/tools/android-tools/bundletool-1.18.2.jar \
  validate --bundle=build/android/kinderwelt-release.aab
sha256sum build/android/kinderwelt-release.aab
```

These signing commands are prepared, **not executed**. Verify the certificate
SHA256 against the owner's independently recorded upload certificate; check
algorithm, validity, no unsigned entries and complete manifest/payload validation
again. Do not treat jarsigner exit zero alone as release approval. Enrol in Play
App Signing with the owner's decision. Protect/delete transient secret files.
No Play Console upload is automated or authorized by this pipeline.

For devices: `adb install build/android/kinderwelt-debug.apk` from the pinned
platform-tools, then follow the checklist. Testing the delivered AAB via generated
split APKs (bundletool/Play internal track) is also mandatory before release.

Both APK and AAB use the matching official Gradle source template. Direct
(non-Gradle) APK export was tried and rejected after a missing themed-icon
resource reference appeared in aapt2 output. The Gradle path resolves resources
normally. The official 4.7.2 template retains AGP 8.6.1, which warns that API 36
is above its tested compileSdk range; the warning is not suppressed. Actual
package validation is required each run, and owner review of a supported future
engine/toolchain update remains a release consideration.

## Export failure diagnostics and hosted runners

The build sets both `ANDROID_HOME` and `ANDROID_SDK_ROOT` to the same resolved,
pinned SDK directory. Ubuntu Actions runners already export a system SDK root;
changing only `ANDROID_HOME` leaves two valid SDK locations and AGP 8.6.1 rejects
that configuration before `compileStandardDebugJavaWithJavac`.

On subprocess failure, timeout or a Godot error with exit status zero, build.py
prints a grouped, ANSI-clean excerpt directly to stdout: initial context, the
first/last Gradle/Godot cause blocks and the final 80 lines, with original line
numbers. An Actions error annotation identifies the failed log. Complete logs
remain in the existing always-uploaded artifact. Child log lines are prefixed so
they cannot become workflow commands. Successful import/APK/AAB phases print PASS.
No environment dump or release-signing invocation was added.

See [the CI correction evidence](android-ci-fix-report.md) for the reproduced
SDK conflict, access limitations and the actual rerun results.
