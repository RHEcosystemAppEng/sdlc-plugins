# Step 7 - Remediation

## Triage Outcome

**Case A + Case B**: The 2.2.x stream (issue scope) has affected versions that need remediation. Additionally, the 2.1.x stream (outside issue scope) is also affected, requiring a cross-stream impact notice.

### Affected versions within scope (2.2.x)

| Version | quinn-proto | Status |
|---------|-------------|--------|
| 2.2.0 | 0.11.9 | Affected |
| 2.2.1 | 0.11.12 | Affected |
| 2.2.2 | 0.11.12 | Affected (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | Already fixed |
| 2.2.4 | 0.11.14 | Already fixed |

### Cross-stream impact (2.1.x, outside scope)

| Version | quinn-proto | Status |
|---------|-------------|--------|
| 2.1.0 | 0.11.9 | Affected |
| 2.1.1 | 0.11.9 | Affected |

## Ecosystem Determination

quinn-proto is a **Cargo** (source dependency) ecosystem package. Per the remediation templates, this requires **two tasks**: an upstream backport task and a downstream propagation subtask.

However, the upstream fix is **already present** on `release/0.4.z` -- tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14. The affected versions (2.2.0, 2.2.1, 2.2.2) shipped older tags (v0.4.5, v0.4.8) that predate the fix. Since the fix is already on the upstream branch, the upstream backport task is not needed. Only a downstream propagation task is required to update the Konflux release repo references.

Since 2.2.3 and 2.2.4 already ship the fixed version, the affected versions (2.2.0-2.2.2) are historical releases. The remediation question is whether a patch release needs to be issued for the 2.2.x stream. Given that 2.2.3+ already includes the fix, no new upstream work is required, but the triage should still create remediation tasks to formally track the resolution.

## Remediation Tasks

### Task 1: Upstream Backport Task (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is already present on release/0.4.z at HEAD (v0.4.11+ ships quinn-proto 0.11.14). This task tracks verification that the fix is included.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- The fix is already present at branch HEAD (tags v0.4.11, v0.4.12 ship 0.11.14)
- Verify the dependency was bumped as part of a prior update
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges (or is verified as already present),
update the source pinning in this Konflux release repo so the next build
ships the fix.

Note: Tags v0.4.11+ already include the fix. Affected releases (2.2.0, 2.2.1, 2.2.2) used older tags (v0.4.5, v0.4.8). If a patch release is needed for the 2.2.x stream, the backend reference should be set to v0.4.11 or later.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag (v0.4.11+)
- Verify the Konflux build pipeline triggers successfully
- The fix is already available at v0.4.11 and v0.4.12

## Acceptance Criteria

- [ ] backend reference updated to include the fix (tag >= v0.4.11)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Cross-Stream Impact Comment (Case B)

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.

Version evidence:
- RHTPA 2.1.0 (v0.3.8): quinn-proto 0.11.9 (vulnerable)
- RHTPA 2.1.1 (v0.3.12): quinn-proto 0.11.9 (vulnerable)

The 2.1.x stream is tracked by the Konflux release repo rhtpa-release.0.3.z.
This stream may require a separate PSIRT triage issue or companion tracker.
```

## Jira Linkage (proposed)

1. Link upstream task to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<upstream-task-key>", type: "Depend")
   ```

2. Link downstream subtask to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")
   ```

3. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")
   ```

4. Transition TC-8001 to In Progress.

5. Assign TC-8001 to current user.

6. Add `ai-cve-triaged` label to TC-8001.

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8001:

```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

### Triage Outcome

Remediation tasks created:
- <upstream-task-key>: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
- <downstream-task-key>: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
  (blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (quinn-proto 0.11.9 in both 2.1.0 and 2.1.1).
```
