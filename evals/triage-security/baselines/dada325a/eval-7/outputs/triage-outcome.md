# TC-8006 — Triage Outcome and How Step 4.2 Handled the Existing Link

## How Step 4.2 handled the existing Related link

1. **Input:** Step 1 had already fetched the `issuelinks` for TC-8006. It holds one link: ID 1990401, type `Related`, outward from TC-8006 to TC-8001.
2. **Sibling found:** The Step 4 JQL returned TC-8001, suffix `[rhtpa-2.2]`. TC-8006 has suffix `[rhtpa-2.1]`, so TC-8001 is a different-stream companion and is handled by Step 4.2, not 4.1.
3. **Idempotency check:** Before creating any link, Step 4.2 looks for an existing link with `type.name == "Related"` where `inwardIssue.key` or `outwardIssue.key` equals TC-8001. Link 1990401 meets both conditions. The direction does not matter, because the rule accepts either inward or outward.
4. **Result:** Link creation is **skipped**. The skill logs:
   > "Related link to TC-8001 already exists — skipping"
5. **No duplicate link:** `jira.create_link(inwardIssue: TC-8006, outwardIssue: TC-8001, type: "Related")` is **not** called. No confirmation prompt is needed for a link, and running the triage again stays idempotent.
6. **Rest of Step 4.2 still runs:** The Affects Versions overlap check found no overlap (2.1.x vs 2.2.x versions), and the sibling landscape table was presented.

## What does not happen

- TC-8006 is **not** closed as Duplicate. TC-8001 is in a different stream, and being In Progress does not change that.
- No second Related link to TC-8001 is created.
- No new Vulnerability issue is created.

## Overall triage path (simulated, interactive mode)

| Step | Result |
|---|---|
| 0 | Config valid. Optional fields (Upstream Affected Component, ProdSec, Embargo) are absent. |
| 0.3 | Matrix is stale (about 131 days). Warning raised; proceeding with the current matrix. |
| 0.8 | Assign to the current user and move New → Assigned (needs confirmation; not executed). |
| 1 | CVE-2026-31812, quinn-proto < 0.11.14, fixed in 0.11.14, scoped to 2.1.x, Cargo. |
| 1.5 | External enrichment not run; Jira description threshold used, at reduced confidence. |
| 1.7 | Skipped (no embargo URL configured). |
| 2 | 2.1.0 YES, 2.1.1 YES (0.11.9); 2.2.0 YES, 2.2.1 YES, 2.2.2 YES (retag); 2.2.3 NO, 2.2.4 NO. |
| 3 | Propose Affects Versions `[RHTPA 2.1.0]` → `[RHTPA 2.1.0, RHTPA 2.1.1]`. |
| 4.1 | No same-stream duplicate. |
| 4.2 | TC-8001 is a cross-stream companion. **Existing Related link detected, creation skipped.** No version overlap. |
| 4.3 | Skipped (custom fields not configured). |
| 4.4 | No preemptive task (none in the scenario). |
| 5 | Lifecycle page not fetched in this eval. Assumed supported pending verification. |
| 6 | No resolved siblings, so not already fixed. |
| 7 | Skipped (Upstream Affected Component field not configured). |
| 7.5 | Find or create the RHTPA 2.1.x release Epic and Task (default patch bump would be 2.1.2). Needs confirmation; dedup in 7.5.3 is skipped. |
| 8 | **Case A + Case B.** Case A: post a cross-stream impact comment saying 2.2.x (2.2.0–2.2.2) is also affected. 2.2.x already has its own CVE Jira (TC-8001), so no preemptive tasks are created. Case B: create 2 Cargo remediation Tasks for 2.1.x: a quinn-proto bump to ≥ 0.11.14 on `release/0.3.z` (a dependency bump if Step 2.5 finds the fix already upstream, otherwise an upstream backport), plus downstream propagation in rhtpa-release.0.3.z. Upstream Blocks downstream, both Depend on TC-8006, both Block the release Task, and TC-8006 is Related to the release Task. |
| Post | Add the `ai-cve-triaged` label and post a summary comment with the reporter @mention and Comment Footnote. |

Every Jira mutation listed above needs engineer confirmation in a live run. None were executed in this eval.
