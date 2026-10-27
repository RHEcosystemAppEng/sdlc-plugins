# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Decision

- **Issue scope**: 2.2.x stream (summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Deployment context**: customer-shipped

### 2.2.x Stream (Scoped)

Versions 2.2.0, 2.2.1, and 2.2.2 are affected. However, versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). The upstream branch `release/0.4.z` already ships the fix at its latest tag (v0.4.12). Since the fix is already available upstream, the dependency bump variant applies (rather than upstream backport).

**Case B**: Affected versions exist within the scoped stream. Create remediation tasks for the 2.2.x stream using the dependency bump variant (upstream fix is already available per Step 2.5).

### 2.1.x Stream (Cross-Stream Impact -- Case A)

All 2.1.x versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` does NOT ship the fix (latest tag v0.3.12 ships quinn-proto 0.11.9). Since the issue is scoped to 2.2.x, the 2.1.x stream triggers Case A (cross-stream impact). Preemptive remediation tasks are created for the 2.1.x stream using the upstream backport variant (fix not yet available on release/0.3.z).

---

## Remediation Task Descriptions

### Task 1: Dependency Bump -- quinn-proto (2.2.x stream)

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
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
```

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.4.z (2.2.x stream)

```
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Task 3 (Preemptive): Upstream Backport -- quinn-proto (2.1.x stream)

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
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
```

Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
Link type: Related (to TC-8001, since this is a preemptive task for a different stream)

### Task 4 (Preemptive): Downstream Propagation -- update backend ref in rhtpa-release.0.3.z (2.1.x stream)

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
Link type: Related (to TC-8001, since this is a preemptive task for a different stream)

---

## Jira Linkage Summary

### 2.2.x Stream (standard remediation)

| From | To | Link Type |
|------|----|-----------|
| TC-8001 | Dependency bump task (2.2.x) | Depend |
| TC-8001 | Downstream propagation task (2.2.x) | Depend |
| Dependency bump task | Downstream propagation task (2.2.x) | Blocks |

### 2.1.x Stream (preemptive remediation)

| From | To | Link Type |
|------|----|-----------|
| TC-8001 | Upstream backport task (2.1.x) | Related |
| TC-8001 | Downstream propagation task (2.1.x) | Related |
| Upstream backport task | Downstream propagation task (2.1.x) | Blocks |

## Task Labels

| Task | Labels |
|------|--------|
| Dependency bump (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 |
| Downstream propagation (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 |
| Upstream backport (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| Downstream propagation (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

## Cross-Stream Impact Comment

The following cross-stream impact comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> Stream 2.1.x has no companion CVE Jira -- preemptive remediation tasks have been created.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: upstream backport task + downstream propagation task (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
