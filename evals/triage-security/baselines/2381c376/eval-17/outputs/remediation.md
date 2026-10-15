# Step 8 -- Remediation

## Triage Decision

- **Case B** applies for stream 2.2.x (the issue's scoped stream): affected versions exist (2.2.0, 2.2.1, 2.2.2).
- **Case A** applies for cross-stream impact: stream 2.1.x is also affected (2.1.0, 2.1.1) but is outside this issue's scope.

### Ecosystem Classification

- Ecosystem: **Cargo** (source dependency)
- Tasks per stream: **2** (dependency bump + downstream propagation)
- Upstream fix available: **Yes** (Step 2.5 confirms release/0.4.z ships quinn-proto 0.11.14)

Since the upstream branch already ships the fixed version, the **dependency bump** variant is used instead of the upstream backport variant for stream 2.2.x.

---

## Stream 2.2.x Remediation Tasks (Case B -- Standard)

### Task 1: Dependency Bump (upstream)

**Proposed Jira action:** `jira.create_issue()`

- **Issue Type**: Task
- **Summary**: `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Link to TC-8001**: Depend

#### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

### Task 2: Downstream Propagation (Konflux release repo)

**Proposed Jira action:** `jira.create_issue()`

- **Issue Type**: Task
- **Summary**: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Blocked by**: Task 1 (dependency bump)
- **Link to TC-8001**: Depend

#### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task updates quinn-proto to 0.11.14
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

- Depends on: [dependency-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Stream 2.1.x Preemptive Remediation Tasks (Case A -- Cross-Stream)

Since the issue is scoped to 2.2.x but stream 2.1.x is also affected, preemptive remediation tasks are created for 2.1.x (assuming no sibling CVE Jira exists for that stream).

### Task 3: Dependency Bump -- Preemptive (upstream, stream 2.1.x)

**Proposed Jira action:** `jira.create_issue()`

- **Issue Type**: Task
- **Summary**: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link to TC-8001**: Related (not Depend, because TC-8001 belongs to a different stream)

#### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the
fixed version.

Affected versions: RHTPA 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE, cross-stream)
```

### Task 4: Downstream Propagation -- Preemptive (Konflux release repo, stream 2.1.x)

**Proposed Jira action:** `jira.create_issue()`

- **Issue Type**: Task
- **Summary**: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Blocked by**: Task 3 (preemptive dependency bump)
- **Link to TC-8001**: Related

#### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the preemptive dependency bump task.

The dependency bump task updates quinn-proto to 0.11.14
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

- Depends on: [preemptive-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8001 (originating CVE, cross-stream)
```

---

## Proposed Jira Link Topology

All links below are proposed actions, not executed.

### Standard remediation links (stream 2.2.x)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8001 | [bump-task] | CVE depends on remediation |
| Depend | TC-8001 | [downstream-task] | CVE depends on remediation |
| Blocks | [bump-task] | [downstream-task] | Downstream blocked by upstream |

### Preemptive remediation links (stream 2.1.x)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8001 | [preemptive-bump-task] | Cross-stream (not Depend) |
| Related | TC-8001 | [preemptive-downstream-task] | Cross-stream (not Depend) |
| Blocks | [preemptive-bump-task] | [preemptive-downstream-task] | Downstream blocked by upstream |

---

## Proposed Cross-Stream Impact Comment (on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [preemptive-bump-task-key] (security-preemptive, upstream bump)
- 2.1.x: [preemptive-downstream-task-key] (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Proposed Affects Versions Correction (on TC-8001)

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Rationale: RHTPA 2.0.0 does not exist as a supported version. Lock file
analysis shows quinn-proto < 0.11.14 affects versions 2.2.0 (0.11.9),
2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3+ ship
quinn-proto 0.11.14 and are not affected. Scoped to stream 2.2.x per
issue suffix [rhtpa-2.2].
```

---

## Proposed Post-Triage Actions (on TC-8001)

1. **Add label**: `ai-cve-triaged`
2. **Transition**: New -> In Progress
3. **Post summary comment** documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (4 total: 2 standard for 2.2.x, 2 preemptive for 2.1.x)
   - Cross-stream impact on 2.1.x

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency -> dependency bump + downstream propagation) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: stream 2.1.x (outside issue scope) has preemptive tasks created
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x), "Related" for preemptive tasks linked to TC-8001 (2.1.x), "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: each task includes upstream coordination guidance (deployment context: upstream)
- [x] **Release Jira linking**: not yet resolved (Step 7.5 would determine release Epic/Task)
- [x] **Dedup consistency**: no dedup detected (Steps 4, 7.5.3 would check)
