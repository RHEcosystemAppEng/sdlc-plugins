# Triage Outcome -- TC-8020

## Summary

Triage of TC-8020 (CVE-2026-31812, quinn-proto < 0.11.14) progressed through Steps 0-7 normally. The version impact analysis (Step 2) determined that versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream are affected, while versions 2.2.3 and 2.2.4 ship the patched quinn-proto 0.11.14.

## Step 7 -- Concurrent Triage Detection Halted Progress

At Step 7, the concurrent triage detection check identified that **TC-8019** is currently in progress and targets the same upstream component (`quinn-proto`). TC-8019 is assigned to `engineer-b@example.com` and has status `In Progress`.

This check runs **before** Case A/B/C branching in Step 8. Because a concurrent triage exists, the skill pauses and presents three options to the engineer before proceeding further:

1. **Wait** -- Pause until TC-8019's triage completes. Re-running triage afterward allows Step 4.3 (cross-CVE overlap detection) to check whether TC-8019's remediation tasks already cover the fix threshold for this CVE (quinn-proto >= 0.11.14). This is the safest option to avoid duplicate remediation tasks.

2. **Skip** -- Skip remediation task creation entirely for TC-8020. A comment is posted on TC-8020 documenting that task creation was skipped due to concurrent triage of the same upstream component by TC-8019. The remaining triage artifacts (Affects Versions correction, ai-cve-triaged label, summary comment) are still applied.

3. **Proceed** -- Continue to Step 8 Case A/B/C branching and create remediation tasks, but add the `concurrent-triage-overlap` label to TC-8020. This label serves as a signal so that when the other engineer's triage of TC-8019 reaches Step 4.3 (cross-CVE overlap detection), it will detect the overlap and handle it appropriately -- either by linking to the existing remediation or by flagging the duplicate.

## Decision Pending

No Jira mutations beyond Step 7 have been proposed. The triage outcome (Case A: cross-stream impact with preemptive tasks, Case B: remediation task creation, or Case C: close as not affected) depends on the engineer's choice at the Step 7 gate.

## Version Impact Context

For reference, the version impact analysis from Step 2:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

If the engineer proceeds (Option 3) or waits and re-runs (Option 1), Step 8 would follow Case B (affected versions exist in the scoped stream), creating two remediation tasks for Cargo ecosystem: an upstream backport task and a downstream propagation subtask. Case A (cross-stream impact) would also apply if the 2.1.x stream is confirmed affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the affected range).
