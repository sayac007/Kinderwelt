# CI artifacts and storage

Automatic `main` push and pull-request checks run the full existing quality,
render, neutral Android export/verification and size checks, **without uploading
artifacts**. Branch pushes do not duplicate PR runs. Successful technical checks
are not a claim that an artifact was uploaded. No `continue-on-error` masks
failed tests or failed explicitly requested uploads.

## Request a temporary download

In Actions, select **Android verification builds → Run workflow**:

- `variant=neutral` (default): one neutral APK and small technical reports.
- `variant=family`: only the family APK and small reports, with pinned private
  illustrations. Only manual `family`/`both` requests receive the family token.
- `variant=both`: both APKs, explicitly requested; about 640 MB combined.
- `include_unsigned_bundles=true`: separately upload the already verified
  unsigned AABs, about 300 MB each. Default **false**. These are not Play uploads.

All new `actions/upload-artifact` steps explicitly use **three-day retention**,
including the unchanged protected manual signing workflow. Automatic neutral
exports still produce and validate both formats locally on the runner; those
files disappear with the runner instead of using retained Actions storage.

In **Kinderwelt quality gates → Run workflow**, both options default to false:
`retain_evidence` retains reports and rendered screenshots; `listening_review`
prepares/retains the complete offline adult listening pack (about 180 MB).
The full suite and graphical checks precede all uploads.

Three days is not a byte quota. Several manually requested APKs or a single
`both` download can still exceed a free plan's included storage. Generate only
what will actually be downloaded; do not increase retention for convenience.

## Account cleanup and long-term evidence

The operator requested deletion of old Actions artifacts on 2026-10-26.
The inventory found **215 artifacts / 67,218,706,584 bytes** in `Kinderwelt`,
and **zero artifacts** in `Kinderwelt-Privat`. Previous workflow retention was
seven days, not GitHub's general 90-day default. Repository visibility was
reported **public** by the live API; this inventory is not a billing calculation.

The cleanup preserves these five existing downloads, **505,439,680 bytes** total:

| Artifact ID | Purpose | Existing expiry |
|---|---|---|
| `12564507418` | Last separate family APK, run `40105564671`, 0.9.4 / 17 | 2026-10-31 |
| `12658795982` | Recent full-size technical/render evidence, run `40336714270` | 2026-11-02 |
| `12574165940` | Store-review drafts | 2026-10-31 |
| `12657381330` | Latest Pages artifact | 2026-10-27 |
| `12658670323` | Latest small quality diagnostic | 2026-11-02 |

Existing expiry is not shortened retroactively. A retained report is not a new
claim of technical success or a signed Play release. The preserved family APK is
an older tested version, not the pending 0.9.6 publication branch. Downloads
still require GitHub access. Remote artifact download returns HTTP 403 in this
client, so no unverifiable mirror or public release of family images was made.

Only explicitly selected transient Actions artifacts are deleted; workflow runs,
logs, repository history, existing release assets, private illustration source
and the [139-file permanent QA archive](qa/README.md) remain untouched. Run links
in historical summaries remain available; removed download links now lead to
their run logs. Recreate listening/review packs from the versioned sources when
needed. No generated per-run inventory is committed to `docs/qa/`.

Important approved builds may be attached to a GitHub Release, which uses
separate storage from Actions artifacts. This cleanup does not publish releases.
Family data must never be moved to a public release. The publication PR's private
release route deliberately refuses public repositories. A draft flag alone does
not replace the required private-repository decision for those files.

GitHub may take **6–12 hours** to recalculate artifact billing after deletion;
a smaller live artifact list is not proof that the billing quota has refreshed.

## Repository setting requiring the operator

Open **Settings → Actions → General → Artifact and log retention** and set
**3 days**, then save. The current GitHub integration returns HTTP 403 for
Actions administration, so this repository default cannot be confirmed/changed
here. Explicit workflow retention already controls the artifact uploads above;
repository defaults also cover future uploads that omit that value and logs.
Do not change billing or delete releases to bypass a stale quota display.

The six artifact-policy regressions in `tests/android/test_artifact_policy.py`
check retention, manual-only uploads, explicit optional large packs, private
family selection, preserved export/size/full quality checks and release guards.
