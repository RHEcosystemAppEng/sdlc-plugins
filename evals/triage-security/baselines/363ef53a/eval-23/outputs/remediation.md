# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Decision

- **Issue scope**: stream 2.2.x (suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Deployment context**: customer-shipped
- **Affected versions in scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in scope (2.2.x)**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 also affected

### Upstream Fix Status

- **Stream 2.2.x** (release/0.4.z): Fix **available** -- v0.4.11+ ships quinn-proto 0.11.14. Remediation uses the **dependency bump** variant.
- **Stream 2.1.x** (release/0.3.z): Fix **not available** -- latest tag v0.3.12 ships quinn-proto 0.11.9. Remediation uses the **upstream backport** variant.

### Case Determination

- **Case A (cross-stream impact)**: Stream 2.1.x is also affected but outside the issue's 2.2.x scope. Proactive remediation tasks are created for 2.1.x as preemptive tasks.
- **Case B (affected -- create remediation tasks)**: Versions 2.2.0, 2.2.1, 2.2.2 in the issue's 2.2.x scope are affected. Remediation tasks created for 2.2.x.

---

## Stream 2.2.x — Remediation Tasks (In-Scope)

Upstream fix is available on release/0.4.z. Using the **dependency bump + downstream propagation** template (2 tasks).

### Task 1: Dependency Bump (stream 2.2.x)

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (stream 2.2.x)

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Stream 2.1.x — Remediation Tasks (Cross-Stream, Preemptive)

> **Preemptive remediation**: These tasks were created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> these tasks will be linked and the `security-preemptive` label removed.

Upstream fix is **not** available on release/0.3.z. Using the **upstream backport + downstream propagation** template (2 tasks). Labels include `security-preemptive`. Link type is "Related" (not "Depend") to TC-8001.

### Task 3: Upstream Backport (stream 2.1.x, preemptive)

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue, Related link -- preemptive)

Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

---

### Task 4: Downstream Propagation (stream 2.1.x, preemptive)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue, Related link -- preemptive)

Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

---

## Jira Linkage Summary

### Stream 2.2.x (in-scope, standard)

| From | To | Link Type |
|------|----|-----------|
| TC-8001 | Dependency bump task (2.2.x) | Depend |
| TC-8001 | Downstream propagation task (2.2.x) | Depend |
| Dependency bump task | Downstream propagation task (2.2.x) | Blocks |

### Stream 2.1.x (cross-stream, preemptive)

| From | To | Link Type |
|------|----|-----------|
| TC-8001 | Upstream backport task (2.1.x) | Related |
| TC-8001 | Downstream propagation task (2.1.x) | Related |
| Upstream backport task | Downstream propagation task (2.1.x) | Blocks |

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (dependency bump or upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive remediation tasks created
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x); "Related" for preemptive tasks linked to TC-8001 from another stream (2.1.x); "Blocks" for upstream-to-downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: Each task's Implementation Notes includes "customer-shipped" guidance (coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure)
- [x] **Release Jira linking**: To be linked after Step 7.5 release Jira orchestration
- [x] **Dedup consistency**: No dedup detected -- all tasks are new
