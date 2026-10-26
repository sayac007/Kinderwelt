# Kinderwelt: Qualität und Prüfstand

**Klasse 1–2:** Ein lokal spielbares Godot-Lernabenteuer mit 400 Grundaufgaben und 800 freiwilligen Boni. Kinder bewegen eine Figur durch sieben wählbare Kulissen und sammeln dauerhaft gespeicherte Punkte. Keine Konten, Werbung, Käufe, Mikrofonaufnahmen oder Telemetrie integriert. Technische Prüfergebnisse sind kein Nachweis pädagogischer Wirksamkeit oder einer Google-Play-Freigabe.

The separate [visual asset IP audit](qa/VISUAL_IP_AUDIT.md) adds two named, current reference files under `docs/qa/`. Its privacy-redacted inventory and local review packs do not constitute legal clearance. The two-file folder counts below describe the pre-audit 0.9.3 verification snapshot.

## Operator device acceptance — 2026-10-26

The operator reports **image selection, rotation and updates PASS on a phone and
a tablet**, with the exercised app behaviour working. The [acceptance record](ACCEPTANCE.md)
and [issue register](play/known-issues.md) now record that practical acceptance.
Device/OS identifiers and the tested app version/hash were not supplied; no broad
Android-version matrix or individually executed backup/transfer test is invented.
This is operator-reported manual evidence, separate from assistant-run automated
checks, full native-language listening or empirical learning-effect evidence.
Earlier NOT VERIFIED statements below remain historical snapshots, superseded
for this reported device-test scope.

The technical baseline is merged `main` `0c42d326`, with the same source tree as
the locally verified `1afb7edb` (224 Python tests and the full Godot suite).
Latest main [Quality](https://github.com/sayac007/Kinderwelt/actions/runs/40356409169),
[Android](https://github.com/sayac007/Kinderwelt/actions/runs/40356409187) and
[Store](https://github.com/sayac007/Kinderwelt/actions/runs/40356409325) runs passed.
These are existing technical results, separate from the new operator report.

The existing key-generation path now has a [browser-only Azure Cloud Shell alternative](android-cloud-shell.md).
This is an operator-run procedure, not a newly executed signing job. Play Console
completion remains with the operator and is outside this update.

## Actions storage remediation — 2026-10-26

The operator-requested cleanup deleted **210 transient artifacts / 66,713,266,904 bytes**;
the immediate post-cleanup API snapshot listed **5 retained artifacts / 505,439,680 bytes** (about 482 MiB).
This is observed repository inventory, not a confirmed refreshed billing quota.
`Kinderwelt-Privat` has zero Actions artifacts. The live `Kinderwelt` repository
is currently public. No release or permanent QA archive was removed or created.

[Current download/retention rules and preserved files](ci-artifacts.md): automatic
main/PR checks keep the full suite, renders and neutral Android export/verification/
size checks, but upload no artifacts. Manual APK requests default to neutral;
family access, AABs, screenshots and complete listening packs require explicit
selection. The newly integrated Store workflow uploads only on manual runs too.
New uploads last three days. Six storage regressions cover these
rules. The documentation checker also verifies extensionless Jekyll sibling-page
sources; it previously rejected the operator's valid new Pages navigation.
The supplied privacy text and live route links are unchanged.

The original **139 historical QA files / 7,383,943 bytes** were reverified via
GitHub tree/tag and local SHA-256 against archive commit
`a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`. Historical run logs/source remain;
links to deleted temporary downloads below now lead to their retained runs.
Repository-wide retention cannot be changed by this integration (Actions admin
API HTTP 403); the operator must set Settings → Actions → General → Artifact
and log retention to three days. Workflow rules take effect after review/merge.
Full current validation is recorded in the focused storage Draft PR; no new
single-run report is committed under `docs/qa/`.

## Publication preparation: 0.9.6 / 19 (2026-10-26)

The following records the initial preparation snapshot; current merged CI and
operator device acceptance are recorded above.

[Current handoff, signing setup and quota-safe delivery](play/PUBLICATION.md).
The confirmed release package is `io.github.sayac007.kinderwelt`; development
packages and their save/signing channel remain unchanged. The preparation starts
at current `main` `75655da2` and restores the reviewed Store/test work that had
landed in predecessor feature branches.

- **PASS locally:** full current suite, **217 Python tests**, **18 new offline
  privacy-view checks**, 15 version-display / 479 crop / 62 import/restart checks
  and existing quest, world, points, speech, layout, fresh-import and content gates.
- The original German policy upload is unchanged. DE/EN/RU offline app text and
  four static HTML pages are generated/checked against the supplied master and
  translation sources. EN/RU translations still need operator review. No web
  hosting/publication was enabled. Privacy text is a read-only parent screen;
  the Google reference is plain text and opens no browser/network service.
- The latest main CI failures are proven **Actions artifact storage quota**
  errors, not a Godot build failure. Quality uploads now follow all technical
  checks, so unavailable delivery cannot prevent the render checks from running.
- A separate manual/main-only/private-repository draft-release delivery path is
  prepared for the verified neutral upload-signed AAB, without Actions artifact
  storage. Only that job requests repository write permission for the private
  draft; the original release workflow remains read-only. Live signed delivery
  is **NOT VERIFIED**. No historical artifact or family source was deleted.
- The real main release probe [40322560219](https://github.com/sayac007/Kinderwelt/actions/runs/40322560219)
  **skipped export**, reporting unavailable signing credentials/operator fields.
  Publisher/contact defaults now use the supplied document. Operator asset
  statement now reads “Alle Rechte vorbehalten, soweit Schutzrechte bestehen.”
  Four upload-key secrets remain required; no production key was
  created and no signed release AAB is claimed.

Clean application source `dbbff35cd50005b43d6736d231adb47c6357ce1c` exported
and verified neutral APK **319,079,418 bytes** and unsigned AAB **305,170,971 bytes**
in `/tmp/kinderwelt-publication/android-neutral/`: correct release package,
0.9.6 / 19, API 24–36, zero permissions, backup exclusions, 16KB checks,
**7,803 resources / 15 notice files**, development APK signer and unsigned AAB
status PASS. Provenance records clean/unchanged source. The real unsigned AAB
was rejected by draft delivery before any GitHub call. Bundletool measured
**274,754,030 bytes** initial download, **27,914,430** base and **246,839,600**
install-time assets; internal base budget PASS. No media was re-encoded.

Twelve real policy frames rendered in DE/EN/RU, phone/landscape, start/end;
German phone start and Russian landscape end were visually inspected. These
are desktop frames, not physical Android certification. Subsequent operator-
licence and inactive-template documentation changes leave application bytes
unchanged. Updated licence, signing, delivery, source-variant, policy and template
regressions passed separately after those changes.

[Push quality 40329261366](https://github.com/sayac007/Kinderwelt/actions/runs/40329261366),
[Android 40329261368](https://github.com/sayac007/Kinderwelt/actions/runs/40329261368)
and [Store 40329261399](https://github.com/sayac007/Kinderwelt/actions/runs/40329261399)
failed only in artifact-retention steps with the confirmed storage-quota error;
technical test/render/build/size steps succeeded. The quality renders now run
before retention, as intended. This is **not an overall green CI/upload result**.
No signed AAB, live draft delivery or public privacy URL is claimed.

Physical Android picker/update/backup acceptance, human listening,
external email/Google practices, privacy hosting and Play decisions remain open.
No new task/audio/artwork content or empirical learning-effect claim is introduced.

## Play preparation snapshot: 0.9.5 / 18

Separate draft changes retain package boundaries: [local images #27](https://github.com/sayac007/Kinderwelt/pull/27)
and [privacy/Store materials #28](https://github.com/sayac007/Kinderwelt/pull/28).
[Upload checklist and reproducible commands](play/README.md),
[three-language tester guide](play/closed-test.md), [open acceptance](play/known-issues.md).

- **Package 4 PASS in CI:** immutable `b87b4d1fcf76f2ef841c652df9930f658dcd26f0`;
  [quality 40124170330](https://github.com/sayac007/Kinderwelt/actions/runs/40124170330)
  and [Android 40124170320](https://github.com/sayac007/Kinderwelt/actions/runs/40124170320).
  Push and PR gates passed. Runtime: 479 new crop/format/orientation checks plus
  62 existing avatar/privacy/restart checks. JPEG/PNG/static WebP; all eight EXIF
  orientations; actual synthetic GPS/camera metadata removed; selected crop,
  private-only storage, points, legacy PNGs, deletion/reset and touch handling.
  No photo/person input was used. Existing quest/world/reward/speech/layout and
  fresh-import gates passed. Twenty-four local crop frames were rendered; selected
  actual phone/landscape views were inspected and reset-button width corrected.
- Both cast variants' APKs and unsigned AABs passed actual resource/15-notice-byte,
  identity, signing/alignment, permission and compiled backup-rule checks in the
  push run above; PR built neutral without family secrets.
  [Private APK/AAB artifact](https://github.com/sayac007/Kinderwelt/actions/runs/40124170320/artifacts/12572279652)
  expires after seven days. These remain development identities, **not final Play bundles**.
- **Package 5 Store CI PASS:** immutable `7a24f94ce42f2be43d66d4263e2f3db38a0fbfa9`,
  [render run 40125177324](https://github.com/sayac007/Kinderwelt/actions/runs/40125177324),
  [quality 40125177353](https://github.com/sayac007/Kinderwelt/actions/runs/40125177353)
  and [Android 40125177326](https://github.com/sayac007/Kinderwelt/actions/runs/40125177326)
  all passed. The later documentation-only notice correction leaves the asset
  distribution licence with the operator; it changes no app/capture bytes.
  Seventeen dimension-checked neutral PNGs: icon, feature and five 1080×1920
  phone captures per language; own-image input is a geometric silhouette.
  Four static, script-free privacy HTML drafts generated. Publication is inactive;
  `--final` rejects unresolved operator placeholders. Six new Store regressions
  cover stale listings, privacy publication guards, geometric-only inputs and
  rejection of family/unknown cast resources. Full current local suite passed
  **207 Python tests**, including those six, plus existing runtime/content gates.
- Listing text is generated/checked against actual catalogs: 8 × 50 base tasks,
  800 bonuses, 7 scenes, 3 languages and 20 music tracks. It contains no learning
  effectiveness claim. Adult listening, independent pedagogy and empirical
  learning effects remain separate open work.
- **Package 6 PASS locally:** complete current suite, **207 Python tests** plus
  **15 actual parent-display checks** in DE/EN/RU, 479 crop + 62 existing avatar
  checks and all existing runtime/content gates. Source application commit
  `77735caca21980876eb14f1d2b4e51c6ac7a021d`.
  No optional report/email button, telemetry or new diagnostic export is added.
- **PASS locally, clean source:** the same commit exported and verified neutral
  APK **319,072,131 bytes** and unsigned AAB **305,164,266 bytes** in
  `build/android-play-preparation-neutral/`. Provenance records `source_dirty=false`
  and no Git-state change during build. Identity `org.example.kinderwelt` remains
  provisional; version **0.9.5 / 18**, API 24–36, both ABIs, 16KB ELF/ZIP checks,
  7,802 payload resources and all 15 byte-matched notices passed. APK uses only
  the cached development key; AAB is explicitly unsigned. Zero permissions and
  compiled cloud/device-transfer exclusions passed. This is not an operator-signed
  Play release.
- Pinned bundletool measured that exact AAB for arm64/de/API36/480dpi:
  **274,747,187 bytes** initial download, **27,914,374** base and **246,832,813**
  additional install-time assets. Internal 190 MB base budget **PASS**. Reports
  are in the ignored build directory; no media was transcoded or key generated.
- The final local Store render generated/verified **17 PNGs** again from clean
  application commit `77735cac` (`build/store-release-preparation/`). Russian own-
  image and English reward frames were visually inspected. The independent
  [combined Store CI 40125379912](https://github.com/sayac007/Kinderwelt/actions/runs/40125379912)
  also **PASS**; [private review drafts](https://github.com/sayac007/Kinderwelt/actions/runs/40125379912/artifacts/12572801385)
  expire after seven days. Direct CI download returns HTTP 403 here; the CI job
  result/metadata are visible, but no downloaded CI pixels are claimed reviewed.
  [Combined quality 40125379916](https://github.com/sayac007/Kinderwelt/actions/runs/40125379916)
  and [Android 40125379879](https://github.com/sayac007/Kinderwelt/actions/runs/40125379879)
  both **PASS** at `77735cac`; PR quality 40125444850 and Android 40125444946 also
  **PASS**. [Current APKs/AABs and technical reports](https://github.com/sayac007/Kinderwelt/actions/runs/40125379879/artifacts/12573542271),
  [quality renders/reports](https://github.com/sayac007/Kinderwelt/actions/runs/40125379916/artifacts/12572717673)
  and [full offline listening review](https://github.com/sayac007/Kinderwelt/actions/runs/40125379916/artifacts/12572882115)
  are private seven-day artifacts. The code/application tree remains unchanged
  by subsequent `[skip ci]` documentation-only synchronization/results commits.
  [Closed-test draft #29](https://github.com/sayac007/Kinderwelt/pull/29) completes
  the three separate review packages. No PR was automatically merged.

**NOT VERIFIED / OPERATOR:** Android 13+ and 10–12 selection/URI/lifecycle,
real hardware performance/update/backup transfer; complete human listening and
independent content review; publisher/contact/legal bases/rights, privacy hosting,
final package/upload key, current audience/rating/Data Safety answers and Play
track/pre-launch approval. The release-environment API returned 404 here; actual
required reviewers/deployment restrictions are **not certified** by the workflow
configuration. No Play setting, production key or family source was changed.
No pedagogical efficacy or upload-readiness claim follows from these tests.

## Play preparation: package 3 source and recording notices (0.9.4 / 17)

Code commit: `bb863fae3d1c2072165a5b284ac9d5c0ea13e6bd`, 2026-10-24.
[Software/asset scope and pending operator decision](../ASSETS_LICENSE.md).

- The root MIT software licence is unchanged. Its exact text is also bundled;
  it does not blanket-license artwork, voice recordings, fonts or music.
- All five CC-BY-SA-derived recordings retain the source's exact licence version
  and link in the music notice and DE/EN/RU parent credits. Russian credits now
  also retain original authors, pinned source URLs and piano-source attribution.
  URLs are displayed as text; no link-opening/network function was added.
- Both export presets and actual APK/AAB bytes must retain **15 notice files**:
  software MIT, font OFL, music notices and six music/source licence texts, plus
  all three voice cards and their licence/provenance notices. Missing, modified,
  excluded or duplicate files fail verification, including install-time assets.
- [Legacy chronology](character-origins.md) now reflects the original four PNGs'
  C2PA creation claims on 20 October 2026. Their original Git bytes/hashes and
  metadata were re-read locally; no images were regenerated/replaced. Signature
  authenticity and rights are not inferred from those claims.
- **PASS locally:** full existing suite with **199 Python tests**, 12,750 quest /
  4,168 world / 1,231 reward checks and the existing privacy, speech, layout and
  content guards. Ten notice regressions cover source scope, same-version policy,
  both filters and each missing/modified/duplicate packaged notice. The updated
  verifier's 18 regressions and five source-variant tests also passed separately.
- **PASS locally:** the final credits view passed **528 checks** with six real
  rendered images, covering 20 tracks, three locales and both orientations.
  Two frames (Russian phone, English landscape) were visually inspected. This
  is not a claim of independent visual/legal review of every track or device.
- Existing audio files, original music manifest fields (including hashes,
  durations and source licences), model cards, image bytes, task contents,
  signing identity and Android workflows are unchanged. Only notice metadata,
  the parent credits and the required software-notice include filter changed.
- [Quality CI 40119107940](https://github.com/sayac007/Kinderwelt/actions/runs/40119107940)
  and [Android CI 40119107914](https://github.com/sayac007/Kinderwelt/actions/runs/40119107914)
  both **PASS** at the code commit above. Quality CI completed the full current
  suite, existing real-render checks and the six additional credits frames.
  Android CI rebuilt and verified both cast variants’ APKs and unsigned AABs,
  including all 15 source-matched notices.
  [Technical renders/reports](https://github.com/sayac007/Kinderwelt/actions/runs/40119107940),
  [offline adult listening review](https://github.com/sayac007/Kinderwelt/actions/runs/40119107940),
  [verified development APKs/AABs and reports](https://github.com/sayac007/Kinderwelt/actions/runs/40119107914)
  were temporary seven-day CI artifacts. They were removed during the operator-requested storage cleanup on 2026-10-26; these links now lead to the retained run logs, not downloads. They were never permanent legal evidence.
- An additional local neutral APK and unsigned AAB also passed actual identity,
  signature/alignment, resources, zero permissions, backup and all 15 notice-byte
  checks (`build/android-package3-neutral/`). That supplemental build records
  `source_dirty=true` because the QA summary was being edited; it is not claimed
  as clean provenance. The CI source above is the immutable reference.

**NOT VERIFIED:** the operator's `{{ASSET_LIZENZ_DES_BETREIBERS}}`, rights for
distribution, hardware acceptance, protected real-key release and Play approval.
The English voice card declares only its **dataset** public domain; no separate
model/output grant is supplied by that card or invented by the new provenance
notice. Qwen's Apache model licence is not automatically applied to recordings.
C2PA signature/trust verification remains unperformed. Technical notice delivery
does not settle these decisions. At this package-3 snapshot, packages 4–6 and `docs/qa/` cleanup were untouched.

## Play preparation: package 2 size measurement (0.9.4 / 17)

Measurement implementation: `c4bdb9b9526fae95a5e4304044f1e79d2fea8a87`;
additional test-only orchestration check: `d2d28897`. Measured on 2026-10-24.
[Reproduction, method, official limits and analysis-only options](android.md).

| Pinned bundletool, arm64 / de / API 36 / 480 dpi | Local fixture bytes | CI neutral preview bytes |
|---|---:|---:|
| Initial download including install-time assets | 274,733,766 | 274,734,124 |
| Base module | 27,914,395 | 27,914,648 |
| Additional install-time assets (difference) | 246,819,371 | 246,819,476 |
| Internal base warning budget | 190,000,000 — **PASS** | 190,000,000 — **PASS** |

The verified local input is the **neutral disposable-fixture AAB** from package
1, application commit `c147947a`, not an operator-signed Play release. The report
records clean measurement provenance, input hash and unchanged source bundle.
Marginal contributions also measured by bundletool: speech 182,033,094 bytes,
music 43,431,958, graphics 22,103,106, engine/Android code 26,117,001, other including
fonts/metadata 1,050,726. They are **not additive**: diagnostic APK sets omit one
category with surviving compressed entries copied verbatim, then rerun get-size.
These unsigned/non-installable sets are discarded; no media is re-encoded, no
source AAB changed, and no signing key is used/created. The generated CI-summary
Markdown matched the retained report exactly.

- **PASS:** complete public `tests/run.sh`, **189 Python tests**, 12,750 quest /
  4,168 world / 1,231 reward checks, 62 avatar import/privacy/restart checks and
  existing layout, speech, lifecycle, fresh-import and content/QA guards.
- **PASS:** 11 size regressions: raw numeric CSV, classification, exact compressed
  bytes/CRC and streaming-descriptor preservation, APK-set targeting metadata,
  neutral-only inputs, source immutability, signing-secret isolation and the
  warning path completing successfully above budget. Oversized data in this
  orchestration test is explicitly a tool fixture, not a measured large bundle.
- **PASS:** actionlint, local documentation/CI references and `git diff --check`.
- [Neutral CI run 40113455357](https://github.com/sayac007/Kinderwelt/actions/runs/40113455357):
  **PASS** at `c4bdb9b9`: actual neutral APK/unsigned AAB rebuilt and verified,
  real bundletool measurement completed and reports uploaded in
  [android-development-artifacts](https://github.com/sayac007/Kinderwelt/actions/runs/40113455357).
  Numeric CI annotations independently expose the measured values without
  depending on an artifact download. CI marginals: speech 182,033,105 bytes, music
  43,431,860, graphics 22,103,156, engine/Android code 26,117,026, other 1,051,098.
  The small local/CI difference reflects different fixture/preview builds; these
  are separately labelled results, not an assertion of byte-identical bundles.

Google's official limits were checked separately: base **500 MB**, individual
asset pack **1.5 GB**, cumulative modules/install-time packs **4 GB**. The 190 MB
budget is internal. Play Console's similar but non-identical size calculation,
other device profiles, protected real-key release signing, reviewer protection,
Play acceptance and hardware remain **NOT VERIFIED**. All three speech languages
remain included. No per-run report or hash inventory was added to `docs/qa/`.

## Play preparation: package 1 (0.9.4 / 17)

Verified code commit: `c147947a13bea587076bcfbfad581ec050637856`, 2026-10-24.
[Release configuration and operator setup](android.md) describe the separate,
neutral-only upload-signing path. `project.godot` is the single version source;
the original development workflow and all learning/audio/art files are unchanged.

- **PASS:** complete `tests/run.sh` with `KINDERWELT_VARIANT=public`, including
  **177 Python tests**, all 12,750 quest / 4,168 world / 1,231 reward checks,
  62 avatar import/restart/privacy checks, layout, speech, lifecycle, fresh-import,
  pronunciation, licence, documentation and pedagogical regression guards.
- **PASS:** 15 release/signing regressions: missing/provisional identity, missing
  credentials/operator placeholders, both preset versions, credential isolation,
  private temporary keystore cleanup, and the actual CI preflight shell block
  skipping without secrets. Real JDK signature tests reject unsigned, modified,
  partly unsigned and wrong-signer archives. Test identities are disposable only.
- **PASS:** actual neutral release AAB exported and signed using an isolated,
  disposable acceptance key (destroyed afterward), then technically verified.
  `build/android-play-package1-verified/kinderwelt-release-neutral.aab`:
  **306,194,336 bytes**, **7,922 signed payload entries**;
  `invalid.kinderwelt.fixture`, 0.9.4 / 17, zero permissions, backup disabled,
  expected signer, manifest/content, ABI and 16-KB ELF checks passed. Provenance:
  `source_dirty=false`, `git_state_changed_during_build=false` at the commit above.
  This is a **test fixture, not an operator-signed Play delivery**.
- **PASS:** actionlint, both workflow YAML parses, local documentation/CI
  references and `git diff --check`. The production `android.yml` is byte-identical
  to the base. The new release workflow has only manual dispatch and read-only
  contents access; it never receives a family token or checks out private assets.
- Neutral debug/unsigned-AAB [CI verification run 40110051611](https://github.com/sayac007/Kinderwelt/actions/runs/40110051611):
  **PASS** at the verified code commit: actual neutral debug APK and unsigned AAB
  built, verified and uploaded as `android-development-artifacts`. An earlier own run was cancelled
  after a local reproduction exposed Java stderr notices corrupting XML parsing;
  the corrected checker captures stdout separately and has a regression.

**NOT VERIFIED:** signing with the operator's actual upload key, final package,
publisher/contact/licence choices, Play upload and all existing device/manual
acceptance. GitHub returned 404 when dispatching the newly added release workflow
before it existed on the default branch. After the operator merged #23,
[live run 40112054573](https://github.com/sayac007/Kinderwelt/actions/runs/40112054573)
completed successfully: configuration check passed, signing/build/upload steps
were visibly skipped. The safety input retained the invalid package placeholder,
so an unexpectedly configured job could not have signed a bundle.
Environment protection settings and real signing remain unverified.
Packages 2–6 are separate follow-up PRs, not covered by these results. No real
upload key, contact information, Play approval or new QA run files were added.

### Release guard follow-up

The review of merged #23 found no tracked keystores/certificates, private-key PEM
blocks or added long Base64 blocks. Its fixed disposable test passwords matched
none of the retained run logs; their key directories were gone. The follow-up
replaces those test passwords with runtime-random values, limits the release job
to manual `main`, references Environment `release` and adds tested `always()`
cleanup below `RUNNER_TEMP/kinderwelt-release`. **16 targeted signing/guard tests,
actionlint and local documentation checks passed.** Gameplay is unchanged.
[Non-main live dispatch 40112335611](https://github.com/sayac007/Kinderwelt/actions/runs/40112335611)
skipped the entire job before Environment access, as intended.
Required reviewers, main-only Environment deployment policy and Environment-scoped
secrets must be configured and verified by the operator; the metadata API returned
404, so protection is **NOT VERIFIED**, not asserted from YAML alone.

## Current avatar-import verification (0.9.4)

Application commit `8eaf9968` adds an optional parent-managed, device-local PNG
figure; [implementation and privacy boundaries](AVATAR_IMPORT_FEASIBILITY.md).
The previous 0.9.3 tables below remain historical evidence, not newly built files.

- Complete existing suite passed with `KINDERWELT_VARIANT=family`: **162 Python
  tests**, 12,750 quest checks, 4,168 world checks, 1,231 reward checks, save/restart,
  14,400 heading and 99,756 letter-layout checks, speech/sequence/world audio and
  66 lifecycle checks. All 3,803 speech files decoded; pedagogy guards passed.
- **62 new Godot import/privacy checks** passed across two app processes:
  transparency/bounds, parent-only mutation controls, failed replacement,
  point preservation, seven sceneries, restart, metadata stripping and reset.
- **681 existing real render frames** passed the existing verifier; **18 extra
  synthetic-avatar frames** were generated for DE/EN/RU in both orientations.
  Two new preview/help frames were locally inspected; no claim is made that every
  generated frame received independent manual review.
- Synthetic EXIF-GPS/camera fixture identity and actual stored-pixel re-encoding
  were checked. Three backup-policy regressions passed, including a real local
  aapt2 compile/link and verification of compiled exclusions/manifest references.
- [Initial Android run 40102432351](https://github.com/sayac007/Kinderwelt/actions/runs/40102432351)
  failed verification and is **not** an installable delivery. Log downloads were
  blocked here, so the exact code was reproduced locally: Godot regenerated
  `src/debug`/`src/release` manifests, dropping the backup-resource references.
  The strict checker caught this; it was not weakened. The fix puts references
  in the retained `src/main/AndroidManifest.xml` and tests build-type rewrites.
- A corrected local family APK **and** unsigned AAB were then actually built and
  verified: version 0.9.4 / 17, zero permissions, backup disabled, v2 development
  signature for APK, 16-KB ZIP/ELF alignment, resource/content checks and compiled
  cloud/device-transfer exclusions with correct manifest references. Local APK:
  **323,927,586 bytes**, SHA-256
  `dcbd1521e0ca6bf25d2aefd2c72a296085f58d6376697a7a89b973b7dd09bb45`.
  This was a dirty-worktree reproduction with the uncommitted fix, not claimed
  as clean immutable provenance. The fresh [CI run 40105564671](https://github.com/sayac007/Kinderwelt/actions/runs/40105564671)
  then **succeeded** at fix commit `f892418ac23a4d79a3e442082fd92c5c5117f343`.
  Its single family-only artifact/download is recorded in [Android](android.md).
  All **162 Python tests** were also repeated successfully after the backup fix.
  No permission or release key was added.

A local extra test was initially started while the render script regenerated the
shared import cache. That concurrent probe was stopped and repeated sequentially:
both import phases passed without script errors. The reproducible suite already
orders imports and tests. An earlier character-target layout failure was fixed by
keeping the original grid size and putting Help in the header.

Native Android picker/URI access, lifecycle and actual backup/restore remain
manual device checks. The parents screen is a navigation boundary, not an age
verification or Google Play/Families certification. New raw logs/renders remain
outside Git.

## Orientierung

| Bereich | Inhalt / zuständige Komponenten |
|---|---|
| Lernen | Je **50 Stationen** in Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch und Geografie; DE/EN/RU mit eigenem nativem Sprachwortschatz. Jede Station: zehn Punkte und freiwillige Boni mit 50/100 Punkten. |
| App | `core/quest/main.tscn`, `core/quest/` und `games/quest/`: Oberfläche, Weltbewegung, Aufgaben, Audio und lokaler Spielstand. Sieben Figuren, fünf Looks, sieben Kulissen, 20 klassische Klavierwiedergaben. |
| Redaktion | `scripts/content/generate.py` kompiliert TSV-/JSON-Quellen mit `advanced.py`, `experience.py` und `pedagogy.py`. [Quellen, Regeln und Ablauf](CONTENT_AUTHORING.md). |
| Sprache | Fertige Vorbisclips: weibliche Serena DE/RU und LJSpeech EN. Lexikalische Betonungsreferenzen, Syntheseprovenienz und ASR-Regressionsdaten. [Verfahren und Hörgrenzen](voice.md). |
| Medien / Android | [Musik](music.md), [Figurenherkunft](character-origins.md), [Build und Paketprüfung](android.md). Familien- und neutrale Variante mit gleicher Spiellogik; private Figuren separat. |
| Menschliche Abnahme | [Hörpaket, Geräteprotokolle, Fachprüfung und Evaluation](ACCEPTANCE.md). [Offene Play-Entscheidungen und Entwürfe](PLAY_READINESS.md). |

## Ausführen

Dieselben Befehle wie im [README](../README.md); Godot 4.7.2, Python 3 und FFmpeg erforderlich:

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Für Bildprüfungen ein neues Ausgabeverzeichnis wählen. CI führt beide Suiten aus und erzeugt separat `kinderwelt-full-listening-review`. Laufzeitberichte liegen unter `qa-results/`, Pakete unter `build/`; CI-Artefakte laufen nach sieben Tagen ab. Tests und Hörpaket benötigen keine privaten Familien-Assets, Tokens oder Sprachmodelle.

## Aktueller Prüfstand — 0.9.3 / Code 16

**24.10.2026. Verifizierter Anwendungscommit: `bace67364a334a592c8fe74f4953f1c5074027ca`.** Die lokalen Android-Builds bestätigen diesen sauberen Commit (`source_dirty: false`). Spätere Änderungen dieses Überblicks betreffen die Anwendung nicht. GitHub baut separat; Status und Downloads im jeweiligen [Actionslauf](https://github.com/sayac007/Kinderwelt/actions/workflows/android.yml). Ein lokaler Erfolg beweist keinen erfolgreichen Remote-Lauf.

| Dimension | Tatsächlich verifiziert / verbleibende Grenze |
|---|---|
| Vollständige Suite | **135 Python-Tests bestanden**; die vollständige `tests/run.sh`-Suite wurde nach der Fixturekorrektur nochmals erfolgreich ausgeführt. 12.750 Aufgaben-, 4.168 Welten- und 1.231 Punkteprüfungen bestanden. Generator reproduziert Inhaltsdateien ohne Diff. Alle 1.200 Aufgaben-IDs, richtigen Antwortwerte und Belohnungen gegenüber `main` erhalten. |
| Inhaltskorrekturen | Beide Helm-Bildlücken geschlossen: Fahrradhelm versus original KI-generierte Kappe/Wollmütze; sichtbare echte Bilder und lokalisierte Namen. Herkunft/Hashes in `art/public/headgear.json`. 30 separat formulierte Sachgegenbeispiele sichern u.a. Achsen, Pilze, Puppenstadien, Stoffeigenschaften und Organe ab. Kategorienprüfung meldet keine offenen Bildwarnungen; unabhängige Sach-/Altersprüfung bleibt erforderlich. |
| Oberfläche | **681 tatsächliche Renderbilder** in vier Displayprofilen; 99.756 Prüfungen über 1.800 Wortansichten und 14.400 Schriftmessungen ohne Überlauf bestanden. Neue Helmaufgabe auf kleinem Display manuell angesehen. Kein vollständiger manueller Bild-/Gerätetest. |
| Punkte / Start | 64.000 aktuelle Punkte, mit alten Belohnungen maximal 67.200. Separater Neustart stellt **3.470 Testpunkte** wieder her, ohne doppelte Belohnung. Frischer Import/Start aus ausgelieferten Dateien und isolierter Familienstart mit 60 echten Frames bestanden. |
| Unterbrechung | Konkreter Fehler behoben: Belohnungstöne pausieren jetzt wie Sprache/Musik beim Hintergrundwechsel. Neuer Test mit **66 echten Godot-Prüfungen**: Pause/Fortsetzung, ausstehendes Lob, gehaltene Geste, gespeicherte Punkte/Kulisse und fünf Drehungen einer offenen Aufgabe. Desktop-Notifications/Resize, keine Android-Hardware- oder Audiofokus-Zertifizierung. |
| Audio / Technik | **Alle 3.803 tatsächlichen Ogg-Dateien decodiert**, 7.281 aktuelle Text-/ID-Bindungen und Dateihashes geprüft. 36 Wiedergabe-, 75 Sequenz- und 38 Weltsprachprüfungen bestanden. Alle 44 geänderten Aufnahmen zusätzlich mit gepinntem CI-FFmpeg decodiert; Dauer/Pegel bestanden. Vollständige Wellenformen und Randstille, Modell-/Lizenznachweise erhalten. |
| Aussprache | Dieselben Frauenstimmen; 44 Aufnahmen gezielt überarbeitet: vier DE- und zehn EN-Stationen einschließlich Boni, zwei RU-Grundfragen. Bei allen 50 nativen Wortfragen je Sprache gewinnt ASR **39/50 DE, 41/50 EN, 44/50 RU** Zielschreibweisen zurück (vorher 35/31/42). Alle 28 geänderten DE-/EN-Bonusfragen vollständig erkannt. Originale Probeparameter und genaue Eingänge bleiben nachgewiesen. ASR-gestützte Auswahl ist kein unabhängiger menschlicher Verständlichkeits- oder Betonungsnachweis; nicht erkannte Wörter bleiben sichtbar. |
| Vollständige Hörabnahme | Offlinepaket mit allen **3.803 unterschiedlichen Aufnahmen / 7.281 Verwendungen** tatsächlich erzeugt; aktuelle Hashes geprüft und JavaScript-Syntax validiert. Prüferklärungen können lokal exportiert/fortgesetzt werden; stale, doppelte oder um persönliche Felder erweiterte Belege werden abgelehnt. Ein leerer Beleg führt tatsächlich zu `INCOMPLETE` / Exit 2. **Keine menschlichen Freigaben eingeholt**, keine vollständige Browser-/Hörabnahme behauptet. |
| Android | **Beide APKs und beide unsignierten AABs tatsächlich gebaut und technisch bestanden.** Familie 7.801, neutral 7.791 geprüfte Ressourcen. Paket/Version, API 24–36, `arm64-v8a`/`x86_64`, ZIP-/ELF-16-KB-Ausrichtung, Launcherbilder und Inhaltsintegrität geprüft. APKs mit bestehender Entwicklungsidentität (v2), AABs unsigniert; Play weiterhin gesperrt. |
| Datenschutz / Herkunft | Begrenzter Quell-/Konfigurationsaudit: keine Netzwerk-/Konten-/Werbeintegration, keine Android-Berechtigungen, Backup deaktiviert. Private Figurenquellen und Android-/Qwen-Workflows unverändert. Quality-Workflow veröffentlicht nur ein separates Hörpaket ohne Familienbilder oder Zugangsdaten. Keine personenbezogenen Testdaten erhoben; keine umfassende Sicherheits-/Rechtszertifizierung. |
| Dokumentation | Alle lokalen Dokumentationsziele und CI-Dateireferenzen geprüft; Details im Laufprotokoll. Alle drei Workflow-YAMLs syntaktisch geparst. `docs/qa/` unverändert zwei Referenzdateien / 78.669 Bytes; 139 historische Originaldateien weiterhin verifiziert. Allgemeine externe HTTP-Erreichbarkeit wird nicht pauschal zertifiziert. |

Die vollständige Suite fand zunächst eine veraltete positive Android-Testfixture: Sie führte die neuen Mützenressourcen noch nicht auf. Die Fixture wurde um Import- **und** Texturdateien ergänzt; die strengere Paketprüfung bleibt erhalten. Ihre 17 Prüfungen bestanden anschließend; die vollständige Suite wurde danach mit allen 135 Python-Tests und sämtlichen Godot-/Qualitätsgates erfolgreich wiederholt.

Lokale Nachweise: `qa-results/qa-v093-full-suite-final.log`, `qa-results/visual-v093-acceptance/`, `qa-results/qa-lifecycle-before.log`/`qa-lifecycle-after.log`, `qa-results/qa-final-native-words.json`, `qa-results/qa-final-native-ru.json`, `qa-results/qa-bonus-clarity-*.json`, `qa-results/qa-documentation-final.log`, `build/listening-acceptance-v093/` und `build/android-v093-acceptance/delivery.json` samt Varianten-Provenienz/Verifikation. Die notwendigen [Worterkennungsreferenzen](../tests/fixtures/voice/subject-recognition.json) und [Bonusreferenzen](../tests/fixtures/voice/carrier-recognition.json) bewahren gemessene Transkripte und Audiohashes im Git. Keine neuen Rohlogs eingecheckt.

### Tatsächlich erzeugte lokale Dateien

APK-Zertifikat wie beim lokalen 0.9.2-Vorgänger: SHA-256 `3444a17df292f9c04a47059082669d28e67bb16014c81bdfa0910d01f0389c15`. Stabile Testpakete `.preview.family.v090` / `.preview.neutral.v090` bleiben erhalten. Das ist eine technische Updatevoraussetzung; ein echtes Android-Update wurde hier nicht ausgeführt. Bei Zertifikatsabweichung nicht deinstallieren, wenn Punkte erhalten bleiben sollen.

Unter `build/android-v093-acceptance/`:

| Datei | Bytes | SHA-256 |
|---|---:|---|
| `kinderwelt-debug-family.apk` | 323,910,788 | `af98141960b91713ddebfae24ae03ac784d3ce8e0b6d4fde63a45cbb7c345296` |
| `kinderwelt-unsigned-family.aab` | 309,995,434 | `257ea05aa2c4644285440eb73d2a9459ae678c6479463866681e41c68cb64c7d` |
| `kinderwelt-debug-neutral.apk` | 319,039,837 | `0398d35fabc7113d4e97898218d13a53fdf097f1b70a3eabbcb430d0b7afbf6e` |
| `kinderwelt-unsigned-neutral.aab` | 305,132,045 | `44dfd3fdd81daa8574e091e54b907c0f9b117973aa143eabec1e4d19aafbcedb` |


Das kompakte `kinderwelt-listening.html` mit 262 echten Hörfolgen liegt der Android-Ausgabe bei. Das vollständige Hörpaket wird separat in Quality-Actions veröffentlicht; ZIP entpacken, `index.html` öffnen. Beide Pakete sind Prüfhilfen, keine erfolgte Hörfreigabe.

## Noch erforderliche menschliche Freigaben

- **Muttersprachliches Hören:** alle Aufnahmen, insbesondere verbleibende Wortfragen, Betonung, interne Zahlwortverbalisation und Fachbegriffe; reale Lautsprecher/Kopfhörer und Musikbalance.
- **Android-Geräte:** Rotation, Touch, Audiofokus, Unterbrechungen, Prozessneustart und echtes Update mit gespeichertem Spielstand. Hier kein nutzbares angeschlossenes Android-Gerät oder eingerichteter Emulator; `/dev/kvm` fehlt. ADB konnte in dieser Sandbox sein unveränderliches Standard-Konfigurationsverzeichnis nicht anlegen. Keine Geräteprüfung als ausgeführt markiert.
- **Unabhängige fachpädagogische Prüfung und Kinderbeobachtung:** konkrete Unterrichtsmodelle, Mehrdeutigkeiten, Lesebelastung und Schwierigkeitsniveau. Entwicklerdurchsicht, Merkmalszählung und konsistente Antworten beweisen keine Lernwirkung. Mehrere externe Fachquellen waren mit HTTP 403 gesperrt; kein erfolgter Quellenabgleich behauptet.
- **Betreiber / Play:** endgültige Paketkennung, Herausgeber/Kontakt, Datenschutzerklärung, Zielgruppen-/Altersangaben, Medienrechte, Store-Eintrag, Release-Signierung und aktuelle Console-Vorgaben. Entscheidungsvorlagen und sichere Einrichtungshinweise vorbereitet; keine Schlüssel erzeugt oder Freigaben geändert.

[Praktische Protokolle und wissenschaftlicher Evaluationsplan](ACCEPTANCE.md) · [Play-Voraussetzungen und Entwürfe](PLAY_READINESS.md). Personenbezogene Kinder-/Forschungsdaten erst nach gesonderter Entscheidung und Schutzkonzept erheben. Aktuell keine Kinderaufnahmen oder Telemetrie; empirische Lernwirkungen nicht nachgewiesen.

## Historische Nachweise und Dokumentationsregeln

Die [vollständige 0.9.2-Prüfübersicht](https://github.com/sayac007/Kinderwelt/blob/4e81e4b34817f4f609ab11c0a73e1824911b3f5b/docs/QUALITY_ASSURANCE.md) enthält die damaligen APK-/AAB-Hashes, 129 Python-Tests und sämtliche Decoder-/Aussprachebefunde. Diese Angaben sind historisch, keine neuen Builds.

[Archiv und Inventar](qa/README.md): **139 unveränderte Originaldateien / 7.383.943 Bytes** bleiben im geprüften Git-Archiv unter Tag `qa-evidence/2026-10-23-v091`, Commit `a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`, dauerhaft erhalten. `docs/qa/` weiterhin zwei Referenzdateien / 78.669 Bytes. Keine historischen QA-Dokumente gelöscht oder privaten Assets veröffentlicht.

Im Git nur aktuellen Überblick, Anleitungen, bekannte Grenzen und notwendige langfristige Referenzen pflegen. **Keine neuen Einzelberichte je Testlauf.** Neue Logs/JSONs nach `qa-results/` oder `build/`. Langfristige Freigaben brauchen verifizierte Ablage mit Commit, Datum, Dateinamen und Hashes; Originale erst nach verifizierter Ersatzablage entfernen. CI-Artefakte laufen ab und sind kein dauerhaftes Freigabearchiv. `documentation.py` prüft lokale Links, Archivindex und CI-Dateireferenzen; README und Überblick nennen dieselben Testkommandos.
