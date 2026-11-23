# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision

**Close TC-8003 as Duplicate of TC-7999.** TC-8003 gets no Affects Versions correction
and no remediation tasks.

## Rationale

1. **Same CVE, same stream.** TC-7999 carries the same CVE label (CVE-2026-31812), the same component (`pscomponent:org/rhtpa-server`) and the same stream suffix `[rhtpa-2.2]`. Under Step 4.1 it is a same-stream sibling, not a cross-stream companion tracker.
2. **The sibling is active.** TC-7999 is In Progress, and an open or in-progress same-stream sibling triggers the Duplicate closure path.
3. **The versions overlap completely.** TC-8003 claims RHTPA 2.2.0, which is a subset of TC-7999's RHTPA 2.2.0 and 2.2.1.
4. **The vulnerability is real for 2.2.x, but already tracked.** Lock-file evidence shows 2.2.0 (0.11.9), 2.2.1 (0.11.12) and 2.2.2 (retag of 2.2.1) are affected; 2.2.3 and 2.2.4 (0.11.14) are not. A Case C "Not a Bug" closure is therefore wrong. The issue is affected, and the remediation belongs to TC-7999.

## Steps executed and their effect

| Step | Result |
|------|--------|
| 0 Config | Valid. Optional overlap, ProdSec and embargo fields are not configured. |
| 0.3 Matrix staleness | Matrix is 148 days old (Last-Updated 2026-06-28). Warning recorded; proceeded. |
| 0.6 Mode | Interactive. FULLSEND_OUTPUT_DIR is absent. |
| 0.8 Assign/transition | Proposed: assign to current user, then New -> Assigned. |
| 1 Data extraction | Complete (see data-extraction.md). |
| 1.5 Enrichment | External APIs not called. Jira description used (fix threshold 0.11.14). |
| 1.7 Embargo | Skipped (no policy URL configured). |
| 2 Version impact | 2.2.x affected: 2.2.0, 2.2.1, 2.2.2. 2.1.x affected: 2.1.0, 2.1.1. |
| 3 Affects Versions | Evidence-based value would be [2.2.0, 2.2.1, 2.2.2]. Not applied because the issue is being closed as a duplicate. |
| 4 Duplicate check | **Same-stream duplicate of TC-7999. Close as Duplicate.** |
| 5 Lifecycle | Not needed once TC-8003 closes as Duplicate. Lifecycle evaluation belongs to TC-7999. Product pages were not fetched. |
| 6 Already fixed | No resolved (Closed/Done) sibling. Not applicable. |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured). |
| 7.5 Release Jira | Not applicable. TC-8003 creates no remediation, so no release Jira linking is needed. |
| 8 Remediation | None from TC-8003. Case A/B/C are superseded by the Duplicate closure. |

## Proposed Jira mutations for TC-8003 (each needs engineer confirmation; none executed)

1. Assign TC-8003 to the current user.
2. Transition New -> Assigned (Step 0.8).
3. Add the duplicate comment, including the Comment Footnote:
   "Duplicate of TC-7999 — same CVE tracked for the same stream 2.2.x. Version impact analysis confirms overlap."
4. Transition to Closed with resolution **Duplicate**.
5. Optionally link TC-8003 to TC-7999 (Duplicate/Related).
6. Add the `ai-cve-triaged` label.
7. Post the post-triage summary comment, including the Comment Footnote. It contains the version impact table, a note that no Affects Versions correction was made (duplicate closure), the outcome "Closed as Duplicate of TC-7999", "no remediation tasks created", "no release Jira", "no dedup", and an @mention of the issue reporter. The reporter is not given in the mock data, so it would be taken from the live Jira issue.

No VEX Justification is set. VEX applies only to "Not a Bug / not affected" closures.

## Follow-ups for the TC-7999 owner (advisory, no mutation by this triage)

- **Add RHTPA 2.2.2** to TC-7999's Affects Versions. 2.2.2 is a backend retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12) and is therefore affected.
- **Remediation path for 2.2.x.** `release/0.4.z` tags v0.4.11 and later already ship quinn-proto 0.11.14, which suggests the fix is upstream. Remediation is likely the "dependency bump / fix available" variant, and 2.2.3 and later already ship the fix. Confirm by checking branch HEAD.
- **Stream 2.1.x is affected and untracked.** 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9, and no 2.1.x sibling was found. Handle this through TC-7999's Case A (cross-stream comment plus preemptive tasks) or a PSIRT-created `[rhtpa-2.1]` issue.
- The due date of 2026-07-15 has already passed.
