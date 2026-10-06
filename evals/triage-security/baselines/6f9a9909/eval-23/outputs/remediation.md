# Step 8 -- Remediation: TC-8001

## Triage Outcome

- **Case A** applies: cross-stream impact detected. The issue is scoped to 2.2.x, but 2.1.x is also affected.
- **Case B** applies: affected versions exist in the scoped stream (2.2.0, 2.2.1, 2.2.2).
- Ecosystem: Cargo (source dependency) -- **2 tasks per stream** (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact Notice

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9 which is within the affected range.

These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with the `security-preemptive` label and linked via "Related" to TC-8001.

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock / Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- Note: upstream branch already ships the fix at tags v0.4.11+ (quinn-proto 0.11.14). The fix needs to be backported or the source reference updated to a commit that includes the bump.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Blocked by**: Upstream backport task (Task 1)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream -- Case A)

If no sibling CVE Jira exists for stream 2.1.x, the following preemptive tasks would be created with the `security-preemptive` label and "Related" link to TC-8001.

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock / Cargo.toml
- Note: the latest tag on this branch (v0.3.12) still ships quinn-proto 0.11.9. The upstream fix needs to be backported to the release/0.3.z branch.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE -- Related link)

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

**Blocked by**: Preemptive upstream backport task (Preemptive Task 1)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE -- Related link)

---

## Jira Linkage Summary

### In-Scope (2.2.x) Tasks

| Task | Type | Link to TC-8001 | Blocked By |
|------|------|-----------------|------------|
| Upstream backport (2.2.x) | Depend | TC-8001 -> Task | -- |
| Downstream propagation (2.2.x) | Depend | TC-8001 -> Task | Upstream backport (Blocks) |

### Preemptive (2.1.x) Tasks

| Task | Type | Link to TC-8001 | Blocked By |
|------|------|-----------------|------------|
| Upstream backport (2.1.x) | Related | TC-8001 <-> Task | -- |
| Downstream propagation (2.1.x) | Related | TC-8001 <-> Task | Upstream backport (Blocks) |

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo is a source dependency ecosystem) -- matches classification table
- [x] **Cross-stream coverage**: 2.1.x (affected, outside scope) has preemptive tasks created (or would need a sibling CVE Jira check first)
- [x] **Link types**: "Depend" for in-scope 2.2.x tasks linked to TC-8001; "Related" for preemptive 2.1.x tasks linked to TC-8001; "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: Each task's Implementation Notes includes guidance for `customer-shipped` deployment context: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
