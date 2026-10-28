# Step 8 -- Remediation: TC-8020

## Triage Outcome

- **Case A** applies: Issue is scoped to rhtpa-2.2, but cross-stream analysis shows rhtpa-2.1 is also affected. Since no sibling CVE Jira exists for rhtpa-2.1, preemptive remediation tasks are required (see outputs/cross-stream.md).
- **Case B** applies: Standard remediation tasks for the scoped stream (rhtpa-2.2).
- Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

## Case B: Remediation Tasks for Current Stream (rhtpa-2.2)

### Task 1: Upstream Backport / Dependency Bump (rhtpa-2.2)

```
Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
Issue Type: Task
Labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
```

#### Description

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
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add tokio@1.42.0`
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

#### Jira Linkage

- Link to TC-8020 with type "Depend" (inward: TC-8020, outward: this task)

---

### Task 2: Downstream Propagation (rhtpa-2.2)

```
Summary: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
Issue Type: Task
Labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
```

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream task.

The upstream task bumps tokio to 1.42.0
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

- Depends on: upstream backport/dependency bump task (upstream task must merge first)
- Depends on: TC-8020 (parent tracking issue)

#### Jira Linkage

- Link to TC-8020 with type "Depend" (inward: TC-8020, outward: this task)
- Link to upstream task with type "Blocks" (inward: upstream task, outward: this task -- this task is blocked by the upstream task)

## Pre-creation Checklist

- [x] **Task count per stream**: 2 tasks for Cargo source dependency ecosystem (upstream + downstream) -- matches classification table
- [x] **Cross-stream coverage**: rhtpa-2.1 has no sibling CVE Jira -- preemptive tasks created (see cross-stream.md)
- [x] **Link types**: "Depend" for tasks linked to TC-8020, "Blocks" from upstream to downstream
- [x] **Preemptive labels**: preemptive tasks for rhtpa-2.1 carry `security-preemptive` label (see cross-stream.md)
- [x] **Coordination guidance**: upstream deployment context guidance included
