# Remediation Tasks — CVE-2026-55123 (tokio)

## Case A: Standard Remediation for Current Stream rhtpa-2.2

The issue TC-8020 is scoped to stream rhtpa-2.2. Both RHTPA 2.2.0 and RHTPA 2.2.1
ship tokio 1.41.1, which is within the affected range (< 1.42.0). Ecosystem is Cargo
(source dependency), so two tasks are created for this stream.

### Task 1: Upstream Backport — rhtpa-2.2

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link to TC-8020**: **Depend** (standard remediation for the scoped stream)

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (tokio is a direct dependency)
- **Remediation action**: run `cargo update -p tokio` to pull in >= 1.42.0
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task 2: Downstream Propagation — rhtpa-2.2

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link to TC-8020**: **Depend** (standard remediation for the scoped stream)

**Link to Task 1**: **Blocks** (upstream task blocks downstream propagation)

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

---

## Case B: Preemptive Remediation for Stream rhtpa-2.1

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira**
of its own. Preemptive remediation tasks are created with the following differences
from standard Case A tasks:

- Labels include `security-preemptive` alongside standard labels
- Link type is **Related** (not Depend) to TC-8020 -- different stream
- Description includes a preemptive remediation prefix noting TC-8020 as originating CVE

### Task 3: Upstream Backport (Preemptive) — rhtpa-2.1

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link to TC-8020**: **Related** (preemptive task for a different stream)

#### Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (tokio is a direct dependency)
- **Remediation action**: run `cargo update -p tokio` to pull in >= 1.42.0
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

### Task 4: Downstream Propagation (Preemptive) — rhtpa-2.1

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link to TC-8020**: **Related** (preemptive task for a different stream)

**Link to Task 3**: **Blocks** (upstream task blocks downstream propagation)

#### Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for rhtpa-2.1 (upstream backport must merge first)
- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

---

## Link Topology Summary

### Standard remediation (rhtpa-2.2 -- Case A)

| From | To | Link Type | Reason |
|------|----|-----------|--------|
| TC-8020 (CVE) | Task 1 (upstream) | Depend | Standard remediation for scoped stream |
| TC-8020 (CVE) | Task 2 (downstream) | Depend | Standard remediation for scoped stream |
| Task 1 (upstream) | Task 2 (downstream) | Blocks | Upstream must merge before downstream propagation |

### Preemptive remediation (rhtpa-2.1 -- Case B)

| From | To | Link Type | Reason |
|------|----|-----------|--------|
| TC-8020 (CVE) | Task 3 (upstream, preemptive) | Related | Preemptive task, originating CVE is from different stream |
| TC-8020 (CVE) | Task 4 (downstream, preemptive) | Related | Preemptive task, originating CVE is from different stream |
| Task 3 (upstream, preemptive) | Task 4 (downstream, preemptive) | Blocks | Upstream must merge before downstream propagation |
