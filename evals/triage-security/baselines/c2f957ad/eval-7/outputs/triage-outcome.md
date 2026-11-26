# Triage Outcome: TC-8006, focused on Step 4.2 handling of the pre-existing link

## How Step 4.2 handled the pre-existing Related link

1. **Sibling identified.** The CVE-label JQL search returned TC-8001, whose suffix `[rhtpa-2.2]` maps to stream 2.2.x. TC-8006's suffix `[rhtpa-2.1]` maps to stream 2.1.x. TC-8001 is therefore a **different-stream companion tracker**, not a duplicate. Step 4.1 does not apply, and TC-8006 is not closed.
2. **Check before create.** Before creating any link, Step 4.2 item 1 reads the `issuelinks` array that Step 1 already fetched via `jira.get_issue`. No extra Jira call is needed. It looks for a link where `type.name == "Related"` and either `inwardIssue.key` or `outwardIssue.key` equals the sibling key.
3. **Match found.** Link ID 1990401 is of type `Related`, outward from TC-8006 to TC-8001. It meets both criteria.
4. **Creation skipped.** The skill logs:
   > "Related link to TC-8001 already exists — skipping"

   `jira.create_link(inwardIssue: TC-8006, outwardIssue: TC-8001, type: "Related")` is **not** called. No link mutation is proposed for engineer confirmation, because there is nothing to change. A duplicate Related link between the same pair is avoided, so the operation is idempotent.
5. **Rest of Step 4.2 still runs.** The skip only affects link creation:
   - Affects Versions overlap check: TC-8006 (2.1.x: RHTPA 2.1.0, plus 2.1.1 proposed) and TC-8001 (2.2.x: RHTPA 2.2.0, 2.2.1) share no versions, so nothing is flagged.
   - The sibling landscape table is shown to the engineer (see sibling-check.md).

## Overall triage result (simulated, nothing executed)

| Step | Result |
|---|---|
| 0.3 | Matrix stale (last updated 2026-06-28, about 151 days ago). Staleness warning issued; proceeding for this eval |
| 0.8 | Proposed: assign to current user and transition New → Assigned |
| 1 | CVE-2026-31812, quinn-proto < 0.11.14 (fixed in 0.11.14), Cargo, scope 2.1.x |
| 1.7 | Skipped (no embargo URL configured) |
| 2 | 2.1.0 and 2.1.1 affected (0.11.9). In 2.2.x, 2.2.0, 2.2.1, and 2.2.2 (retag) are affected; 2.2.3 and 2.2.4 are not (0.11.14) |
| 3 | Proposed Affects Versions: [RHTPA 2.1.0] → [RHTPA 2.1.0, RHTPA 2.1.1] |
| 4.1 | No same-stream duplicate |
| 4.2 | Related link to TC-8001 already exists, so creation is skipped. No version overlap |
| 4.3 | Skipped (custom fields not configured) |
| 4.4 | No preemptive task (assumed) |
| 8 | **Case A + Case B.** The issue is scoped and the other stream (2.2.x) is also affected, so a cross-stream impact comment is posted that refers to companion TC-8001 via the existing Related link. No preemptive tasks are created for 2.2.x, because it already has its own CVE Jira (TC-8001). Case B creates 2 Cargo remediation tasks for 2.1.x only, linked to TC-8006 with "Depend": an upstream backport or dependency bump on `release/0.3.z` (depending on Step 2.5), plus a downstream propagation task in rhtpa-release.0.3.z that the first task Blocks |

Every mutation above (assignment, transition, Affects Versions edit, comments with the Comment Footnote, task creation, links, and the `ai-cve-triaged` label) requires engineer confirmation and was **not** executed in this eval.
