# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision: **Close as Duplicate of TC-7999**

## Rationale

1. **Same CVE, same stream, open sibling.** TC-7999 has the label CVE-2026-31812, the same component `pscomponent:org/rhtpa-server` and the same stream suffix `[rhtpa-2.2]`. It is In Progress. Under Step 4.1, a same-stream sibling that is open or in progress means the current issue is a duplicate.
2. **The versions overlap completely.** TC-8003's only Affects Version (RHTPA 2.2.0) is already on TC-7999 ([RHTPA 2.2.0, RHTPA 2.2.1]). The lock-file evidence confirms 2.2.0 is affected (quinn-proto 0.11.9 < 0.11.14).
3. **Nothing would be lost by closing.** All remediation for stream 2.2.x is tracked by TC-7999. Creating remediation tasks from TC-8003 would duplicate TC-7999's work.

## Effect on later steps

| Step | Result |
|---|---|
| 3 – Affects Versions correction | Not applied to TC-8003 because it is being closed as a duplicate. The 2.2.2 gap is handed to TC-7999. |
| 5 – Lifecycle check | Not needed for a duplicate closure. The product pages were not fetched because external calls were forbidden. |
| 6 – Already fixed | Not applicable: no resolved (Closed/Done) siblings. |
| 7 / 7.5.3 – Concurrent triage / dedup | Skipped: Upstream Affected Component field is not configured. |
| 7.5 – Release Jira | Not applicable: no remediation tasks are created from TC-8003. |
| 8 – Remediation | **No remediation tasks created.** Case A/B/C do not apply because the issue ends as a duplicate. |

## Proposed Jira mutations (each needs engineer confirmation; NOT executed)

1. Assign TC-8003 to the current user (Step 0.8 / 4.1). The transition to Assigned is superseded by the closure.
2. Add the duplicate comment to TC-8003, including the Comment Footnote (text in duplicate-check.md).
3. Transition TC-8003 to **Closed**, resolution **Duplicate**.
4. Optional traceability link TC-8003 -> TC-7999 (Duplicate/Related, created only if it does not already exist).
5. Add the `ai-cve-triaged` label to TC-8003.
6. Post a post-triage summary comment on TC-8003 that includes the version impact table, the duplicate outcome, an @mention of the issue reporter, and the Comment Footnote. There are no remediation tasks, release Jira entries or dedup results to list.

No VEX Justification is set, because a duplicate closure is not a "not affected" determination.

## Follow-ups for TC-7999's owner (informational)

- Add **RHTPA 2.2.2** to TC-7999's Affects Versions. It is a backend retag of 2.2.1 and ships quinn-proto 0.11.12.
- RHTPA 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (fixed).
- Stream **2.1.x** (2.1.0 and 2.1.1, quinn-proto 0.11.9) is also affected and has no CVE Jira. It needs a cross-stream comment or preemptive remediation through TC-7999's triage, or PSIRT follow-up.

## Caveats

- The security matrix is 145 days old (Last-Updated 2026-06-28). I chose "Proceed anyway" for the simulation, and a refresh is recommended.
- No MITRE/OSV cross-validation was done. The fix threshold (0.11.14) comes from the Jira description only.
- The due date (2026-07-15) has already passed. That does not change the duplicate decision, but it raises the urgency on TC-7999.
- All Jira and lock-file data is simulated from the provided eval files.
