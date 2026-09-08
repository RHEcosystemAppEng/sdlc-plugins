# Step 8 -- Remediation: CVE-2026-55123

## Triage Outcome

- **Case A applies**: Issue is scoped to stream rhtpa-2.2, but stream rhtpa-2.1 is also affected
- **Case B applies**: Affected versions exist -- create remediation tasks
- Cross-stream impact detected: stream rhtpa-2.1 has no sibling CVE Jira -- preemptive tasks required

## Case A -- Current Stream (rhtpa-2.2): Standard Remediation Tasks

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

### Task 1: Upstream Backport (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
**Link**: Depend -> TC-8020

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
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
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
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
**Link**: Depend -> TC-8020, Blocks <- upstream backport task

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

## Case B -- Cross-Stream Preemptive Tasks (rhtpa-2.1)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0 threshold) but has no sibling CVE Jira.
Preemptive remediation tasks are created with the `security-preemptive` label and linked
to the originating CVE Jira (TC-8020) with "Related" link type (not "Depend").

Ecosystem: Cargo (source dependency) -- 2 preemptive tasks.

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
**Link**: Related -> TC-8020

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

Remediate CVE-2026-55123: tokio use-after-free in task abort.
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
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
**Link**: Related -> TC-8020, Blocks <- preemptive upstream backport task

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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream (upstream backport + downstream propagation)
  - rhtpa-2.2: 2 standard tasks (Depend link to TC-8020)
  - rhtpa-2.1: 2 preemptive tasks (Related link to TC-8020)
- [x] **Cross-stream coverage**: stream rhtpa-2.1 (outside issue scope) has no sibling CVE Jira -> preemptive tasks created
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020; "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020; "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label
- [x] **Coordination guidance**: not included (Deployment Context column absent from Source Repositories table -- backward compatibility)
