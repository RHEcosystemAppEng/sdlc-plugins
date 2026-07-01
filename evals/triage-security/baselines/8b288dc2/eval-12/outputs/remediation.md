# Step 8 -- Remediation: CVE-2026-48901 (h2 < 0.4.8)

## Triage Outcome

- **Stream 2.2.x (scoped)**: Version 2.2.0 is affected. Versions 2.2.1+ are not affected (h2 >= 0.4.8). This is **Case A** -- create remediation tasks for the affected version.
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected. This is **Case B** -- post cross-stream impact comment and create preemptive remediation tasks (assuming no sibling CVE Jira exists for 2.1.x).

Ecosystem: **Cargo** (source dependency) -- requires 2 tasks per stream: upstream backport + downstream propagation.

---

## Case A -- Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

**Description**:

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: 2.2.0 (build v0.4.5, h2 0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

**Description**:

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

### Jira Linkage (2.2.x)

1. Link upstream task to TC-8030 with type "Depend"
2. Link downstream subtask as blocked by upstream task with type "Blocks"
3. Transition TC-8030 to In Progress

---

## Case B -- Cross-Stream Impact: Stream 2.1.x

### Cross-Stream Impact Comment

Post to TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> All versions in 2.1.x (2.1.0, 2.1.1) ship h2 0.4.5 which is within the affected range.
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Tasks for Stream 2.1.x

Since no sibling CVE Jira exists for stream 2.1.x, create preemptive remediation tasks with `security-preemptive` label and "Related" link type.

#### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: 2.1.0 (build v0.3.8, h2 0.4.5), 2.1.1 (build v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

#### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

### Preemptive Task Linkage (2.1.x)

1. Link both preemptive tasks to TC-8030 with type "Related" (not "Depend" -- different stream)
2. Link downstream subtask as blocked by upstream task with type "Blocks"

### Preemptive Tasks Comment

Post to TC-8030:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: upstream-task-key (security-preemptive), downstream-task-key (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
