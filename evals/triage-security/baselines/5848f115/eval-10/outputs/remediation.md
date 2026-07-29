# Remediation -- CVE-2026-55123

## Triage Decision

- Issue TC-8020 is **scoped** to stream rhtpa-2.2
- Stream rhtpa-2.2 versions are **affected** (tokio 1.41.1 < 1.42.0)
- Stream rhtpa-2.1 is also affected but has **no CVE Jira**
- Ecosystem: Cargo (source dependency) -- **2 tasks per stream**
- Decision: **Case A** (cross-stream impact with preemptive remediation) + **Case B** (create remediation tasks)

---

## Case A -- Current Stream (rhtpa-2.2) Remediation Tasks

These are standard remediation tasks linked to TC-8020 with "Depend" link type.

### Task 1: Upstream Backport (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link**: Depend (inward: TC-8020, outward: this task)

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Run `cargo update -p tokio` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Links**:
- Depend (inward: TC-8020, outward: this task)
- Blocks (inward: upstream task, outward: this task)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

---

## Case B -- Preemptive Remediation Tasks for Stream rhtpa-2.1

These are **preemptive** remediation tasks for stream rhtpa-2.1, which has no
CVE Jira of its own. They are linked to TC-8020 with "Related" (not "Depend")
link type and carry the `security-preemptive` label.

### Task 3: Preemptive Upstream Backport (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link**: Related (inward: TC-8020, outward: this task)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Run `cargo update -p tokio` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, different stream)

---

### Task 4: Preemptive Downstream Propagation (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Links**:
- Related (inward: TC-8020, outward: this task)
- Blocks (inward: preemptive upstream task, outward: this task)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the preemptive upstream backport task.

The upstream backport task bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, different stream)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation). rhtpa-2.2: 2 tasks, rhtpa-2.1: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: Stream rhtpa-2.1 has no CVE Jira -- preemptive tasks created with `security-preemptive` label.
- [x] **Link types**: "Depend" for tasks linked to TC-8020 (own stream), "Related" for preemptive tasks linked to TC-8020 (other stream), "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: Tasks for rhtpa-2.1 carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream coordination guidance (deployment context: upstream).
