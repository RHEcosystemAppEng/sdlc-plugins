# Triage Outcome: TC-8006 (CVE-2026-31812, quinn-proto, [rhtpa-2.1])

## How Step 4.2 handled the pre-existing Related link

1. Step 4 found one sibling for CVE-2026-31812: TC-8001, stream suffix `[rhtpa-2.2]`, status In Progress, Affects Versions RHTPA 2.2.0 and 2.2.1.
2. TC-8001's stream (2.2.x) differs from TC-8006's stream (2.1.x). It is therefore a **cross-stream companion tracker**, not a duplicate, and Step 4.1 closure does not apply.
3. Before creating a link, Step 4.2 item 1 checks TC-8006's existing `issuelinks`, which Step 1 already fetched. The issue already has:
   - Link ID 1990401, `type.name = "Related"`, `outwardIssue.key = "TC-8001"` (TC-8006 -> TC-8001).
4. Both match criteria are met: the type is Related, and the sibling key appears as the inward or outward issue. The skill therefore **skipped link creation** and logged:

   > "Related link to TC-8001 already exists — skipping"

5. Result: **no `jira.create_link` call** and no duplicate Related link. Because no mutation was proposed, no confirmation was requested. Re-running triage is idempotent for this link. The existing link's direction (outward rather than inward) is irrelevant, because the check matches either side.
6. Step 4.2 then continued with its other checks:
   - **Affects Versions overlap:** none. TC-8006 has only 2.1.x versions and TC-8001 has only 2.2.x versions.
   - **Sibling landscape table:** shown to the engineer (see sibling-check.md).

## Overall triage outcome (simulated, pending engineer confirmations)

| Step | Result |
|---|---|
| 0.3 | The matrix is 151 days old, so the staleness warning is shown. Assumed "Proceed anyway". |
| 0.8 | Assign TC-8006 to the current user and transition New -> Assigned. |
| 1 | CVE-2026-31812, quinn-proto < 0.11.14, fixed in 0.11.14, Cargo, scoped to 2.1.x |
| 1.5 | External APIs not queried. Fell back to the Jira description threshold of 0.11.14. |
| 1.7 | Skipped (no embargo policy URL configured) |
| 2 | 2.1.0 YES (0.11.9), 2.1.1 YES (0.11.9); 2.2.0 YES, 2.2.1 YES, 2.2.2 YES (retag of 2.2.1), 2.2.3 NO, 2.2.4 NO |
| 3 | Affects Versions [RHTPA 2.1.0] -> [RHTPA 2.1.0, RHTPA 2.1.1], plus a correction comment with the footnote |
| 4.1 | No same-stream duplicate |
| 4.2 | Related link to TC-8001 already exists, so it was skipped. No version overlap. |
| 4.3 | Skipped (custom fields not configured) |
| 4.4 | No preemptive task for 2.1.x |
| 5 | Lifecycle check (not fetched). Assumed 2.1.x is supported. |
| 6 | Not already fixed (TC-8001 is In Progress, not Closed/Done) |
| 7 | Skipped (Upstream Affected Component field not configured) |
| 7.5 | Find or create the release Epic and Task for the 2.1.x stream ("RHTPA <version> Release Tasks" / "RHTPA <version> CVE triage"), with individual confirmation |
| 8 | **Case A + Case B** (details below) |

### Step 8 details

- **Case A (cross-stream):** post a comment on TC-8006 that quinn-proto < 0.11.14 also affects stream 2.2.x (2.2.0, 2.2.1, 2.2.2). That stream is tracked by companion TC-8001 through the existing Related link. No preemptive tasks are created, because 2.2.x already has a CVE Jira.
- **Case B (2.1.x):** create 2 remediation Tasks, because Cargo is a source dependency:
  1. An upstream backport (or a dependency bump, if Step 2.5 finds 0.11.14 already on `release/0.3.z`) to bump quinn-proto to >= 0.11.14 in rhtpa-backend.
  2. Downstream propagation in rhtpa-release.0.3.z, blocked by task 1.
  - Each task is linked to TC-8006 with "Depend". Task 1 Blocks task 2. Each task Blocks the release Task, and TC-8006 is Related to the release Task.
- **Post-triage:** add the `ai-cve-triaged` label, then post a summary comment with the impact table, the Affects Versions correction, the task links, the release Jira references, an @mention of the reporter, and the Comment Footnote.
