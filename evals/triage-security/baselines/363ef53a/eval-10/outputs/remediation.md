# Remediation — TC-8020

## Triage Outcome

- **Case A** (cross-stream impact): stream rhtpa-2.1 is also affected, no CVE Jira exists for that stream -- create preemptive remediation tasks
- **Case B** (affected): stream rhtpa-2.2 is affected -- create standard remediation tasks

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream + downstream)

---

## Case B: Standard Remediation Tasks for Current Stream (rhtpa-2.2)

### Task 1: Upstream Backport (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-55123
**Link**: Depend -> TC-8020

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest
  compatible version. If the update pulls a version that still falls within
  the affected range, pin explicitly: `cargo add tokio@1.42.0`
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

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-55123
**Link**: Depend -> TC-8020, Blocks -> upstream task (Task 1)

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

- Depends on: upstream backport task (must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

---

## Case A: Preemptive Remediation Tasks for Stream rhtpa-2.1

No CVE Jira exists for stream rhtpa-2.1. Preemptive tasks are created with
the `security-preemptive` label and linked to TC-8020 via "Related" (not "Depend").

### Task 3: Preemptive Upstream Backport (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
**Link**: Related -> TC-8020

#### Description

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest
  compatible version. If the update pulls a version that still falls within
  the affected range, pin explicitly: `cargo add tokio@1.42.0`
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

- Depends on: TC-8020 (originating CVE from stream rhtpa-2.2)
```

### Task 4: Preemptive Downstream Propagation (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
**Link**: Related -> TC-8020, Blocks -> preemptive upstream task (Task 3)

#### Description

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the preemptive upstream backport task.

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

- Depends on: preemptive upstream backport task (must merge first)
- Depends on: TC-8020 (originating CVE from stream rhtpa-2.2)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream (upstream + downstream). rhtpa-2.2: 2 tasks. rhtpa-2.1: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 (no CVE Jira) gets preemptive tasks.
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020; "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020; "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: upstream deployment context guidance included in all tasks.
- [x] **Release Jira linking**: would apply post-creation (Step 7.5).
- [x] **Dedup consistency**: no dedup detected.
