# Google Play release gates — BLOCKED

Prepared 2026-10-20. No publication, upload authorization, legal approval, device
certification or demonstrated learning effect is implied. Technical test results
are in release-report.md; previous pedagogical hypotheses remain hypotheses.

| Gate | Current state / required owner action |
|---|---|
| Identity | BLOCKED: replace `org.example.kinderwelt` with an owner-approved permanent package ID; update verifier and both presets together. Confirm name/rights and versionCode sequence. |
| Signing | BLOCKED: no upload/release key supplied. Establish owner-controlled upload keystore, backup, protected secret injection and Play App Signing; verify certificate fingerprint. No private keys in Git or build archives. |
| Target API | BLOCKED for release: build targets API 36, min 24. Verify current mobile-app requirements and deadlines against official Play guidance at release time. API 36 is an engine/toolchain selection, not proof of current policy compliance. |
| 16 KB / native compatibility | ZIP/ELF checks automated; test actual AAB-generated APKs on a 16 KB-page Android device/emulator and required Android versions. No device result yet. |
| Privacy | Owner/legal review of privacy-policy-draft.md, real controller/contact and public HTTPS policy URL; match app and Play Console declarations. No fabricated contact or hosted policy. |
| Data safety | Review each category in privacy draft for the actual final binary and all SDKs. Local progress is retained on device; no telemetry, ads, account or purchases added. Do not auto-submit “no data” solely from a source scan. |
| Target audience / Families | Select actual intended age groups and declare child-directed content truthfully. Review Families requirements, SDK inventory, permitted content and audience settings. No ads are implemented. An adult discussion option is voluntary, not a parental consent mechanism. |
| Age rating | Owner completes current IARC/content rating questionnaire; do not invent a rating. Describe social scenarios and all content truthfully. |
| Store assets | Review German listing and original icon; replace desktop UI draft screenshots with actual release-device captures. Prepare/review required feature graphic (1024×500), phone/tablet captures, metadata and any currently required promotional assets. No placeholder graphic should be uploaded as final. |
| Listing / legal | Owner confirms developer identity, contact, ownership, distribution countries, support, privacy URL, category, pricing and accessibility descriptions. No unsupported learning claims. |
| Account / testing | Confirm developer account verification and any account-specific internal/closed testing, tester count/duration and production-access requirements in Play Console. Not inferred or performed. |
| Devices | Execute the protocol below; verify delivered split APKs rather than only a desktop view or universal debug APK. |
| Approval / upload | Separate explicit owner approval and Play Console access needed. This pipeline does not upload. Final signed bundle hash and certificate must be reviewed before any upload. |

## Manual device protocol — NOT RUN

Use synthetic progress only; no child data, recordings or account names. Record
only device model/OS/API/page size, build SHA256 and technical results. Install
APK with adb from a writable developer environment, launch offline and visit all
36 tasks. Solve each, request hints, undo, mute, reduce motion, use back and return
to hub. Confirm visible touch feedback, scroll reachability, audio volume and
icons. Check TalkBack/switch/keyboard accessibility with a human reviewer; no
accessibility certification is claimed.

Repeat representative paths in portrait and landscape, rotate while selecting,
during hints, after completion, and after background/resume. Check safe areas,
cutouts, gesture navigation and Android edge-to-edge behavior; confirm no lost
input or inaccessible controls. `fullUser` deliberately permits both axes while respecting the user’s rotation lock; OS
and hardware can impose their own orientation rules.

Kill/relaunch: progress/settings persist. Reset: local progress clears. Check
uninstall/reinstall expectations, updates signed by the same key, storage
failures and app data backup disabled. Test min API 24, target API 36, a modern
physical phone, tablet, arm64 and (where supported) x86_64/emulator, including
16 KB page-size configuration. Measure actual startup, frame behavior, memory,
battery and audio; no measurements are currently available.

Generate/install AAB split APKs using a real owner-controlled test identity or
Play internal testing, verify certificate/package/version and repeat offline
startup, content loading and rotation. Any child usability/effect evaluation is
a separate consented study under the existing quality protocols.

## Official sources to recheck at release

- https://developer.android.com/google/play/requirements/target-sdk
- https://support.google.com/googleplay/android-developer/answer/11926878
- https://support.google.com/googleplay/android-developer/answer/9893335 (Families)
- https://support.google.com/googleplay/android-developer/answer/10787469 (Data safety)
- https://support.google.com/googleplay/android-developer/answer/9859655 (ratings)
- https://developer.android.com/guide/practices/page-sizes
- https://support.google.com/googleplay/android-developer/answer/1078870 (assets)

These references are review destinations, not a claim that their current contents
were fully verified. On 2026-10-20 the target-SDK developer.android.com page and
Play target-API help page returned HTTP 403 in this cloud environment. Current
Play requirements must therefore be verified externally before release.
