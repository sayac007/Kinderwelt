# Quality evidence and long-term references

Start with [QUALITY_ASSURANCE.md](../QUALITY_ASSURANCE.md).
This directory retains the archive index and the two named, current visual-audit
references. It is not a destination for individual test-run logs.

- [VISUAL_IP_AUDIT.md](VISUAL_IP_AUDIT.md): current visual provenance/similarity
  triage, coverage gaps and owner review actions; no legal clearance.
- [visual-ip-manifest.json](visual-ip-manifest.json): redacted inventory;
  private images, identifying paths and private image hashes are withheld.
- [ARCHIVE_INDEX.tsv](ARCHIVE_INDEX.tsv): the unchanged, reviewed index of
  **139 historical files / 7,383,943 bytes**.

## Historical evidence is preserved

The original files remain byte-for-byte in the same private repository at tag
[`qa-evidence/2026-10-23-v091`](https://github.com/sayac007/Kinderwelt/tree/qa-evidence/2026-10-23-v091/docs/qa),
commit [`a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`](https://github.com/sayac007/Kinderwelt/tree/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa).
The index records source paths, sizes, SHA-256, Git blob IDs, Git dates, purposes
and earlier references. Unrecorded run times are not invented. This is a durable
Git reference, not an expiring artifact; do not delete or retarget it.

```sh
git fetch origin refs/tags/qa-evidence/2026-10-23-v091:refs/tags/qa-evidence/2026-10-23-v091
git show qa-evidence/2026-10-23-v091:docs/qa/phase2.log > /tmp/kinderwelt-phase2.log
```

Historical logs can contain local paths and variant metadata. Do not publish
copies without review. No historical file, photo, family illustration or key
has been removed or newly published by the visual audit. History rewriting is
outside this workorder.

## Storage policy

New run output belongs in `qa-results/` or `build/`. Manually requested new CI artifacts expire
after three days and are not a long-term evidence archive. The explicitly named
current audit report and its redacted inventory are maintained references, not
one new report per run. The existing voice-recognition fixtures are necessary
regression references rather than a general run archive.

The full sensitive inventory and restricted review ZIP stay outside the repository
in an owner-only local directory. The owner subsequently authorized the unchanged
40-candidate non-sensitive ZIP on a separate private download branch because
local links and release-asset uploads failed; see the audit report for that exact
exception and verified commit. Do not merge the download branch into `main`.
The owner-returned manual findings and local C2PA metadata are current provenance
references under `scripts/qa/`, not per-run logs. No automatic image search or
upload follows from importing them. Restricted material remains excluded from
Git, PR attachments, CI artifacts and releases.
