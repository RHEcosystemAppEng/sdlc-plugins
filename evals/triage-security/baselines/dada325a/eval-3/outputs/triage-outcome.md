# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision

**Close TC-8003 as Duplicate of TC-7999.** Create no remediation tasks for TC-8003.

## Rationale

1. **Same CVE, same stream.** TC-7999 has the label CVE-2026-31812 and the same stream suffix `[rhtpa-2.2]` (stream 2.2.x). Per Step 4.1, an open or in-progress same-stream sibling makes the current issue a duplicate.
2. **The sibling is active.** TC-7999 is In Progress, so the vulnerability is already being tracked and worked on.
3. **The versions are already covered.** TC-8003's only Affects Version (RHTPA 2.2.0) is already on TC-7999.
4. **The exposure is real but already owned.** The version impact analysis (simulated Cargo.lock data at pinned tags) shows 2.2.x versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14. Because the fix work belongs to TC-7999, this is not a "Not a Bug" closure and no VEX Justification is set.

## Version Impact Summary

| Version | quinn-proto | Affected |
|---------|-------------|----------|
| 2.1.0 | 0.11.9 | YES (other stream) |
| 2.1.1 | 0.11.9 | YES (other stream) |
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | same as 2.2.1 (retag) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

## Steps After the Duplicate Decision

- **Step 3 (Affects Versions):** the evidence supports [2.2.0, 2.2.1, 2.2.2], but the change is not applied to TC-8003 because it is being closed as a duplicate.
- **Step 5 (Lifecycle):** not needed. The issue closes as Duplicate, and the product pages URL was not fetched because external calls are forbidden.
- **Step 6 (Already Fixed):** no resolved sibling exists (TC-7999 is In Progress, not Closed/Done), so this check does not apply.
- **Step 7 / 7.5.3:** skipped, because the Upstream Affected Component field is not configured.
- **Step 7.5 / Step 8:** skipped for TC-8003. Release Jira linking, Case A, and Case B task creation all belong to the canonical issue TC-7999.

## Proposed Jira Mutations for TC-8003 (each needs engineer confirmation; none executed)

1. Assign TC-8003 to the current user (Step 0.8 and Step 4.1).
2. Transition New -> Assigned (Step 0.8), then -> Closed with resolution **Duplicate**.
3. Post a duplicate comment that cites TC-7999, stream [rhtpa-2.2], and the version impact evidence, and includes the Comment Footnote (skill `triage-security`).
4. Add the label `ai-cve-triaged`.
5. Post a post-triage summary comment containing:
   - the version impact table
   - the Affects Versions note (not corrected because of the duplicate closure)
   - the outcome: closed as Duplicate of TC-7999
   - remediation tasks: none
   - release Jira: none
   - an @mention of the issue reporter
   - the Comment Footnote

   Reporter account ID: the eval input has none; in a live run it comes from the Jira issue data.
6. Optional: link TC-8003 to TC-7999 (Duplicate/Related) for traceability.

## Follow-ups for the Engineer (not on TC-8003)

- **TC-7999 Affects Versions are incomplete.** They are missing **RHTPA 2.2.2**, a backend retag of 2.2.1 with quinn-proto 0.11.12, which is vulnerable. Recommend updating TC-7999 to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2], through the TC-7999 owner or by re-triaging TC-7999.
- **The 2.1.x stream is affected too** (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). The sibling search found no 2.1.x CVE issue. That cross-stream work (a Case A comment or preemptive tasks for 2.1.x) belongs to TC-7999's triage, or a future PSIRT `[rhtpa-2.1]` issue, rather than this duplicate.
- **The fix is already available upstream on 2.2.x.** v0.4.11 and later (2.2.3, 2.2.4) ship quinn-proto 0.11.14, so TC-7999's remediation is likely a dependency-bump variant, or simply a confirmation that 2.2.3 and later contain the fix.
- **The security matrix is stale.** It was last updated 2026-06-28 (131 days ago), so a refresh with `/setup` Step 10.6 is recommended.
- **Due date is past.** TC-8003's due date of 2026-07-15 has passed; TC-7999's due date should be checked.
- **External enrichment was skipped.** MITRE and OSV were not queried, so the 0.11.14 threshold comes from the Jira description only and confidence is reduced.
