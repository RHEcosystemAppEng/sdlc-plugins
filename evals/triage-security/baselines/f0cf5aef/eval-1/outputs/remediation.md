# Step 8 -- Remediation

## Triage Outcome: Case B (Affected) + Case A (Cross-Stream Impact)

The issue TC-8001 is scoped to stream **2.2.x**. Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the scoped stream.

Additionally, stream **2.1.x** (versions 2.1.0, 2.1.1) is also affected (Case A -- cross-stream impact).

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case B: Remediation Tasks for Stream 2.2.x (Issue's Scoped Stream)

### Task 1: Upstream Backport (Stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Note: upstream branch HEAD (v0.4.11+) already ships quinn-proto 0.11.14,
  so the fix may already be present on the branch tip. Verify and propagate
  downstream.

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage**: Link with type "Depend" from TC-8001 to this task.

---

### Task 2: Downstream Propagation (Stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (or transitive) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage**:
- Link with type "Depend" from TC-8001 to this task
- Link with type "Blocks" from upstream task (Task 1) to this task (downstream blocked by upstream)

---

## Case A: Cross-Stream Impact -- Preemptive Remediation for Stream 2.1.x

Stream 2.1.x (versions 2.1.0 and 2.1.1) is also affected but is outside the issue's scope (TC-8001 is scoped to 2.2.x). If no sibling CVE Jira exists for stream 2.1.x, create preemptive remediation tasks.

### Proposed Cross-Stream Impact Comment (on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Task 3 (Preemptive): Upstream Backport (Stream 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
- Note: upstream branch HEAD for release/0.3.z still ships quinn-proto 0.11.9.
  An upstream backport PR is needed to bump quinn-proto to >= 0.11.14 on this branch.

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue -- cross-stream)
```

**Jira linkage**: Link with type "Related" (not "Depend") from TC-8001 to this task (preemptive task linked to originating CVE).

---

### Task 4 (Preemptive): Downstream Propagation (Stream 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

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
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (or transitive) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue -- cross-stream)
```

**Jira linkage**:
- Link with type "Related" (not "Depend") from TC-8001 to this task (preemptive)
- Link with type "Blocks" from preemptive upstream task (Task 3) to this task

---

## Proposed Preemptive Tasks Comment (on TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <task-3-key> (upstream backport, security-preemptive)
- 2.1.x: <task-4-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream. Stream 2.2.x: 2 tasks. Stream 2.1.x: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: stream 2.1.x (outside issue scope) covered by preemptive tasks (assuming no sibling CVE Jira exists for 2.1.x).
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (Tasks 1, 2 -> TC-8001). "Related" for preemptive tasks linked to originating CVE (Tasks 3, 4 -> TC-8001). "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: Tasks 3 and 4 carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task's Implementation Notes includes upstream deployment context guidance.
