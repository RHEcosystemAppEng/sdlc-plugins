# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A**: Cross-stream impact -- stream 2.1.x is also affected but this issue is scoped to 2.2.x
- **Case B**: Affected -- create remediation tasks for the scoped stream (2.2.x)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation)
- **Deployment context**: customer-shipped

## Remediation Tasks for Stream 2.2.x (Scoped -- Standard Tasks)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend on TC-8001

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend on TC-8001; Blocked by upstream backport task (Task 1)

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
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

- Depends on: Upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream -- Case A)

Stream 2.1.x does not have its own CVE Jira for CVE-2026-31812. These preemptive tasks are created proactively from the cross-stream impact analysis of TC-8001 (stream 2.2.x).

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001 (not Depend, because this is a different stream)

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
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

- Related to: TC-8001 (originating CVE, stream 2.2.x)

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001; Blocked by upstream backport task (Task 3)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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

- Blocked by: Upstream backport task (Task 3) (upstream backport must merge first)
- Related to: TC-8001 (originating CVE, stream 2.2.x)

---

## Cross-Stream Impact Comment (for TC-8001)

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9 which is within the affected range.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: Task 3 (upstream backport, security-preemptive), Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

## Summary of All Remediation Tasks

| # | Type | Stream | Repository | Target Branch | Labels | Link to TC-8001 |
|---|------|--------|------------|---------------|--------|-----------------|
| 1 | Upstream backport | 2.2.x | rhtpa-backend | release/0.4.z | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation | 2.2.x | rhtpa-release.0.4.z | main | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (preemptive) | 2.1.x | rhtpa-backend | release/0.3.z | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (preemptive) | 2.1.x | rhtpa-release.0.3.z | main | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

All four remediation task descriptions include the **Coordination Guidance** subsection under Implementation Notes with the `customer-shipped` deployment context guidance: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
