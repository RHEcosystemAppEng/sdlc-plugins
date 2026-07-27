# Remediation — CVE-2026-55123 (tokio < 1.42.0)

## Triage Outcome

- **Case A** applies: the issue is scoped to stream rhtpa-2.2, but cross-stream analysis reveals rhtpa-2.1 is also affected and has no sibling CVE Jira.
- **Case B** applies: affected versions exist within the issue's scoped stream (rhtpa-2.2), so remediation tasks are created.

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case B: Remediation Tasks for Current Stream (rhtpa-2.2)

### Task 1: Upstream Backport (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link**: Depend -> TC-8020

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be confirmed via lock file inspection)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

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

**Link**: Depend -> TC-8020, Blocked by upstream backport task

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: carried forward from upstream task
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

---

## Case A: Preemptive Remediation Tasks for Stream rhtpa-2.1

Since no sibling CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks
are created with the `security-preemptive` label and "Related" link type to TC-8020.

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link**: Related -> TC-8020

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

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via lock file inspection)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (related -- originating CVE from stream rhtpa-2.2)

---

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link**: Related -> TC-8020, Blocked by preemptive upstream backport task

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

The upstream backport bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (related -- originating CVE from stream rhtpa-2.2)
