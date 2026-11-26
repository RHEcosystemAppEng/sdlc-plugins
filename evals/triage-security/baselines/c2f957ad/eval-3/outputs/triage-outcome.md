# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto) [rhtpa-2.2]

## Decision: Close as Duplicate of TC-7999

TC-8003 is a **same-stream duplicate**. TC-7999 tracks the same CVE (CVE-2026-31812),
the same component (`pscomponent:org/rhtpa-server`), and the same stream suffix
`[rhtpa-2.2]` (stream 2.2.x). TC-7999 is already **In Progress**. Step 4.1 says that
when a same-stream sibling is open or in progress, the current issue is closed as
Duplicate.

## Rationale

1. **Same CVE, same stream.** Both issues carry label CVE-2026-31812 and suffix
   `[rhtpa-2.2]`. PSIRT creates one issue per stream on purpose, so a second issue
   for the same stream is redundant, not a companion tracker.
2. **Versions are covered.** TC-8003 claims [RHTPA 2.2.0]. TC-7999 claims [RHTPA 2.2.0,
   RHTPA 2.2.1], which contains all of TC-8003's scope.
3. **Version impact confirms overlap.** For stream 2.2.x, lock files show quinn-proto
   0.11.9 (2.2.0), 0.11.12 (2.2.1), 0.11.12 (2.2.2, retag of 2.2.1), and 0.11.14 (2.2.3,
   2.2.4). The affected 2.2.x versions are 2.2.0, 2.2.1, and 2.2.2. They are the same
   exposure that TC-7999 tracks.
4. **The sibling is active.** TC-7999 is In Progress, so remediation is already
   underway. Creating tasks from TC-8003 would duplicate that work.

## Proposed Jira mutations on TC-8003 (each needs engineer confirmation; none executed)

| # | Action | Detail |
|---|--------|--------|
| 1 | Assign | Current user (Step 0.8 / Step 4.1) |
| 2 | Comment | "Duplicate of TC-7999 – same CVE tracked for the same stream 2.2.x. Version impact analysis confirms overlap." Includes the version impact summary and the triage-security Comment Footnote. |
| 3 | Transition | Closed, resolution **Duplicate** (target status name found dynamically via get_transitions) |
| 4 | Link (recommended) | TC-8003 to TC-7999 (duplicate relationship) |
| 5 | Label | Add `ai-cve-triaged` |
| 6 | Summary comment | Post-triage summary: version impact table, outcome = closed as Duplicate of TC-7999, no remediation tasks created, @mention of the issue reporter, Comment Footnote |

## Steps intentionally not performed for TC-8003

- **Step 3 (Affects Versions correction):** The evidence-backed scope would be
  [RHTPA 2.2.0, 2.2.1, 2.2.2], compared with the current [RHTPA 2.2.0]. Correcting a
  duplicate that is being closed adds nothing, so the correction is reported but not
  applied.
- **Steps 5–8 (lifecycle, already-fixed, concurrent triage, release Jira,
  remediation):** Not run. The duplicate closure ends triage. No remediation Tasks,
  release Epic/Task, or preemptive tasks are created from TC-8003. Step 6 would not
  apply anyway, because TC-7999 is In Progress, not Closed/Done. Steps 4.3 and 7 are
  also not configured (no Upstream Affected Component field).
- **Case C / VEX:** Not applicable. The product IS affected, so a VEX justification
  must not be set on this Duplicate closure.

## Follow-up recommendations for the engineer (canonical issue TC-7999)

1. **Missing Affects Version on TC-7999:** RHTPA 2.2.2 (backend `v0.4.8`, retag of
   2.2.1, quinn-proto 0.11.12) is affected but not listed on TC-7999. Recommend adding
   RHTPA 2.2.2.
2. **Cross-stream impact on 2.1.x:** RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9
   (affected), and no 2.1.x CVE issue was found. TC-7999's triage should apply Case A:
   a cross-stream impact comment plus preemptive `security-preemptive` remediation
   tasks for 2.1.x (upstream backport on `release/0.3.z` plus downstream propagation).
3. **2.2.x remediation path:** `release/0.4.z` already ships quinn-proto 0.11.14 as of
   tag v0.4.11 (RHTPA 2.2.3+). The fix is available upstream. Remediation under TC-7999
   is mainly about shipping a fixed build to users still on 2.2.0–2.2.2, or confirming
   that 2.2.3+ is the fix release.
4. **Data quality caveats:** The security matrix is 151 days old. External CVE
   enrichment (MITRE/OSV) and development-stream (branch HEAD) checks were not
   performed in this eval. Neither affects the Duplicate decision.
