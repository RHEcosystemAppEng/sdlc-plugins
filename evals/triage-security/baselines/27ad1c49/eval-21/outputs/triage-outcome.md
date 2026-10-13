# Triage Outcome for TC-8020

## Summary

**Issue**: TC-8020 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Affected range**: < 0.11.14
**Fixed version**: 0.11.14
**CVSS**: 7.5 (High)
**Stream scope**: 2.2.x

## Triage Decision: Remediation Required (Case B) -- Blocked by Concurrent Triage (Step 7)

### Version Impact Summary

Within the 2.2.x stream (this issue's scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.4 | 0.11.14 | NO | fixed |

Three versions (2.2.0, 2.2.1, 2.2.2) within the issue's scoped stream are affected. This means the triage outcome is **Case B: Affected -- create remediation tasks** (not Case C, which applies only when no supported versions are affected).

### Cross-Stream Impact (Case A)

Because this is a scoped issue (`[rhtpa-2.2]`) and the 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), **Case A applies** before Case B:

- A cross-stream impact comment would be posted to TC-8020 noting that 2.1.x versions are also affected.
- The skill would check for an existing sibling CVE Jira for the 2.1.x stream (same CVE label, stream suffix `[rhtpa-2.1]`).
- If no sibling exists, preemptive remediation tasks would be created for the 2.1.x stream with the `security-preemptive` label and "Related" link type.
- If a sibling exists, the 2.1.x stream is handled via its own CVE Jira.

### Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Proposed (scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1
- The correction requires engineer confirmation and a comment documenting the change with lock-file evidence.

### Concurrent Triage Block (Step 7)

**The triage is currently blocked at Step 7.** A concurrent triage was detected:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and also targets the same upstream component (`quinn-proto`).
- The engineer must choose one of three options before remediation can proceed:
  1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap.
  2. **Skip** -- skip task creation entirely; add a comment explaining the skip.
  3. **Proceed** -- create tasks with `concurrent-triage-overlap` label for later dedup.

### What Happens After the Engineer Decides

#### If the engineer chooses "Wait":
- Triage pauses. When TC-8019 completes, the engineer re-runs triage for TC-8020.
- Step 4.3 (cross-CVE overlap detection) will search for TC-8019's remediation tasks that bump quinn-proto. If any task bumps quinn-proto to >= 0.11.14, it already covers TC-8020's fix threshold, and no new remediation task is needed -- TC-8020 can be linked to the existing task and potentially closed.

#### If the engineer chooses "Skip":
- No remediation tasks are created for TC-8020.
- A Jira comment is posted on TC-8020 explaining that task creation was skipped due to concurrent triage on the same upstream component (TC-8019).
- Affects Versions correction (Step 3) and sibling/duplicate checks (Step 4) still apply.

#### If the engineer chooses "Proceed":
- The `concurrent-triage-overlap` label is added to TC-8020.
- Step 7.5 (Release Jira Orchestration) runs: find or create release Epic and release Task for the 2.2.x stream, then check cross-CVE dedup (Step 7.5.3).
- Step 8 proceeds with Case A + Case B:

  **Case A (cross-stream impact)**:
  - Post cross-stream impact comment on TC-8020.
  - Check for 2.1.x sibling CVE Jira.
  - Create preemptive remediation tasks for 2.1.x if no sibling exists.

  **Case B (remediation for 2.2.x)**:
  - Ecosystem: Cargo (source dependency) -- 2 tasks per stream.
  - Task 1: Upstream backport or dependency bump -- bump quinn-proto to >= 0.11.14 in the backend repository on branch `release/0.4.z`.
  - Task 2: Downstream propagation -- update the backend source reference in `rhtpa-release.0.4.z` to pick up the fix.
  - Both tasks linked to TC-8020 with "Depend" link type.
  - Downstream task blocked by upstream task ("Blocks" link type).
  - Both tasks linked to the release Task ("Blocks").
  - TC-8020 linked to the release Task ("Related").

  **Post-triage actions**:
  - Add `ai-cve-triaged` label to TC-8020.
  - Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter.

### Ecosystem and Remediation Approach

- **Ecosystem**: Cargo (quinn-proto is a Rust crate)
- **Remediation approach**: Depends on Step 2.5 (upstream fix check):
  - If the upstream branch (`release/0.4.z`) already ships quinn-proto >= 0.11.14: **dependency bump** variant (run `cargo update -p quinn-proto`) + downstream propagation.
  - If the upstream branch does NOT yet ship the fix: **upstream backport** (PR to bump quinn-proto on the upstream branch) + downstream propagation.
- Based on the mock data, version 2.2.3 (tag v0.4.11) already ships quinn-proto 0.11.14, suggesting the upstream branch `release/0.4.z` likely already has the fix. In that scenario, the dependency bump variant would apply.

### Key Findings

1. **PSIRT Affects Versions are incorrect**: RHTPA 2.0.0 does not exist in the version streams. The correct scoped Affects Versions are RHTPA 2.2.0 and RHTPA 2.2.1.
2. **Partial impact within the scoped stream**: Only 2.2.0, 2.2.1, and 2.2.2 (retag) are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version.
3. **Cross-stream impact exists**: The 2.1.x stream is also affected and may require preemptive remediation tasks or a separate CVE Jira.
4. **Concurrent triage blocks remediation**: TC-8019 is actively triaging the same upstream component (quinn-proto). The engineer must decide how to coordinate before remediation tasks can be created, to avoid duplicate work.
