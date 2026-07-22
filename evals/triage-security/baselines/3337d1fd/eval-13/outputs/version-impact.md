# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x  | 2.1.0   | 0.3.8  | `v0.3.8`   | 0.11.9      | YES       |       |
| 2.1.x  | 2.1.1   | 0.3.12 | `v0.3.12`  | 0.11.9      | YES       |       |
| 2.2.x  | 2.2.0   | 0.4.5  | `v0.4.5`   | 0.11.9      | YES       |       |
| 2.2.x  | 2.2.1   | 0.4.8  | `v0.4.8`   | 0.11.12     | YES       |       |
| 2.2.x  | 2.2.2   | 0.4.9  | `v0.4.8`   | --          | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x  | 2.2.3   | 0.4.11 | `v0.4.11`  | 0.11.14     | NO        | ships fixed version |
| 2.2.x  | 2.2.4   | 0.4.12 | `v0.4.12`  | 0.11.14     | NO        | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

The dependency is a Cargo crate in the backend repository. Remediation follows the source dependency ecosystem path: upstream backport task + downstream propagation subtask.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | quinn-proto at Latest Tag | Fixed? |
|--------|-----------|-----------------|--------------------|----|--------|
| 2.1.x  | Cargo     | `release/0.3.z` | `v0.3.12`          | 0.11.9  | NO     |
| 2.2.x  | Cargo     | `release/0.4.z` | `v0.4.12`          | 0.11.14 | YES    |

### Analysis

- **2.2.x stream (issue-scoped)**: The upstream branch `release/0.4.z` already includes the fix (quinn-proto 0.11.14 since tag `v0.4.11`). The Konflux releases 2.2.3 and 2.2.4 already ship the fixed version. No new remediation task is needed for this stream -- the fix was already propagated to the latest releases. Affected versions 2.2.0, 2.2.1, and 2.2.2 are superseded by the fixed 2.2.3+ releases.

- **2.1.x stream (cross-stream)**: All versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range. The upstream branch `release/0.3.z` does NOT have the fix -- the latest tag (`v0.3.12`) still ships 0.11.9. Remediation is required: an upstream backport to `release/0.3.z` followed by a downstream propagation in the Konflux release repo.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which is incorrect -- no 2.0.x stream exists.

Since the issue is scoped to the **2.2.x stream**, the Affects Versions correction is scoped to 2.2.x versions only:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions RHTPA 2.2.3 and RHTPA 2.2.4 are excluded because they ship the fixed quinn-proto 0.11.14.

The 2.1.x versions (RHTPA 2.1.0, RHTPA 2.1.1) are also affected but belong to a different stream -- they would be tracked by a companion CVE Jira for the 2.1.x stream, or covered by preemptive remediation tasks (Case B).

## Cross-Stream Impact Summary

The issue is scoped to 2.2.x, but the 2.1.x stream is also fully affected. This triggers Case B (cross-stream impact) in Step 8 -- see remediation output for details.
