# IARC and child audience — operator-review worksheet

**Draft; no rating assigned or submitted.** Use the current
[Play rating guidance](https://support.google.com/googleplay/android-developer/answer/9859655?hl=en)
and [Families policy](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en).
The actual IARC form and regional results are controlled by Play/the operator.
Technical tests cannot decide a rating or certify appropriateness for every child.

| Topic / proposed direction | Basis and required decision |
|---|---|
| Intended audience: early primary school; choose actual child age groups | [Project overview](../../README.md), [content and layout tests](../../tests/quest.gd), [manual adult/child protocol](../ACCEPTANCE.md). Operator chooses ages; no automated educational-effect claim. |
| Violence/fear | [Seven scene definitions](../../core/quest/scenery.gd), [ghost/world props](../../games/quest/world_props.gd), [hero rendering](../../core/quest/hero.gd). Friendly floating ghosts appear in a castle. **Manually inspect** artwork/animations and decide the exact fear/violence answers; do not assume “none” from test success. |
| Sexual content, substances, gambling, offensive language | [Task registry](../../games/quest/tasks.json), [localized text](../../games/quest/languages.json), [pedagogy regression](../../scripts/qa/pedagogy.py). No such game mechanic is intended. Operator must review actual pictures, three-language audio and wording before answering. |
| User interaction/content sharing: no app communication or public content feed | [Device-local image controls](../../core/quest/avatar_import.gd), [no-network path guard](../../tests/android/test_avatar_privacy.py), [zero-permission verifier](../../scripts/android/verify.py). Adults may import their own local picture; it is not submitted to others. Disclose that local feature accurately if the form asks. |
| Purchases/advertising: no app feature implemented | [Architecture/content audit](../../scripts/qa/audit.py), [Android export checks](../../scripts/android/verify.py). Operator checks final dependencies/build; no ad identifier or payment permission is requested. |
| Personal information / location | [Data Safety worksheet](data-safety.md), [private save whitelist](../../core/save_store.gd), [GPS-removal regressions](../../tests/avatar_crop.gd). Local picture handling remains personal-image processing even without transmission. |
| Hardware suitability, clarity and learning content | [Acceptance protocol](../ACCEPTANCE.md). Full native-language listening, independent pedagogy and Android-device checks remain **NOT VERIFIED**; automated checks are not empirical learning evidence. |

Before submission the operator must approve publisher/contact/privacy URL, asset
rights, audience, final listing/screenshots, actual content and the generated
rating. Keep the family build and source photos out of Store materials. No Google
Play setting, legal approval or release-signing decision is made by this worksheet.
