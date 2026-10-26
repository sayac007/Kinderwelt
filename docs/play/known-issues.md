# Known issues — operator-maintained register

Current repository target: **0.9.6 / 19**. The version used in the operator's
phone/tablet report was not specified. On 2026-10-24 the accessible GitHub issue tracker returned
**zero open issues** (`gh issue list --state open --json number,title,url`). This
is not proof that the app has no bugs. No issue or owner comment was fabricated.
Update this table from actual reports and link the responsible issue/commit.

| Issue / link | Affected version | Status | Reproduction / workaround | Fix / verified version |
|---|---|---|---|---|
| No open tracker entries at the recorded query | 0.9.5 / 18 preparation | No tracker report | — | — |

## Operator device acceptance — 2026-10-26

The operator reports image selection, rotation, updates and the exercised app
behaviour working on a **phone and a tablet**. Status: **PASS — operator reported**.
[Recorded scope](../ACCEPTANCE.md): no device model, OS version, app version,
package or APK hash was supplied. No independent execution or full per-OS/format
matrix is inferred. No identifying device or child data is recorded.

## Remaining acceptance detail, not confirmed defect reports

| Boundary | Version | Status / owner |
|---|---|---|
| Image picker, rotation and updates on phone/tablet | Operator-tested build; version unspecified | PASS — operator report 2026-10-26; detailed Android-version/URI/cancel matrix not supplied |
| Specific low-memory/performance and backup/transfer scenarios | Current release preparation | Not individually documented in the general operator report; no defect reported |
| Complete DE/EN/RU listening and independent pedagogical review | Current bundled content | OPEN — adult reviewers; automated transcripts are not clearance |
| Final package, upload key, protected release environment, rights/contact/privacy publication, Data Safety/age rating | Release preparation | OPERATOR DECISION; no Play upload readiness claim |
| Play internal/closed track, pre-launch reports and account-specific test requirements | First upload | NOT VERIFIED — operator/Play Console |

Use [the test guide](closed-test.md) and [full acceptance](../ACCEPTANCE.md).
Do not put child/family photos, saves, credentials or identifying bug-report data
in this file. No new single-run QA logs are kept in Git.
