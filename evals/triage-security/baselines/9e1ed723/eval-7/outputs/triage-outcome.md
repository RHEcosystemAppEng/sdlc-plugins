# Triage Outcome: TC-8006, and how Step 4.2 handled the pre-existing link

## How Step 4.2 handled the pre-existing Related link

1. The Step 4 sibling search returned TC-8001 (stream suffix `[rhtpa-2.2]`). TC-8006's suffix is `[rhtpa-2.1]`, so TC-8001 is a **cross-stream companion**, not a duplicate. Step 4.1 duplicate closure does not apply.
2. Step 4.2 item 1 says to check for an existing link before creating one. The skill read TC-8006's `issuelinks` (already fetched in Step 1). It found link ID **1990401**, with `type.name = "Related"` and `outwardIssue.key = TC-8001`. Both conditions hold: the type is Related, and the inward or outward key matches the sibling.
3. **Outcome: link creation was skipped (idempotent behaviour).** No `jira.create_link` call was made, so no duplicate Related link exists. The skill logged:
   > "Related link to TC-8001 already exists — skipping"
4. The existing link's direction (outward, TC-8006 → TC-8001) differs from the direction the skill would use when creating one (inward = current, outward = sibling). Direction is irrelevant to the match, so the link was accepted as-is. It was not deleted, recreated, or modified.
5. Step 4.2 then continued normally:
   - Affects Versions overlap check: TC-8006 (2.1.0, 2.1.1) vs TC-8001 (2.2.0, 2.2.1) have no overlap, so nothing was flagged.
   - The sibling landscape table was presented (see `sibling-check.md`).

## Overall triage outcome (simulated; every Jira mutation would need engineer confirmation)

| Step | Result |
|---|---|
| 0.8 | Assign TC-8006 to the current user and transition New → Assigned |
| 2 | 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 (< 0.11.14), so they are affected. Out of scope: 2.2.0, 2.2.1, and 2.2.2 (retag) are affected; 2.2.3 and 2.2.4 (0.11.14) are not |
| 3 | Affects Versions `[RHTPA 2.1.0] → [RHTPA 2.1.0, RHTPA 2.1.1]` plus a correction comment (with footnote, no ProdSec @mention because none is configured) |
| 4.1 | No same-stream duplicate |
| 4.2 | Related link to TC-8001 already exists, so it was skipped. No version overlap |
| 4.3 | Skipped (component custom fields not configured) |
| 4.4 | No preemptive task for rhtpa-2.1 |
| 5 | Lifecycle check against the product pages URL (not executed in this eval) |
| 6 | No resolved sibling. TC-8001 is In Progress, so the issue is not already fixed |
| 7 | Skipped (Upstream Affected Component field not configured) |
| 7.5 | Find or create the "RHTPA 2.1.x CVE triage" release Epic/Task for the 2.1.x stream (needs individual confirmation) |
| 8 | **Case A + Case B**: post a cross-stream impact comment saying 2.2.x is also affected and tracked by companion TC-8001 (no preemptive tasks, since that stream has its own CVE Jira). Create 2 Cargo remediation tasks for 2.1.x (upstream fix on `release/0.3.z` in rhtpa-backend, plus downstream propagation in rhtpa-release.0.3.z, linked with Blocks). Link both to TC-8006 with "Depend" and to the release Task with "Blocks". Link TC-8006 to the release Task with "Related" |
| Post-triage | Add the `ai-cve-triaged` label and a summary comment (impact table, AV correction, tasks, release refs, reporter @mention, Comment Footnote) |

Net effect for Step 4: **zero new links were created toward TC-8001.** The pre-existing Related link (ID 1990401) is the only cross-stream link, which avoids duplicate links on re-triage.
