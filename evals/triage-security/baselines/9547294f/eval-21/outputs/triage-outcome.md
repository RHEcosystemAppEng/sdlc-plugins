# Triage Outcome -- TC-8020

## Summary

Triage of TC-8020 (CVE-2026-31812, quinn-proto < 0.11.14) proceeded through Steps 0-7. The version impact analysis (Step 2) determined that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected, while versions 2.2.3 and 2.2.4 ship the patched version 0.11.14.

## Step 7 -- Concurrent Triage Detection (Blocking)

At Step 7, concurrent triage detection identified that **TC-8019** is actively being triaged (status: In Progress, assignee: engineer-b@example.com) and affects the **same upstream component** (quinn-proto, via `customfield_10632`).

This concurrent triage warning was presented to the engineer before proceeding to Step 8 (Case A/B/C branching). The triage outcome depends on the engineer's selection:

### Option 1: Wait (Recommended)

If the engineer chooses to **wait**:
- Triage pauses until TC-8019's triage completes
- Upon resumption, Step 4.3 (cross-CVE overlap detection) is re-run to check whether TC-8019's remediation already covers the quinn-proto fix threshold (0.11.14)
- If TC-8019's remediation bumps quinn-proto to >= 0.11.14, TC-8020 can be closed as already covered
- If TC-8019's remediation does not cover the threshold, standard remediation tasks are created

### Option 2: Skip

If the engineer chooses to **skip**:
- No remediation tasks are created for TC-8020
- A Jira comment is posted: "Remediation task creation skipped due to concurrent triage TC-8019 (In Progress) on the same upstream component (quinn-proto). Re-run triage after TC-8019 completes."
- The `ai-cve-triaged` label is still applied to mark the issue as reviewed

### Option 3: Proceed with Overlap Label

If the engineer chooses to **proceed**:
- The `concurrent-triage-overlap` label is added to TC-8020
- Triage continues to Case A (affected versions exist in the 2.2.x stream)
- Standard remediation tasks are created:
  - Upstream backport task: bump quinn-proto to >= 0.11.14 in backend repo on branch `release/0.4.z`
  - Downstream propagation subtask: update backend reference in rhtpa-release.0.4.z
- The `concurrent-triage-overlap` label signals to TC-8019's triage (via Step 4.3) that overlapping remediation may exist

## Version Impact Context

For reference, the version impact analysis from Step 2:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Versions 2.2.0 through 2.2.2 ship quinn-proto versions below the fix threshold of 0.11.14 and are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## Proposed Actions (Pending Engineer Decision)

All proposed actions are contingent on the engineer's choice at the Step 7 concurrent triage gate:

1. **Affects Versions Correction** (Step 3): Proposed change from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` based on lock file evidence. Version names are from the supportability matrix, resolved dynamically via Jira version registry.

2. **Remediation Task Creation** (Step 8, if proceeding): Two tasks following Cargo ecosystem two-task pattern:
   - Upstream backport: Remediate CVE-2026-31812 -- bump quinn-proto to 0.11.14 (rhtpa-2.2)
   - Downstream propagation: Propagate CVE-2026-31812 fix -- update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

3. **Label Addition**: `ai-cve-triaged` label applied to TC-8020 after triage completes.

4. **Post-Triage Summary Comment**: Summary comment posted to TC-8020 documenting the version impact table, Affects Versions correction, triage outcome, and remediation task links.
