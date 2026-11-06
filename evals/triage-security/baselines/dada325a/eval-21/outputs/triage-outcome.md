# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision

**Paused at Step 7 – Concurrent Triage Detection. Waiting for the engineer to choose Wait / Skip / Proceed.**
Recommended choice: **Wait** and coordinate with engineer-b@example.com on TC-8019.

No remediation tasks, release Jira items, labels, comments, or transitions have been created or executed. All Jira
mutations below are *proposed only* (eval forbids Jira calls, and every mutation needs engineer confirmation).

## Why

1. **Affected (lock-file evidence):** in the scoped stream 2.2.x, RHTPA 2.2.0 (quinn-proto 0.11.9), 2.2.1 (0.11.12)
   and 2.2.2 (same as 2.2.1, retag) are vulnerable (< 0.11.14). 2.2.3 and 2.2.4 ship 0.11.14 and are **not** affected.
   Outside the issue's scope, 2.1.0 and 2.1.1 (0.11.9) are also affected.
2. **PSIRT Affects Versions is wrong:** `RHTPA 2.0.0` -> proposed `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`.
3. **Concurrent triage:** the Step 7 JQL on `cf[10632] ~ 'quinn-proto'` returned TC-8019 (In Progress,
   engineer-b@example.com). Creating quinn-proto remediation tasks now risks duplicating TC-8019's work. Step 4.3
   cross-CVE overlap detection could not mitigate this, because the PS Component / Stream fields are not configured.
   The skill requires the engineer's choice before going on to Step 7.5 and Case A/B/C.

## Proposed actions recorded so far (pending confirmation)

| Step | Proposed mutation |
|---|---|
| 0.8 | Assign TC-8020 to current user; transition New -> Assigned |
| 3 | Affects Versions `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` + correction comment (with Comment Footnote; no ProdSec @mention, not configured) |

## What happens after the engineer's choice

- **Wait:** stop now; re-run `/sdlc-workflow:triage-security TC-8020` after TC-8019 completes.
- **Skip:** no remediation tasks; comment on TC-8020 explaining the skip because of concurrent triage TC-8019.
- **Proceed:** add label `concurrent-triage-overlap` to TC-8020, then:
  - Step 7.5: find/create the release Epic/Task for 2.2.x and run the cross-CVE dedup check (7.5.3). If TC-8019 has
    already linked a quinn-proto remediation Task to the release Task, link TC-8020 to it instead of creating new tasks.
  - Step 8 **Case A** (scoped issue, other stream 2.1.x affected): post a cross-stream impact comment. If 2.1.x has no
    companion CVE Jira, create preemptive tasks (label `security-preemptive`, link type Related): an upstream backport of
    quinn-proto >= 0.11.14 on `release/0.3.z`, then a downstream propagation task.
  - Step 8 **Case B** for 2.2.x: 2 Cargo tasks (dependency bump + downstream propagation, linked with Depend). Note that
    `release/0.4.z` released tags v0.4.11+ already ship 0.11.14, so the fix is effectively shipped in RHTPA 2.2.3+. The
    engineer should check whether the bump is a no-op and whether the issue can instead record 2.2.3 as the fixed release.
  - Post-triage: add the `ai-cve-triaged` label and post a summary comment @mentioning the reporter (with Comment Footnote).

## Caveats

- The mock issue file shows key TC-8001; the task's key TC-8020 was used.
- The security matrix is 131 days old (Last-Updated 2026-06-28), so newer releases may be missing.
- External CVE enrichment (MITRE/OSV), the lifecycle page, Jira version discovery, development-stream HEAD and sibling
  searches were not run (no external calls in eval). Jira description data was used for the fix threshold (0.11.14).
