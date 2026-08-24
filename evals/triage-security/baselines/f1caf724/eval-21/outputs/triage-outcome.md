# Triage Outcome -- TC-8020 (CVE-2026-31812)

## Issue Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |
| 2.2.0 | 2.2.x | 0.11.9 | YES |
| 2.2.1 | 2.2.x | 0.11.12 | YES |
| 2.2.2 | 2.2.x | -- | YES (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO (fixed) |

## Triage Decision: Case A + Case B (pending Step 7 resolution)

### Case B -- Remediation Required (scoped stream 2.2.x)

Supported versions within the issue's scoped stream (2.2.x) are affected: versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto below the fix threshold (0.11.14). Versions 2.2.3 and 2.2.4 already include the fix and are NOT affected.

**Ecosystem**: Cargo (source dependency) -- this requires **2 tasks** for the 2.2.x stream:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `rhtpa-backend` repository on `release/0.4.z` branch.
2. **Downstream propagation task**: Update the rhtpa-backend source reference in the `rhtpa-release.0.4.z` Konflux release repo. Blocked by the upstream task.

### Case A -- Cross-Stream Impact (2.1.x also affected)

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected: both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9.

Per Case A, a cross-stream impact comment would be posted on TC-8020:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for the 2.1.x stream, proactive (preemptive) remediation tasks would be created for 2.1.x with the `security-preemptive` label and "Related" link type back to TC-8020.

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect -- there is no 2.0.x stream in the configuration. The correction for the scoped stream (2.2.x) would be:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version (0.11.14).

## Step 7 -- Concurrent Triage Block

Triage is **blocked at Step 7** before remediation task creation can proceed. A concurrent triage was detected:

- **TC-8019** is `In Progress`, assigned to `engineer-b@example.com`, and affects the same upstream component (`quinn-proto` via `customfield_10632`).

The user must choose one of three options before Case A/B remediation tasks are created:

1. **Wait** -- pause until TC-8019's triage completes, then re-run Step 4.3 to detect overlap (recommended -- TC-8019's remediation may already cover TC-8020's fix threshold)
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label so TC-8019's Step 4.3 picks up the overlap

### Why "Wait" is recommended

Both TC-8019 and TC-8020 affect `quinn-proto`. If TC-8019's remediation bumps quinn-proto to >= 0.11.14, that fix would also satisfy TC-8020's fix threshold. Step 4.3 (Cross-CVE overlap detection) would detect this and recommend closing TC-8020 as already covered -- avoiding duplicate remediation tasks. Waiting avoids creating redundant upstream backport and downstream propagation tasks that would target the same repository branches.

## Post-Triage Actions (after Step 7 resolution)

Once the user resolves the Step 7 block, the following actions complete the triage:

1. **Add label** `ai-cve-triaged` to TC-8020
2. **Post summary comment** on TC-8020 with version impact table, Affects Versions correction, triage outcome, and links to created remediation tasks (if any)
3. **Transition** TC-8020 to In Progress (if remediation tasks were created) or Closed (if covered by TC-8019's remediation via overlap detection)
