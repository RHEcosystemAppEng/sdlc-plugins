# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A** applies: issue is scoped to 2.2.x, but 2.1.x is also affected with no sibling CVE Jira.
- **Case B** applies: affected versions exist within the issue scope (2.2.x).
- Ecosystem: Cargo (source dependency) -- 2 tasks per stream.
- 2.2.x upstream fix status: YES (release/0.4.z already ships 0.11.14) -- use dependency bump variant.
- 2.1.x upstream fix status: NO (release/0.3.z still at 0.11.9) -- use upstream backport variant.
- Preemptive tasks for 2.1.x carry `security-preemptive` label and use "Related" link type.

---

## Task 1: Dependency bump -- 2.2.x stream (within scope)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Link**: Depend (inward: TC-8001, outward: this task)

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream propagation -- 2.2.x stream (within scope)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Links**:
- Depend (inward: TC-8001, outward: this task)
- Blocks (inward: Task 1, outward: this task) -- blocked by the dependency bump task

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
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

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Task 3: Upstream backport -- 2.1.x stream (preemptive, Case A)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related (inward: TC-8001, outward: this task) -- preemptive uses "Related" not "Depend"

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto denial of service vulnerability.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 4: Downstream propagation -- 2.1.x stream (preemptive, Case A)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Links**:
- Related (inward: TC-8001, outward: this task) -- preemptive uses "Related" not "Depend"
- Blocks (inward: Task 3, outward: this task) -- blocked by the upstream backport task

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
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

- Depends on: Task 3 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Post-Triage Summary

### Label

Add `ai-cve-triaged` label to TC-8001.

### Affects Versions Correction

Remove: RHTPA 2.0.0
Add: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Cross-Stream Impact Comment

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. No sibling CVE Jira exists for stream 2.1.x.
Preemptive remediation tasks created:
- 2.1.x: Task 3 (upstream backport, security-preemptive), Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates a stream-specific CVE Jira for [rhtpa-2.1], Step 4.4
reconciliation will link them and remove the label.

### Remediation Task Summary

Within-scope remediation (2.2.x):
- Task 1: Dependency bump -- update quinn-proto to 0.11.14 on release/0.4.z (upstream fix already available)
- Task 2: Downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by Task 1)

Preemptive remediation (2.1.x -- no CVE Jira for this stream):
- Task 3: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (fix not yet available upstream)
- Task 4: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by Task 3)

### Link Topology

- TC-8001 --[Depend]--> Task 1, Task 2
- TC-8001 --[Related]--> Task 3, Task 4 (preemptive)
- Task 1 --[Blocks]--> Task 2 (upstream blocks downstream, 2.2.x)
- Task 3 --[Blocks]--> Task 4 (upstream blocks downstream, 2.1.x)
