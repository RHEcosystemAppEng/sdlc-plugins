# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto < 0.11.14)

## Decision

**Paused at Step 7, Concurrent Triage Detection.** The final Case A/B outcome waits for the engineer's choice (Wait / Skip / Proceed).

TC-8019 (In Progress, assignee engineer-b@example.com) is triaging another CVE on the same upstream component, quinn-proto. Creating remediation tasks now risks duplicates. No remediation tasks are created until the engineer decides. **Recommendation: Wait** and coordinate with engineer-b.

## Findings so far

1. **Configuration valid.** Security Configuration is present. The Upstream Affected Component field (customfield_10632) is configured. PS Component and Stream fields are not, so Step 4.3 was skipped.
2. **Matrix stale.** Last-Updated is 2026-06-28, 129 days old (threshold is 14 days). The engineer was warned. The eval proceeded with the current matrix.
3. **Scope.** The issue is scoped to stream **2.2.x** (`[rhtpa-2.2]`). The ecosystem is Cargo (source dependency).
4. **Version impact (lock files at pinned tags):**
   - 2.2.0 (0.11.9): affected
   - 2.2.1 (0.11.12): affected
   - 2.2.2 (retag of 2.2.1): affected
   - 2.2.3 and 2.2.4 (0.11.14): not affected
   - 2.1.0 and 2.1.1 (0.11.9): affected, outside this issue's scope
5. **Affects Versions correction (proposed):** `[RHTPA 2.0.0]` becomes `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. The PSIRT value is wrong because no 2.0 stream exists. A correction comment with the Comment Footnote is proposed. There is no ProdSec @mention because none is configured.
6. **Embargo check skipped** because no policy URL is configured. External CVE enrichment was not performed (eval restriction), so the Jira description threshold (fixed in 0.11.14) is used.
7. **Steps 4–6:** no sibling, lifecycle, or resolved-sibling data was supplied, so nothing was filtered out in these steps. In a live run, the Step 4 JQL `labels = 'CVE-2026-31812'` would look for a 2.1.x companion issue.
8. **Step 7:** concurrent triage TC-8019 detected (see concurrent-triage.md).

## Planned path after the engineer's choice

- **Wait:** stop now. Re-run triage after TC-8019 completes and check whether its remediation bumps quinn-proto to 0.11.14 or later on release/0.4.z. If it does, link TC-8020 to that task (Related to TC-8019, Depend to the covering task) instead of creating new tasks.
- **Skip:** no remediation tasks. Post an explanatory comment on TC-8020 with the footnote.
- **Proceed:** add label `concurrent-triage-overlap`, then:
  - Step 7.5: find or create the release Epic and Task for the 2.2.x release family. Run the cross-CVE dedup check (7.5.3) against remediation Tasks already linked for quinn-proto, which may include TC-8019's.
  - Case A (scoped issue, other stream affected): post a cross-stream impact comment saying 2.1.x (2.1.0, 2.1.1) is also affected. If no 2.1.x CVE Jira exists for CVE-2026-31812, create preemptive tasks for 2.1.x: label `security-preemptive`, linked to TC-8020 with Related.
  - Case B for 2.2.x creates 2 Cargo tasks: an upstream task (dependency bump if Step 2.5 confirms release/0.4.z ships 0.11.14, otherwise upstream backport) plus a downstream Konflux propagation task. The downstream task is blocked by the upstream task, both link to TC-8020 with Depend, and both link to the release Task with Blocks. The latest 2.2.4 already ships 0.11.14, so the remediation is likely small: confirm the next release keeps 0.11.14 or later.
- **Case C does not apply:** supported versions in scope (2.2.0–2.2.2) are affected, so this is not "Not a Bug".

## Post-triage (after completion, not executed)

- Add label `ai-cve-triaged`.
- Post a summary comment covering:
  - the impact table and Affects Versions correction
  - the outcome and any task or release references
  - the concurrent-triage note about TC-8019
  - an @mention of the reporter
  - the triage-security Comment Footnote

## Items not verified in this eval

- Upstream branch HEAD versions (Step 2.5), dependency chain (Step 2.3.5), development-stream status, Jira version IDs, lifecycle status, sibling issues. No simulated data was provided for these, so nothing was assumed.
- The issue key in the mock file (TC-8001) differs from the task target (TC-8020). TC-8020 was used.
