# Android CI correction — 2026-10-20

Branch `feat/android-release`, starting at `99f9ea9`; correction for existing
PR #5. No new PR, release key, signing policy or Google Play gate was introduced.
The existing release remains blocked. Historical release evidence is preserved.

## Access boundary

`gh run list --repo sayac007/Kinderwelt --branch feat/android-release --workflow
android.yml` failed with GitHub API `Forbidden`. The unauthenticated workflow
web page returned HTTP 404. Therefore **the original failed Actions artifact and
its apk.log could not be downloaded or inspected here**. No original run ID or
original-log contents are invented. This report separates that limitation from
the concrete local reproduction below. A successful future Actions rerun is
not claimed; pushing the same branch triggers rechecking of PR #5.

## Concrete reproduced cause

The Ubuntu runner image exports both `ANDROID_HOME` and `ANDROID_SDK_ROOT`.
The old build script copied the parent environment and changed only
`ANDROID_HOME` to the pinned SDK. With the inherited root still pointing at an
existing second SDK, Android Gradle Plugin 8.6.1 rejects the conflicting paths.
Official runner configuration inspected at commit
`82d1b86ad393865982dd29535cb8d3adbc68e41e`:
[install-android-sdk.sh](https://github.com/actions/runner-images/blob/82d1b86ad393865982dd29535cb8d3adbc68e41e/images/ubuntu/scripts/build/install-android-sdk.sh).
This establishes the documented runner environment, not the unavailable failed
run's exact image revision.

First an absent foreign root was tried; that build passed because AGP ignores
an invalid SDK location. A second reproduction used an **existing** SDK root
(directory with platform-tools copied from the checksum-verified SDK):

```bash
mkdir -p /tmp/kinderwelt-runner-sdk
cp -a /workspace/tools/android-sdk/platform-tools /tmp/kinderwelt-runner-sdk/
ANDROID_HOME=/tmp/kinderwelt-runner-sdk \
ANDROID_SDK_ROOT=/tmp/kinderwelt-runner-sdk \
GODOT=/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64 \
  python3 scripts/android/build.py --output build/android-ci-existing-sdk
```

Before the SDK correction (already with improved log printing), this failed at
APK export with exit status 1. The actual reproduced apk.log says:

```text
* What went wrong:
Could not determine the dependencies of task ':compileStandardDebugJavaWithJavac'.
> Several environment variables and/or system properties contain different paths to the SDK.
  Please correct and use only one way to inject the SDK location.
  
  ANDROID_HOME: /workspace/tools/android-sdk
  ANDROID_SDK_ROOT: /tmp/kinderwelt-runner-sdk
  
  It is recommended to use ANDROID_HOME as other methods are deprecated
```

Complete pre-fix log:
`/workspace/Kinderwelt/build/android-ci-existing-sdk/apk.log`.
SHA256 `f5b35749806ef1c5fe633dd484091968795161db89981105458ea206e56800df`.
The main captured output `/tmp/kinderwelt-ci-existing-sdk.log` also contains that
cause and the new Actions error annotation. This is a demonstrated configuration
failure at the reported export step, not a list of speculative causes. Direct
comparison to the inaccessible original Actions log remains unavailable.

## Correction

Set both SDK variables in the child environment to the same resolved pinned SDK
path before any Godot/Gradle command. Do not change the parent shell, shared
runner SDK or export/signing settings. Print the selected SDK path without
printing the environment or credentials.

`run()` now prints a grouped, ANSI-clean excerpt on nonzero exit, Godot error
with exit zero, launch failure and timeout. It includes first/final cause blocks
and the final 80 lines with original line numbers; complete files remain in the
existing always-uploaded artifact. Child lines are prefixed to prevent them from
becoming Actions workflow commands. Each successful phase reports PASS. The
existing workflow's test discovery automatically runs the six added diagnostic
regressions; its step label now reflects both pipeline and package checks.

## Actual rerun results

All commands below were executed on the corrected working tree based on
`99f9ea9`; source_dirty=true in provenance accurately records uncommitted fixes
at test time. Final documentation changes do not alter the tested scripts.
Machine evidence: [android-ci-fix-evidence.json](android-ci-fix-evidence.json).

- `python3 -m unittest discover -s tests/android -v`: **16 PASS** (10 existing
  artifact checks + 6 new subprocess/diagnostic cases). New cases exercise a
  nonzero subprocess with a long log and middle cause, ANSI error/exit zero,
  partial output on timeout, successful output, command-line injection defense
  and missing executable. Log `/tmp/kinderwelt-ci-fix-unit.log`.
- `GODOT=... bash tests/qa/run.sh --output /tmp/kinderwelt-ci-fix-quality`:
  **PASS**. Existing smoke 33 + learning 559 + input 59 + scenarios 585 =
  **1236 checks**, zero failures. All **144** task/viewport combinations pass.
  GUT quality **6 tests / 13433 assertions**, selected GUT upstream tests
  **13 / 62**, QA Python tests **16**, fresh import/start and source stability
  all PASS. Log `/tmp/kinderwelt-ci-fix-quality.log`.
- The exact same existing foreign SDK variables were inherited again, now with
  output `build/android-ci-fix`: **APK and AAB exports PASS**. Package verification
  also PASS: ZIP integrity, identity/version/APIs, no requested permissions,
  backup disabled, fullUser orientation, both ABIs, no development/key files,
  native 16 KB ELF alignment, APK zipalign/apksigner v2 and unsigned AAB
  bundletool/manifest/jarsigner checks. Log `/tmp/kinderwelt-ci-fix-build.log`.

| Actual artifact | Bytes | SHA256 |
|---|---:|---|
| `build/android-ci-fix/kinderwelt-debug.apk` | 162757294 | `422e601dd12f730e3edb3ab8d166c3ad620781d42840544b157556c5ed2d2178` |
| `build/android-ci-fix/kinderwelt-unsigned.aab` | 52392096 | `05c315084d1aab91be0f7d70b77092d6b7d8233f264893afc8ebebc424c2665b` |

The APK uses only the existing ephemeral development-signing flow. The AAB is
unsigned. No release-signing operation was performed. Real-device and Play
approvals are unchanged; this correction concerns SDK selection and diagnostics.
