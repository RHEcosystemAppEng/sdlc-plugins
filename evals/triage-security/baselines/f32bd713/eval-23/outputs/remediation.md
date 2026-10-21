# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case B** (Affected -- create remediation tasks) applies to the 2.2.x stream.
- **Case A** (Cross-stream impact) applies: the 2.1.x stream is also affected but is outside the issue scope `[rhtpa-2.2]`. Preemptive remediation tasks are created for 2.1.x.

### Scoped stream (2.2.x) -- Dependency Bump variant

Upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version). The dependency bump variant applies (2 tasks).

### Cross-stream (2.1.x) -- Preemptive, Upstream Backport variant

Upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (vulnerable). The upstream backport variant applies (2 preemptive tasks).

---

## Remediation Task 1: Dependency Bump -- quinn-proto (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend (inward: TC-8001, outward: this task)

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

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

## Remediation Task 2: Downstream Propagation -- backend ref in rhtpa-release.0.4.z (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend (inward: TC-8001, outward: this task); Blocks (inward: Task 1, outward: this task)

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Remediation Task 1 (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 3 (Preemptive): Upstream Backport -- quinn-proto (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related (inward: TC-8001, outward: this task) -- preemptive, originating CVE is from 2.2.x stream

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto vulnerability (panic on large stream counts).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
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

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 4 (Preemptive): Downstream Propagation -- backend ref in rhtpa-release.0.3.z (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related (inward: TC-8001, outward: this task); Blocks (inward: Task 3, outward: this task)

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Remediation Task 3 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact Comment (for TC-8001)

Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. The 2.1.x stream is tracked by preemptive remediation tasks (see Related links) and may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: Remediation Task 3 (upstream backport, security-preemptive), Remediation Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x = 2 tasks (dependency bump + downstream propagation); 2.1.x = 2 preemptive tasks (upstream backport + downstream propagation). Matches ecosystem classification table (source dependency = 2 tasks per stream).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created since no sibling CVE Jira exists for that stream.
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks to TC-8001); "Related" for preemptive tasks linked to the originating CVE Jira (2.1.x tasks to TC-8001); "Blocks" for upstream to downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task's Implementation Notes includes `customer-shipped` guidance: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
- [x] **Deployment context source**: The `customer-shipped` deployment context was resolved from the Source Repositories table in CLAUDE.md, where `rhtpa-backend` is listed with Deployment Context = `customer-shipped`.

## Link Topology Summary

```
TC-8001 (CVE Vulnerability)
  |-- Depend --> Task 1 (Dependency Bump, 2.2.x)
  |-- Depend --> Task 2 (Downstream Propagation, 2.2.x)
  |-- Related --> Task 3 (Upstream Backport, 2.1.x, preemptive)
  |-- Related --> Task 4 (Downstream Propagation, 2.1.x, preemptive)

Task 1 (Dependency Bump) -- Blocks --> Task 2 (Downstream, 2.2.x)
Task 3 (Upstream Backport) -- Blocks --> Task 4 (Downstream, 2.1.x)
```
