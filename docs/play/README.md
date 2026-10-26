# Play upload preparation

The public release is **neutral only**. Draft PRs remain separate; no automatic
merge or Play upload is performed. Family graphics/photos never enter Store
materials. This folder contains operator-review drafts, not approval decisions.

1. Review/merge the release, measured size, notices and local-image packages in
   order. Current technical evidence: [quality overview](../QUALITY_ASSURANCE.md).
2. Approve rights and fill the final package, publisher, support contact and asset
   licence. Configure the protected `release` environment and offline key backup
   using [Android release instructions](../android.md). Confirm required reviewers
   and `main`-only deployment in GitHub; a workflow environment name alone does
   not prove that its protection rules exist.
3. Replace/approve every placeholder in the [DE](../privacy/datenschutz.de.md),
   [EN](../privacy/privacy.en.md) and [RU](../privacy/privacy.ru.md) privacy drafts,
   including date, legal bases, rights and support handling. Generate static HTML:
   `python3 scripts/store/privacy.py --output build/privacy`. Final publication
   preparation uses `--final`, which fails on unresolved fields. The inactive
   [Pages template](../../.github/workflow-templates/privacy-pages.yml) lives outside
   the active workflows; only the operator enables hosting and copies it after
   approval. No Pages settings or publication were changed.
4. Review [Data Safety](data-safety.md) and [content rating](content-rating.md)
   against the actual final build and current Console questions. Pick child age
   groups and complete Families declarations yourself. No blanket legal or learning
   efficacy claim is made.
5. Check generated listing text in [DE](listing.de.md), [EN](listing.en.md),
   [RU](listing.ru.md): `python3 scripts/store/listing.py --check`. This compares
   the entire generated text with actual tasks, locales, scenes and music catalogs.
   Use `--write` after deliberate content changes, then review again.
6. Generate Store graphics (Godot 4.7.2, real graphics backend, neutral snapshot
   and isolated user data):

   ```sh
   GODOT=/path/to/Godot_v4.7.2-stable_linux.x86_64 LIBGL_ALWAYS_SOFTWARE=1 \
     xvfb-run -a -s '-screen 0 1280x1920x24 -noreset' python3 scripts/store/render.py --output build/store
   ```

   Output: 512×512 icon, 1024×500 text-free feature graphic, five **1080×1920**
   phone screenshots per DE/EN/RU: characters, own-image editor, world path,
   maths, reward. The own image is an original geometric silhouette, never a
   photograph. Input guards reject family/unknown character inputs and external
   or embedded photos in the placeholder. The script cannot accept a user photo
   or family variant. It produces review drafts and a provenance record, not
   a Store approval. Use a new output directory on repeated runs.
7. The separate [Store preparation workflow](../../.github/workflows/store.yml)
   renders review artifacts only, with read-only repository access and no family
   token, release secrets, Pages permissions or publishing. Artifacts expire after
   seven days; keep operator-approved final Store materials in an appropriate
   private archive. They are not QA/legal acceptance records by themselves.
8. Build/verify the neutral AAB with operator-owned credentials using the manual
   `android-release.yml` on `main`. The source must include the reviewed image
   feature. A preview/test identifier or unsigned AAB cannot be uploaded as the
   final release. Inspect identity, signature, notice/resource, permission/backup,
   16KB alignment and bundletool size reports. Only then upload manually to Play's
   internal/closed test; resolve Play's pre-launch results and complete physical
   [device/listening/content acceptance](../ACCEPTANCE.md).

**Still operator-owned:** final package and upload key, release environment
protection, publisher/support/legal decisions, public privacy URL, asset rights,
audience/rating/Data Safety answers, tester invitations/account requirements,
actual Play acceptance and production decision. Do not paste keys into chat or Git.

## Closed-test handoff

Use the [DE/EN/RU tester guide](closed-test.md) and [known-issue register](known-issues.md).
The parents area shows the canonical version/code without collecting diagnostics.
The optional email/report button is intentionally omitted: reports use the
operator-selected channel, with no new permission or in-app data-export path.
