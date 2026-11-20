# Triage Outcome: TC-8006 (CVE-2026-31812, quinn-proto, [rhtpa-2.1])

## How Step 4.2 handled the pre-existing Related link

1. The sibling JQL returned TC-8001. Its suffix `[rhtpa-2.2]` maps to stream 2.2.x, and TC-8006's suffix `[rhtpa-2.1]` maps to stream 2.1.x. So TC-8001 is a **cross-stream companion**, not a duplicate, and Step 4.1 does not apply.
2. Before creating any link, Step 4.2 checked TC-8006's existing `issuelinks`, which were already fetched in Step 1. It found link **1990401**:
   - `type.name` = `Related`
   - the `outwardIssue.key` = `TC-8001`
3. Both match criteria held, so the skill **skipped link creation** and logged:
   > "Related link to TC-8001 already exists — skipping"
4. No `jira.create_link` call was proposed or run. This idempotent check prevents a duplicate Related link between the same pair of issues. The existing link's direction (TC-8006 → TC-8001) is accepted because the check matches either the inward or the outward endpoint.
5. Step 4.2 then went on with its other duties as normal. The Affects Versions overlap check found no overlap (2.1.x versions against 2.2.x versions), and the sibling landscape table was presented.

## Overall triage result (remaining steps, simulated)

| Step | Result |
|---|---|
| 0.3 Matrix staleness | Matrix is 145 days old (last updated 2026-06-28). Warning raised; proceeded in this eval |
| 0.8 Assign/transition | Proposed: assign to the current user and transition New → Assigned (needs confirmation) |
| 1.7 Embargo | Skipped (no policy URL configured) |
| 2 Version impact | 2.1.0 and 2.1.1 are **affected** (quinn-proto 0.11.9 < 0.11.14). In 2.2.x, 2.2.0–2.2.2 are affected and 2.2.3–2.2.4 are fixed |
| 3 Affects Versions | Proposed `[RHTPA 2.1.0]` → `[RHTPA 2.1.0, RHTPA 2.1.1]` |
| 4 Sibling check | TC-8001 is a cross-stream companion. Related link already exists, so creation was skipped. No version overlap |
| 4.3 / 7 / 7.5.3 | Skipped (Upstream Affected Component field not configured) |
| 4.4 Preemptive reconciliation | No matching preemptive task assumed |
| 5 Lifecycle | Not fetched (no external calls). Assumes 2.1.x is supported, to verify against the product pages |
| 6 Already fixed | TC-8001 is In Progress, not Closed/Done, so there is no already-fixed coverage |
| 7.5 Release Jira | Would search for or create "RHTPA 2.1.x Release Tasks" and the matching CVE triage Task. With no existing Epic, the default proposal is RHTPA 2.1.2 (needs confirmation) |
| 8 Remediation | **Case A + Case B** (see below) |

### Case A – Cross-stream impact

Stream 2.2.x is also affected, but it already has its own CVE Jira (TC-8001). So **no preemptive tasks are created**. The skill would post this cross-stream comment, with the Comment Footnote, after confirmation:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.2.x (RHTPA 2.2.0, 2.2.1, and 2.2.2, a retag of 2.2.1) based on lock file analysis. This stream is tracked by companion issue TC-8001 (see Related links).

### Case B – Remediation for 2.1.x (Cargo means 2 tasks)

Upstream fix status on `release/0.3.z` (Step 2.5) could not be checked without `git show`. Depending on the result:
- Fix not on the branch: (1) an upstream backport task bumping quinn-proto to ≥ 0.11.14 on `rhtpa-backend` `release/0.3.z`, and (2) a downstream propagation task in `rhtpa-release.0.3.z`, blocked by task 1.
- Fix already on the branch: a dependency bump task (`cargo update -p quinn-proto`) plus downstream propagation.

Links: each task Depend → TC-8006, upstream Blocks downstream, each task Blocks the release Task, and the release Task Related to TC-8006.

### Post-triage

- Add the `ai-cve-triaged` label to TC-8006.
- Post a summary comment with the version impact table, the Affects Versions correction, the remediation task keys, the release Jira keys, an @mention of the reporter, and the Comment Footnote.

All Jira mutations above are proposals that need engineer confirmation. None were executed in this eval.
