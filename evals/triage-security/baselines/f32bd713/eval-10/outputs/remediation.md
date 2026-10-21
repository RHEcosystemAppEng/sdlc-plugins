# Step 8 -- Remediation: TC-8020

## Triage Decision

- **Issue stream scope**: 2.2.x (rhtpa-2.2)
- **Affected versions in scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag)
- **Cross-stream affected**: 2.1.x (rhtpa-2.1) -- no sibling CVE Jira exists
- **Ecosystem**: Cargo (source dependency)
- **Tasks per stream**: 2 (upstream backport/dependency bump + downstream propagation)

## Case B: Standard Remediation Tasks (Stream 2.2.x -- Issue Scope)

These are standard remediation tasks for the issue's own stream. Linked to TC-8020 with "Depend" link type.

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-55123
**Link**: Depend (inward: TC-8020, outward: this task)

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio versions before 1.42.0) is affected by a
use-after-free when a spawned task is aborted while holding a borrowed reference.

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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-55123
**Link**: Depend (inward: TC-8020, outward: this task)
**Blocked by**: Task 1 (Blocks link: inward: Task 1, outward: this task)

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

## Case A: Preemptive Remediation Tasks (Stream 2.1.x -- Cross-Stream)

These are preemptive remediation tasks for stream 2.1.x, which is affected but has no CVE Jira of its own. Linked to TC-8020 with "Related" link type (not "Depend"). Labels include `security-preemptive`.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
**Link**: Related (inward: TC-8020, outward: this task)

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio versions before 1.42.0) is affected by a
use-after-free when a spawned task is aborted while holding a borrowed reference.

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest
  compatible version (>= 1.42.0)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating CVE Jira, cross-stream)
```

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
**Link**: Related (inward: TC-8020, outward: this task)
**Blocked by**: Task 3 (Blocks link: inward: Task 3, outward: this task)

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE Jira, cross-stream)
```

## Jira Linkage Summary

### Standard tasks (2.2.x stream)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8020 | Task 1 (upstream) | CVE to remediation |
| Depend | TC-8020 | Task 2 (downstream) | CVE to remediation |
| Blocks | Task 1 (upstream) | Task 2 (downstream) | Upstream blocks downstream |

### Preemptive tasks (2.1.x stream)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8020 | Task 3 (upstream, preemptive) | Cross-stream originating CVE |
| Related | TC-8020 | Task 4 (downstream, preemptive) | Cross-stream originating CVE |
| Blocks | Task 3 (upstream) | Task 4 (downstream) | Upstream blocks downstream |

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: stream 2.1.x has no sibling CVE Jira -- preemptive tasks created
- [x] **Link types**: "Depend" for standard tasks linked to TC-8020; "Related" for preemptive tasks linked to TC-8020; "Blocks" for upstream to downstream within a stream
- [x] **Preemptive labels**: Tasks 3 and 4 carry the `security-preemptive` label
- [x] **Coordination guidance**: Source Repositories table has no Deployment Context column -- coordination guidance omitted
- [x] **Dedup consistency**: no dedup detected -- all tasks are new
