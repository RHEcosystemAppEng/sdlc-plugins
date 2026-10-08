# Step 8 -- Remediation: CVE-2026-55123

## Triage Decision

- Issue TC-8020 is **scoped** to stream rhtpa-2.2
- In-scope stream rhtpa-2.2: versions RHTPA 2.2.0 and RHTPA 2.2.1 are **affected** (tokio 1.41.1 < 1.42.0)
- Out-of-scope stream rhtpa-2.1: versions RHTPA 2.1.0 and RHTPA 2.1.1 are **affected** (tokio 1.40.0 < 1.42.0)
- Sibling CVE Jira for rhtpa-2.1: **none found** (JQL search for label CVE-2026-55123 in stream rhtpa-2.1 returned no results)

## Applicable Cases

1. **Case A** (Cross-stream impact): Stream rhtpa-2.1 is affected and has no CVE Jira -- create preemptive remediation tasks
2. **Case B** (Affected): Stream rhtpa-2.2 is the in-scope stream -- create standard remediation tasks

---

## Case B: Standard Remediation Tasks (stream rhtpa-2.2)

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

### Task 1: Upstream backport/dependency bump (rhtpa-2.2)

```
Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-55123
Link to TC-8020: Depend
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (tokio is a direct dependency of the backend workspace)
- Run `cargo update -p tokio` to pull in tokio >= 1.42.0
- Verify Cargo.lock reflects tokio >= 1.42.0 after the update
- If the update pulls a version still in the affected range, pin explicitly:
  `cargo add tokio@1.42.0`

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

---

### Task 2: Downstream propagation (rhtpa-2.2)

```
Summary: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-55123
Link to TC-8020: Depend
Blocked by: Task 1 (upstream backport)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
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

---

## Case A: Preemptive Remediation Tasks (stream rhtpa-2.1)

No sibling CVE Jira exists for stream rhtpa-2.1. Creating preemptive remediation tasks.

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

### Preemptive Task 1: Upstream backport/dependency bump (rhtpa-2.1)

```
Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
Link to TC-8020: Related (not Depend -- originating CVE is from a different stream)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (tokio is a direct dependency of the backend workspace)
- Run `cargo update -p tokio` to pull in tokio >= 1.42.0
- Verify Cargo.lock reflects tokio >= 1.42.0 after the update
- If the update pulls a version still in the affected range, pin explicitly:
  `cargo add tokio@1.42.0`

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

- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

---

### Preemptive Task 2: Downstream propagation (rhtpa-2.1)

```
Summary: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
Link to TC-8020: Related (not Depend -- originating CVE is from a different stream)
Blocked by: Preemptive Task 1 (upstream backport)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) = 2 tasks per stream (upstream + downstream). rhtpa-2.2: 2 tasks, rhtpa-2.1: 2 tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: Stream rhtpa-2.1 has no sibling CVE Jira -- preemptive tasks created.
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020; "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020; "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream coordination guidance (deployment context: upstream).
- [x] **Dedup consistency**: No dedup detected -- all tasks are new.

## Jira Linkage Summary

### Standard remediation (rhtpa-2.2)

| Link | From | To | Type |
|------|------|----|------|
| CVE to upstream task | TC-8020 | upstream-task-rhtpa-2.2 | Depend |
| CVE to downstream task | TC-8020 | downstream-task-rhtpa-2.2 | Depend |
| Upstream blocks downstream | upstream-task-rhtpa-2.2 | downstream-task-rhtpa-2.2 | Blocks |

### Preemptive remediation (rhtpa-2.1)

| Link | From | To | Type |
|------|------|----|------|
| CVE to preemptive upstream task | TC-8020 | preemptive-upstream-task-rhtpa-2.1 | Related |
| CVE to preemptive downstream task | TC-8020 | preemptive-downstream-task-rhtpa-2.1 | Related |
| Preemptive upstream blocks downstream | preemptive-upstream-task-rhtpa-2.1 | preemptive-downstream-task-rhtpa-2.1 | Blocks |
