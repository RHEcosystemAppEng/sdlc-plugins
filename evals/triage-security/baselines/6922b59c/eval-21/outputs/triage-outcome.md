# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High) -- Denial of Service
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

### Scoped stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream (2.1.x) -- outside issue scope

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

## Triage Decision

**Case B (Affected)** with **Case A (Cross-stream impact)** applies, but is **gated by Step 7 concurrent triage detection**.

### Rationale

1. **Affected versions exist in the scoped stream**: RHTPA 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below the 0.11.14 fix threshold. This triggers Case B (create remediation tasks).

2. **Cross-stream impact detected (Case A)**: Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9). Since TC-8020 is scoped to 2.2.x, the 2.1.x impact must be reported via a cross-stream comment. Proactive (preemptive) remediation tasks should be created for 2.1.x if no companion CVE Jira exists for that stream.

3. **Concurrent triage blocks immediate task creation (Step 7)**: TC-8019 is actively being triaged by engineer-b@example.com for the same upstream component (quinn-proto). The engineer must choose one of three options (wait, skip, or proceed with overlap label) before remediation tasks can be created.

4. **Fix is already present in later versions**: RHTPA 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). The fix was incorporated at build tag v0.4.11 (released 2026-03-23). This means the fix exists upstream; a dependency bump approach (Step 2.5 "fix available" variant) is appropriate rather than an upstream backport.

### Affects Versions Correction (Step 3)

- **Current (incorrect)**: RHTPA 2.0.0
- **Corrected**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Reason**: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis shows versions 2.2.0 through 2.2.2 are affected within the issue's scoped stream (2.2.x).

### Planned Actions (pending Step 7 resolution)

If the engineer chooses to **proceed** (Option 3) or **wait and re-triage** (Option 1, after TC-8019 completes):

#### For scoped stream 2.2.x (Case B):

Since the upstream fix is already available (quinn-proto 0.11.14 is shipped in later builds), the "fix available" variant applies:

1. **Task 1 -- Dependency bump**: Bump quinn-proto to >= 0.11.14 in the backend source repository (Cargo ecosystem). Uses `cargo update` to bump the dependency on the `release/0.4.z` branch.

2. **Task 2 -- Downstream propagation**: Propagate the bumped dependency into the Konflux release repo (rhtpa-release.0.4.z) via `artifacts.lock.yaml` update. Blocked by Task 1.

Both tasks linked to TC-8020 with "Depend" link type. If release Jira is active (Step 7.5), tasks are also linked to the release Task with "Blocks".

#### For cross-stream 2.1.x (Case A):

- Post cross-stream impact comment on TC-8020
- Check for existing companion CVE Jira for 2.1.x stream
- If no companion exists: create preemptive remediation tasks with `security-preemptive` label and "Related" link to TC-8020
- If companion exists: skip -- that stream's CVE Jira handles its own remediation

### If the engineer chooses to **skip** (Option 2):

- No remediation tasks created
- Comment added to TC-8020 documenting skip due to concurrent triage on TC-8019
- Triage can be revisited after TC-8019 completes

## Post-Triage Actions (after Step 7 resolution and remediation)

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment with version impact table, Affects Versions correction, triage outcome, remediation task links, and reporter mention
3. Transition issue status as appropriate

## Key Observations

- The PSIRT-assigned Affects Version (RHTPA 2.0.0) is incorrect -- no 2.0.x stream exists
- The vulnerability was already fixed in the 2.2.x stream starting with build v0.4.11 (RHTPA 2.2.3), meaning only older releases (2.2.0-2.2.2) require remediation
- The 2.1.x stream is fully affected across all versions and requires either a companion CVE Jira or preemptive remediation
- Concurrent triage on TC-8019 for the same component (quinn-proto) must be resolved before creating remediation tasks to avoid duplicates
