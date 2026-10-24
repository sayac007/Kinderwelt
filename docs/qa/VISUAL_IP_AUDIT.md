# Visual asset IP and similarity audit

**Date:** 2026-10-24. **Application inventory snapshot:**
`352da6fc3be885e565267fabc47b28ad709cd4d1` (merged PR #17).
Original audit: merged PR #18. **Owner-review/C2PA follow-up base:**
`2d69117ed7b15d94319c17bbae9764cc39290513`, branch
`audit/visual-ip-owner-review`. Repository visibility was checked: **private**.

This is an inventory and bounded local risk screen, **not legal clearance**.
A generation claim, a matching local output, a lack of search hits or a generic
visual style does not establish originality or the right to distribute an image.
The assistant made no online reverse-image search or external image/vision
submission. The owner's subsequently supplied manual findings are recorded below.
No game/source visual, mechanics, voice/music, signing, Android workflow or
family-access configuration was changed. Review crops are local derivatives.
New audit material is English; existing product translations are preserved.

## Inventory and coverage

The [redacted manifest](visual-ip-manifest.json) records individual unique
visual files, exact duplicate occurrences, dimensions/formats, source evidence,
references, import/derivative relationships, frame rectangles, native drawable definitions, risk dimensions,
privacy classification and review status. Sensitive paths, image hashes,
coordinates and local locators are retained only in the owner-only inventory.
Opaque private IDs use a local persistent map rather than private hash prefixes.
Counts below retain the original inventory snapshot. This bounded follow-up
adds evidence for its existing records; it is not a new full-workspace scan.

| Scope | Measured count |
|---|---:|
| Current workspace files inspected by signature | 123,377 |
| Unique visual files/resources across all retained inputs | 4,785 |
| Exact-byte occurrences, including packages and Git aliases | 11,007 |
| Current project source assets across both cast variants | 33 |
| Logical atlas/sprite frames with source-matched metadata | 174 |
| Locally screened frames in current non-sensitive atlases | 116 |
| Visual-path Git blobs across all local refs, complete non-shallow history | 209 |
| Readable outer/nested source/Office/build/export-template containers | 75 |
| Procedural graphics/UI source files | 11 |

The workspace count includes thousands of old screenshots, test renders,
compiled textures, fonts, native drawable definitions and repeated build inputs. It is **not** the number of
illustrations in the current app. PNG/JPEG/WebP/GIF/SVG/ICO, Godot textures,
font resources, misnamed files, embedded source SVG and container members are
handled. Seven nested ZIP/JAR/AAR containers were recursively inspected without extraction (bounded depth/size); their visual members are included. Exact hashes deduplicate files; normalized thumbnail/pixel groups and
source-declared crops relate variants without treating them as new licenses.
Historical wardrobe metadata is used only for its exact source image SHA.
Procedural props, ghosts, UI shapes and rigged body/leg transforms are code
relationships, not independently licensed image sources.

**Visual-review coverage:** 19 source/atlas images received assistant local
visual triage, six SVG sources received geometry inspection and two Nunito
source/import records received license-metadata inspection. **4,758 unique
records were not independently visually examined.** In particular, family
images and unclassified retained material were not sent to vision services.
Whole-atlas inspection is distinguished from an individual reverse-image search.

## Risk assessment

| Overall triage tier | Records |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 111 |
| Low | 8 |
| Unreviewed | 4,666 |

Tiers are provisional. The manifest separates recognizable resemblance,
provenance/license adequacy, distribution exposure and private sensitivity.
Unreviewed is **not** low risk. A low resemblance screen is not a rights grant.
The difference between review-status and overall-risk counts is intentional:
some sources have technical provenance evidence but no independent visual review.

### Concrete findings

1. **No specific franchise character/logo was identified in the locally
   screened current project illustrations.** Their large eyes, colorful costumes,
   stars, planets and plush rendering are not by themselves evidence of copying.
   No claim is made about every retained screenshot or all possible prior art.
2. **Correction: all four legacy PNGs contain embedded C2PA credentials.**
   The first audit incorrectly stated that their metadata contained no
   provider/authorship attestation. Reading Pillow's ordinary image-info fields
   missed their `caBX`/JUMBF content. The original Git bytes and retained outputs
   match by SHA-256; both contain creation claims for ChatGPT / gpt-image on
   2026-10-20. Those claims have **not** been cryptographically authenticated.
   Original prompts, reference rights and applicable grants are not established
   by a filename or an unauthenticated credential. They remain excluded from
   current runtime, with **medium** provenance priority.

| Non-sensitive legacy asset ID | Exact retained output filename |
|---|---|
| `image-26cd7dab38602ae98834` | `exec-c84720a3-0e2c-4434-ad7c-d9264e8abae2.png` |
| `image-317a7d58430e3f9c88b1` | `exec-2e9c9a6d-7bda-4c43-945d-a0d86d7243fb.png` |
| `image-35a7192d211191ede087` | `exec-9f485dfe-5766-4fdf-9a7a-ec04aa40e23b.png` |
| `image-a0fb2eaf69eea145a82b` | `exec-c5159b37-464c-4659-bfb2-5e319db6bfc0.png` |

3. **Current generation records are evidence anchors, not authenticated rights
   records.** For example, the app-icon source/runtime hashes and resized pixels
   match the retained originals recorded in `art/public/app-icon/generation.json`.
   Shared scenes/atlases also have local hash/pixel relationships. The root MIT
   text explicitly describes the new foundation software/documentation; an
   explicit art-inclusive licensing statement and applicable provider/reference
   terms would improve the distribution record. No incompatible art license was
   established merely from this documentation gap.
4. **Vendor/test-tool graphics are not automatically project-generated art.**
   Installed Godot export-template bytes explain native Android graphics; retained
   test-tool fonts/vectors also exist. The current Nunito OFL notice was compared
   byte-for-byte in all four current artifacts. Attribution adequacy for every
   vendor/test-tool resource remains a separate review item. The public
   [Godot-design README](https://github.com/godotengine/godot-design/blob/5a20962ba50c9ba77fc7a7cf07ba827739b39cf3/README.md)
   and license text were read on 2026-10-24; its default CC BY 4.0 declaration must
   not be applied automatically to every unrelated Android template bitmap.
5. **Privacy is a separate distribution concern.** There are 42 known
   family-derived file/texture records; 18 have retained Git occurrences.
   A further 4,624 records are conservatively restricted/unclassified, including
   many screenshots. Those counts do not mean all screenshots contain family
   members. Previously produced source-snapshot ZIPs retain screenshots whose
   sensitivity was not independently established. Keep repository/history,
   snapshots and review copies private; classify them before any public release.
   No privacy-safe public release of those unclassified images is inferred.

No confirmed unauthorized third-party artwork was established in the screened
current set. There is no evidence-based instruction to replace all current art.
Any urgent, specific match found during owner review should instead trigger a
hold on the affected distribution item and targeted rights/remediation work.

## Owner findings and Content Credentials follow-up

The [owner-review evidence ledger](../../scripts/qa/visual-ip-owner-review.json)
preserves the supplied decisions, URLs and dates, bound to all **40 delivered
candidate IDs, 18 source hashes and the exact frame rectangles**. The submitted
semicolon-separated CSV has SHA-256
`e5d3f9eae0f751374d5d01089ed1b7bf7f9927d8343377c243dd303886ca9ad5`.

- **32** entries report `no match`.
- **7** report similarities or many similar results, without a confirmed exact copy.
- **1** refers to another reviewed entry (`see rank 6`).

The `reverse_search_status` column was blank throughout. The supplied findings
are recorded as **owner-reported manual review**, not silently converted into
independently reproduced searches or verified source licenses. The linked sites
were not visited again, and no new image search was performed. Search screenshots,
exact queries and original-author/license evidence were not supplied. General
similarity and stock-search results do not establish copying or permission.

### C2PA metadata and seven derivative chains

**11 of the 18 source PNGs** contain readable `caBX`/JUMBF credentials: four
legacy figures, `science-a`, `science-b`, `objects`, `icons`, `cap`, `beanie` and
`adventure-worlds`. Their claim generator is `OpenAI Media Service API`; their
creation action names `ChatGPT` / `gpt-image` and
`trainedAlgorithmicMedia`. `OpenAI Media Service` also appears as certificate
name text; it is not being asserted as a verified certificate issuer.

The other **seven** contain no embedded manifest, but all seven match retained
originals whose credentials contain the same generation claims. Source and
derivative SHA-256 were checked against `art/character-origins.json`; actual
RGBA pixels were compared after the recorded transformation:

| Current source | Verified relationship to credentialed original |
|---|---|
| `squirrel.png` | Lanczos resize; resulting RGBA pixels identical |
| `looks-squirrel.png` | Lanczos resize; resulting RGBA pixels identical |
| `neutral-cast.png` | Lossless recompression; RGBA pixels identical |
| `home.png` | Lanczos resize; resulting RGBA pixels identical |
| `castle.png` | Lanczos resize; resulting RGBA pixels identical |
| `landscape.png` | Lanczos resize; resulting RGBA pixels identical |
| `appicon.png` | Lanczos resize; resulting RGBA pixels identical |

The ledger records full hashes, original filenames and per-file creation claims.
The [bounded local metadata reader](../../scripts/qa/visual_c2pa.py) uses no new
dependency or network client. It checks chunk CRC and reads definite-length CBOR
claim/action fields; **it does not validate C2PA signatures, certificate trust,
timestamp authorities, assertion hashes or asset binding**. CRC is not an
authenticity check. No online verifier was used.

These credentials strengthen the documented generation lineage, but do not
identify the route by which a file reached the project: an AI image downloaded
from a website can retain its original OpenAI credentials. Even an authentic
generation credential would not by itself settle reference rights, resemblance
or licensing. No additional image replacement is supported by the supplied
findings; no further image-search sweep was initiated.

### Why the legacy creation date is consistent

All four embedded creation claims are on **2026-10-20, between 18:11:35 and
18:13:57 UTC**. Their exact hashes already occur in introduction commit
`3909c4cf4e055483b746fcbd89b640b2c97e109e`, recorded at **18:34:22 UTC** that day.
They were removed in `daa0df88d472ceae9be91bc1ff50857b2ba9170a`, recorded at
**20:29:08 UTC** the same day. Each first-commit blob was re-read and matched by
SHA-256; the ledger records the individual timestamps and comparisons.

"Legacy" means the superseded cast, not an assertion that the images predate
2026-10-20. There is no discrepancy requiring newly generated replacements:
the outdated origin description is corrected in
[the provenance registry](../../art/character-origins.json). Git clocks and
embedded creation times remain recorded claims rather than trusted timestamps.
The four exclusion hashes and Android blocking rules remain unchanged.

## Android packaging comparison

Existing 0.9.3 artifacts were inspected; **no new APK/AAB was built for this audit**.
Their provenance points to clean application commit
`bace67364a334a592c8fe74f4953f1c5074027ca`.

| Existing artifact | Unique image/font resources | Unmatched image/font resources |
|---|---:|---:|
| `kinderwelt-debug-neutral.apk` | 59 | 0 |
| `kinderwelt-unsigned-neutral.aab` | 59 | 0 |
| `kinderwelt-debug-family.apk` | 70 | 0 |
| `kinderwelt-unsigned-family.aab` | 70 | 0 |

Each artifact also contains **ten compiled native drawable definitions**, separately inventoried: 80 visual records total for family, 69 for neutral. Nine APK definitions match installed template bytes exactly; one generated adaptive-icon wrapper differs. The ten AAB protobuf definitions are inventoried but their semantic equivalence is not fully decoded. Their source-level/semantic verification remains **incomplete**; zero in the table refers specifically to the image/font subset, not blanket native-resource or IP clearance. They are not ten missing game illustrations.

The comparison uses exported `.import` remaps (including stripped dependency
sections), packaged cast source hashes, exact template bytes, decoded Godot
textures and native-resolution launcher comparisons. Monochrome stars are
compared against the SVG's imported raster with alpha respected. Native-size
comparison avoids falsely treating a blurred 48-pixel icon as unrelated art.
This verifies technical source coverage, **not copyright or trademark clearance**.
Artifact hashes and any unmatched IDs are recorded in the redacted manifest.

## Owner-only review deliverables

Two separate local ZIPs exist outside the repository: a 40-candidate,
non-sensitive review pack with contact sheets and individual originals/crops,
and a restricted family/unclassified-source pack. The restricted ZIP, private
images and full sensitive inventory remain outside Git, PR, CI and releases.
Actual local paths, sizes, SHA-256 and CRC verification are in the private
`delivery.json`; paths to sensitive material are not reproduced in this report.
Local links were not downloadable by the owner, and a private draft-release
asset upload returned HTTP 403; the empty draft was removed. The owner then
explicitly approved a **non-sensitive-only exception** to the no-Git rule:
the unchanged 40-candidate ZIP is available on the separate private
[delivery branch](https://github.com/sayac007/Kinderwelt/tree/delivery/visual-ip-public-candidates/downloads/visual-ip-review),
commit `4c3d0e525ae98f28d62dd7c4388deac32178df1c`. Its remote Git blob/size and
local SHA-256 were verified. Do not merge that branch into `main` or publish the
pack. No private/family pack was uploaded.

The original queue starts `not_searched` and `online_upload_permitted=false`.
The returned owner CSV separately records the owner's supplied permissions and
findings; it does not trigger any automatic external upload or search.
Only after the owner approves a **specific non-sensitive file**, the owner may
open Google Images/Lens, upload that candidate, inspect similar results, trace
the earliest credible author/source and record URLs, dates, license terms and
notes locally. No hits is not clearance; resemblance alone is not infringement.
Restricted family/unclassified material has no public-upload instructions.

## Reproduce and verify

Python 3 and Pillow are required (Pillow **12.3.0** was used). Pillow is already
used by the repository's art-authoring tools; no new large dependency was added.
The audit-specific tests report a skip if this optional library is absent;
that is not a completed audit. All audit checks were actually executed here.

```sh
python3 scripts/qa/visual_ip.py --output /owner-only/visual-review/full-inventory.json \
  --generated-root /path/to/retained/generated_images \
  --templates-root /path/to/installed/android/templates \
  --redacted-output docs/qa/visual-ip-manifest.json
python3 scripts/qa/visual_ip_pack.py --inventory /owner-only/visual-review/full-inventory.json \
  --output /owner-only/visual-review/owner-pack
python3 -m unittest discover -s tests/android -p test_visual_ip.py -v
python3 -m unittest discover -s tests/android -p test_visual_c2pa.py -v
python3 scripts/qa/visual_c2pa.py --image assets/quest/science-a.png
python3 scripts/qa/documentation.py --check --verify-archive
```

The scanner never writes art into the repository or uploads images. The full
inventory/private ID map must persist locally to keep opaque IDs stable across
updates. Tests cover signature enumeration, duplicates/SHA, stripped import
remaps, historical private Git blobs, embedded SVG, lossless/masked crops,
animation/atlas frames, alpha-aware identity, deterministic output, stale review
hashes, private redaction, ZIP separation and absence of upload/shell clients.
Actual source/private-path and private-hash redaction was checked against the
full real inventory, in addition to synthetic fixtures. All review ZIPs passed
CRC checks; original/candidate hashes are recorded separately.

**Original PR #18 validation (commit `b9c29f5837c38856b905307bdcf01270992cfb41`):**
the complete existing `tests/run.sh` suite passed; the
final Python repetition passed **149 tests including all 13 audit tests**.
Godot checks passed: 12,750 task checks, 4,168 world checks, 1,231 reward checks,
66 lifecycle checks, save/restart, text/letter layout and audio playback/sequence
checks. All 3,803 shipped speech files decoded. Documentation checks passed:
102 local links, 14 CI references and all 139 archived originals. No new render
suite or Android build was needed for this asset-preserving audit.

**Owner/C2PA follow-up:** 21 focused visual-audit regressions passed, including
seven new credential/CSV cases and the new private/stale-owner-evidence boundary
case. All 18 source identities, seven derivative hash/pixel relationships and
four unchanged first-commit legacy blobs were checked locally. The complete
Python suite passed **157 tests** in 101.074 seconds and decoded all 3,803 speech
files. Documentation revalidation passed **105 local links, 14 CI references
and all 139 archived originals**. Updated manifest/reader consistency and actual
private-path/hash redaction passed. Historical Godot/build results above are
not presented as newly rerun tests; no Android rebuild or new render suite was
performed for these audit-only changes.

```sh
GODOT=/path/to/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
python3 -m unittest discover -s tests/android -v
```

**CI:** deliberately suppressed with `[skip ci]`. The unchanged trusted-push
Android workflow would otherwise create/upload a family APK. This audit's
local-only family-material restriction takes precedence; Android workflows,
signing and access remain unchanged. No remote green check is claimed.

## Coverage gaps and next workorder

- Compiled native XML/protobuf semantic verification is incomplete as described above.
- Nine local symlinks were not followed; one empty/invalid archive was not
  readable. One language-escaped test-source SVG literal was not decoded as a
  standalone image. These are recorded rather than silently cleared.
- The original family reference-photo corpus was not downloaded or opened;
  its count, permissions and consent remain unknown. All such inputs are
  **not available / not reviewed**, never cleared.
- Most screenshots, retained historical images and historical fonts have not
  received independent visual/license review. Available version-matched atlas
  metadata yielded 174 frames; unsupported historical/procedural transformations
  are not invented as separate licensed assets.
- Historical Git coverage covers visual-path objects across all local refs,
  not signature scanning of every non-visual historical blob, deleted remote
  artifacts, inaccessible cloud files or all third-party image collections.
- C2PA credential stores embed provider-icon image boxes. These are recorded as
  credential metadata, not additional playable illustrations or independently
  reviewed sources in the original inventory totals.
- Owner-supplied search observations are now available, but no independent
  search reproduction, qualified legal opinion, worldwide rights clearance or
  ownership determination has been obtained. Cryptographic C2PA validation has
  not been performed and is not represented as a prerequisite for ordinary play.

**Conditional remediation workorder:** retain the owner's completed candidate
findings and privately classify retained/unclassified sources before redistribution.
For a documented specific match or missing right, first obtain/verify the license
or owner decision. Only then replace the selected IDs, preserve the desired game
style and stable task IDs, update provenance/frame data, and run affected
regression/export checks. Do not mass-replace AI art based on style alone.
Separately confirm the visual-art licensing scope and vendor/font obligations,
and review family consent/history before public redistribution. No image
replacement or history rewriting is authorized or performed by this audit PR.
