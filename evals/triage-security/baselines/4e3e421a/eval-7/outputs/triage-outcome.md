# Triage Outcome: TC-8006 (focus on Step 4.2 handling of the pre-existing link)

## How Step 4.2 handled the pre-existing Related link

1. Step 4 found one sibling for CVE-2026-31812: **TC-8001** `[rhtpa-2.2]`, In Progress, with Affects Versions RHTPA 2.2.0 and 2.2.1.
2. TC-8001 is on stream 2.2.x and TC-8006 is on stream 2.1.x, so TC-8001 is a **cross-stream companion tracker**, not a duplicate. Step 4.1 does not apply and no Duplicate closure happens.
3. Step 4.2.1 says to check for an existing link before creating one. The `issuelinks` array on TC-8006 from Step 1 already has:
   - Link ID **1990401**, `type.name = "Related"`, outward TC-8006 → TC-8001.
   This matches both criteria: the link type is Related, and `outwardIssue.key` is the sibling key. The check accepts either direction, inward or outward.
4. Result: **link creation skipped**. Log line:
   > "Related link to TC-8001 already exists — skipping"
   - No `jira.create_link` call is made or proposed.
   - No duplicate Related link is created.
   - Nothing about this link goes to the engineer for confirmation, because no mutation is needed.
   - The existing link (ID 1990401) is left as-is. Its direction is not changed and it is not recreated.
5. Step 4.2.2 overlap check: TC-8006 has {2.1.0, 2.1.1} and TC-8001 has {2.2.0, 2.2.1}. There is no overlap and no flag.
6. Step 4.2.3 showed the sibling landscape (see sibling-check.md).

## Overall triage outcome (proposals only; no Jira mutations executed)

| Step | Result |
|---|---|
| 0.3 | Matrix is about 128 days old, so the stale warning fires. The eval proceeds with the current matrix. |
| 0.8 | Assign TC-8006 to the current user and transition New to Assigned |
| 1 | CVE-2026-31812, quinn-proto < 0.11.14, fix 0.11.14, Cargo, scoped to 2.1.x |
| 1.7 | Skipped (no embargo URL configured) |
| 2 | 2.1.0 YES (0.11.9), 2.1.1 YES (0.11.9). Other stream: 2.2.0, 2.2.1, 2.2.2 YES; 2.2.3, 2.2.4 NO |
| 3 | Affects Versions: [RHTPA 2.1.0] → [RHTPA 2.1.0, RHTPA 2.1.1], with a correction comment and footnote |
| 4.1 | No same-stream duplicates |
| 4.2 | TC-8001 is a companion. The Related link already exists, so it was skipped (idempotent). No version overlap. |
| 4.3 | Skipped (custom fields not configured) |
| 4.4 | No preemptive tasks found |
| 5 | Lifecycle check would run against the Product pages URL. Not fetched in this eval. |
| 6 | Not already fixed (TC-8001 is In Progress, not resolved) |
| 7 | Skipped (Upstream Affected Component field not configured) |
| 7.5 | Find or create the release Epic "RHTPA 2.1.x Release Tasks" and the release Task "RHTPA <next 2.1.z> CVE triage". Each needs individual confirmation. |
| 8 | **Case A + Case B.** Case A: cross-stream impact comment saying 2.2.x is also affected and is tracked by companion TC-8001 through the existing Related link, so no preemptive tasks are needed. Case B: two Cargo tasks for 2.1.x. Task 1 is the upstream backport or dependency bump of quinn-proto to >= 0.11.14 on `release/0.3.z`. Task 2 is downstream propagation in rhtpa-release.0.3.z and is blocked by Task 1. Both link to TC-8006 with "Depend", get a description digest comment, and link to the release Task with "Blocks". TC-8006 links to the release Task with "Related". |
| Post | Add the `ai-cve-triaged` label and post a summary comment with the reporter @mention and Comment Footnote |

## Key point

Step 4.2 is idempotent. Because the Related link between TC-8006 and TC-8001 already existed (link ID 1990401), the skill detected it in the Step 1 `issuelinks` data, logged "Related link to TC-8001 already exists — skipping", and created no duplicate link.
