# Triage Outcome: TC-8020

## Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (Rust crate)

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream (2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

PSIRT assigned `RHTPA 2.0.0`, which does not exist in any configured version stream. Correction scoped to the 2.2.x stream:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version (0.11.14).

## Concurrent Triage Detection (Step 7)

**Concurrent triage detected.** TC-8019 is currently In Progress, assigned to engineer-b@example.com, and affects the same upstream component (`quinn-proto` via `customfield_10632`).

The engineer must choose before proceeding to Step 8:

1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation; add explanatory Jira comment
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label for deduplication

**This decision gates entry to Step 8.** No Case A/B/C branching occurs until the engineer selects an option.

## Triage Decision (Step 8) -- Pending Concurrent Triage Resolution

The triage outcome depends on the engineer's choice in Step 7. The following describes what would happen for each option:

### If engineer chooses "Proceed" (Option 3)

The issue falls into **Case A** (Affected -- create remediation tasks) with **Case B** (Cross-stream impact) applying as well:

**Case A -- Remediation tasks for in-scope stream 2.2.x:**

Since quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** would be created per affected stream:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `rhtpa-backend` source repository on branch `release/0.4.z`. Labels would include `concurrent-triage-overlap` alongside standard security labels.
2. **Downstream propagation subtask**: Update the backend source reference in `rhtpa-release.0.4.z` to a tag containing the bumped dependency. Blocked by the upstream task.

Both tasks would be linked to TC-8020 with "Depend" link type and carry the `concurrent-triage-overlap` label so that TC-8019's engineer can detect the overlap via Step 4.3 cross-CVE overlap detection.

**Case B -- Cross-stream impact (2.1.x):**

The issue is scoped to 2.2.x, but lock file analysis shows the 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted to TC-8020. If no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks (with `security-preemptive` label) would be created for stream 2.1.x.

### If engineer chooses "Wait" (Option 1)

Execution pauses. The engineer should re-run triage after TC-8019 completes. At that point, Step 4.3 cross-CVE overlap detection would check whether TC-8019's remediation tasks already bump quinn-proto to >= 0.11.14, potentially covering TC-8020 without needing new tasks.

### If engineer chooses "Skip" (Option 2)

No remediation tasks are created. A Jira comment is added to TC-8020 explaining that task creation was skipped due to concurrent triage on TC-8019 for the same upstream component (quinn-proto). The `ai-cve-triaged` label is still added, and the post-triage summary documents the skip decision.

## Key Findings

1. **PSIRT Affects Versions is incorrect**: RHTPA 2.0.0 does not exist in any configured stream. Must be corrected to RHTPA 2.2.0, 2.2.1, 2.2.2.
2. **Partial fix already shipped**: Versions 2.2.3+ already include quinn-proto 0.11.14 (the fix). Only 2.2.0, 2.2.1, and 2.2.2 need remediation.
3. **Cross-stream impact**: The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9).
4. **Concurrent triage blocks task creation**: TC-8019 is actively being triaged for the same component. The engineer must decide how to handle potential duplicate remediation before tasks can be created.
