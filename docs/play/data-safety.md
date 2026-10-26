# Data Safety — proposed answers for operator review

**Draft, not submitted.** Recheck the final neutral signed build and the current
[Google definition of collection](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en).
Google describes collection as transmitting data from the app off the device;
local processing alone is distinct. The optional photo can be personal data
while being processed locally. Do not claim that the app never handles an image
of a person. This draft concerns app behaviour, not Play/OS/provider processing
or voluntary support correspondence. No Console declarations were changed.

| Proposed answer / scope | Source and evidence |
|---|---|
| App collects/shares user data off device: **No, proposed**, subject to final build review | No app network path; [import dependency guards](../../tests/android/test_avatar_privacy.py), [content/architecture audit](../../scripts/qa/audit.py), [zero-permission compiled manifest checks](../../scripts/android/verify.py). No INTERNET permission. This does not audit Google's own services. |
| Photos/videos: selected character image is **processed locally**, not collected/transmitted by the app under the definition above | [Bounded decode/orientation](../../core/quest/avatar_image.gd), [pixel-only private PNG and deletion](../../core/quest/custom_avatar.gd), [24 actual GPS/camera fixtures and crop tests](../../tests/avatar_crop.gd). Source URI/original are not retained by the importer. No camera, upload, sharing or gallery export. |
| Device location: **not collected**; source GPS metadata is discarded | [Structured EXIF fixture test](../../tests/android/test_avatar_privacy.py), [runtime metadata-removal test](../../tests/avatar_crop.gd). Synthetic location 0°N/0°E is fixture data under tests, excluded from app packaging. |
| Personal identifiers, accounts, contacts, financial/health data, messages: **no collection path implemented** | [Save field whitelist](../../core/save_store.gd), [runtime import path guard](../../tests/android/test_avatar_privacy.py), [compiled zero permissions](../../scripts/android/verify.py). Human-body learning content is not a health-data collection feature. |
| App activity/diagnostics/device identifiers: **not sent**; points/preferences remain private on-device | [Save schema](../../core/save_store.gd), [restart/score tests](../../tests/save_restart.gd), [lifecycle tests](../../tests/qa/lifecycle.gd). No analytics or automated crash-upload SDK is integrated. |
| App backup/device transfer: excluded, **physical restore test NOT VERIFIED** | [Backup rules](../../scripts/android/backup_policy.py), [compiled rule assertions and negative regressions](../../tests/android/test_verification.py). The original gallery/provider/cloud image is outside the app's control. |
| Deletion: adults can remove the image, confirm reset, or uninstall | [Parent flow and confirmation](../../core/quest/main.gd), [remove/reset runtime tests](../../tests/avatar_import.gd), [crop/reset tests](../../tests/avatar_crop.gd). No account deletion is required because no app accounts exist. |
| Encryption in transit / mandatory collection questions | Operator to follow current form branching for an app with no off-device collection; do not invent a transport protocol or select answers blindly. Evidence: no network path above. |

**Operator decisions:** {{HERAUSGEBER}}, {{SUPPORT_EMAIL}}, public
{{DATENSCHUTZ_URL}}, applicable legal bases and separate support retention,
final package/SDK inventory, target ages and privacy publication. The three
[privacy drafts](../privacy/privacy.en.md) are not published or legally approved.
Android 13+ and 10–12 system picker/backup acceptance remains under
[ACCEPTANCE](../ACCEPTANCE.md). Rights and actual spoken clarity also remain
separate acceptance decisions. No personal test photos should enter reports.
