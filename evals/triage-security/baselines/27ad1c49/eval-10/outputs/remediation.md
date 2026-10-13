# Remediation Tasks — CVE-2026-55123 (tokio)

## Overview

- **Issue**: TC-8020 (scoped to rhtpa-2.2)
- **CVE**: CVE-2026-55123
- **Library**: tokio
- **Fix threshold**: >= 1.42.0
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream

This issue follows the Case A + Case B path:
- **Case B (current stream rhtpa-2.2)**: Standard remediation tasks for RHTPA 2.2.0, 2.2.1, 2.2.2
- **Case A (cross-stream rhtpa-2.1)**: Preemptive remediation tasks for RHTPA 2.1.0, 2.1.1 (no CVE Jira exists for this stream)

---

## Case B: Standard Remediation Tasks (rhtpa-2.2)

The upstream branch `release/0.4.z` already ships tokio 1.42.0 (confirmed by
RHTPA 2.2.3 and 2.2.4 shipping the fix). Therefore, the dependency bump variant
is used instead of the upstream backport variant.

### Task 1: Dependency Bump (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: update tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link**: Depend -- inward: TC-8020, outward: this task

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio < 1.42.0) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest
  compatible version (>= 1.42.0)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

### Task 2: Downstream Propagation (rhtpa-2.2)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Links**:
- Depend -- inward: TC-8020, outward: this task
- Blocks -- inward: Task 1 (dependency bump), outward: this task (downstream blocked by upstream)

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the dependency bump task.

The dependency bump task bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

---

## Case A: Preemptive Remediation Tasks (rhtpa-2.1)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira.
These preemptive tasks are created proactively from cross-stream impact
analysis. They carry the `security-preemptive` label and use the "Related"
link type (not "Depend") to the originating CVE Jira TC-8020.

The upstream branch `release/0.3.z` does NOT yet ship tokio 1.42.0, so
the upstream backport variant is used.

### Task 3: Upstream Backport -- Preemptive (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link**: Related -- inward: TC-8020, outward: this task (preemptive -- originating CVE is in a different stream)

#### Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- The upstream branch release/0.3.z currently ships tokio 1.40.0 --
  an upstream backport is required to bump the dependency

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating tracking issue, cross-stream)
```

### Task 4: Downstream Propagation -- Preemptive (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Links**:
- Related -- inward: TC-8020, outward: this task (preemptive)
- Blocks -- inward: Task 3 (upstream backport), outward: this task (downstream blocked by upstream)

#### Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8020 (originating tracking issue, cross-stream)
```

---

## Jira Linkage Summary

### Standard tasks (rhtpa-2.2)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8020 | Task 1 (dep bump) | CVE to remediation |
| Depend | TC-8020 | Task 2 (downstream) | CVE to remediation |
| Blocks | Task 1 (dep bump) | Task 2 (downstream) | Upstream blocks downstream |

### Preemptive tasks (rhtpa-2.1)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8020 | Task 3 (backport) | Cross-stream preemptive link |
| Related | TC-8020 | Task 4 (downstream) | Cross-stream preemptive link |
| Blocks | Task 3 (backport) | Task 4 (downstream) | Upstream blocks downstream |

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (upstream + downstream)
- [x] **Cross-stream coverage**: rhtpa-2.1 (affected, no CVE Jira) covered by preemptive tasks
- [x] **Link types**: "Depend" for standard tasks linked to TC-8020; "Related" for preemptive tasks linked to TC-8020; "Blocks" for upstream-to-downstream within each stream
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label
- [x] **Coordination guidance**: included (deployment context: upstream)
- [x] **Dedup consistency**: no dedup applicable (no existing remediation tasks)
