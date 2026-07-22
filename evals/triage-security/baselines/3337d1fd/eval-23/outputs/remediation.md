# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case A** applies: supported versions within the issue's stream scope (2.2.x) are affected.
Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14.

**Case B** also applies: cross-stream impact detected. The 2.1.x stream (versions 2.1.0 and
2.1.1) is also affected. Since TC-8001 is scoped to `[rhtpa-2.2]`, the 2.1.x impact is outside
this issue's scope and requires cross-stream handling.

The ecosystem is **Cargo** (source dependency), so **two tasks** are created per affected stream:
an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency of the backend workspace)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround
  is viable (see upstream changelog)

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

## Task 2: Downstream Propagation Subtask (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case B: Cross-Stream Impact

### Cross-stream impact comment (posted to TC-8001)

Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 (quinn-proto 0.11.9) and 2.1.1
(quinn-proto 0.11.9) are affected. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x Stream

Since no existing CVE Jira was found for the 2.1.x stream for CVE-2026-31812,
proactive remediation tasks are created with the `security-preemptive` label.

#### Preemptive Task 3: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link type**: Related (to TC-8001, not Depend, because TC-8001 belongs to a different stream)

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency of the backend workspace)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround
  is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue, Related link)

#### Preemptive Task 4: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link type**: Related (to TC-8001)

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream preemptive backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

- Depends on: upstream preemptive backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue, Related link)

---

## Jira Linkage Summary

### Standard remediation (2.2.x stream -- Case A)

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Depend | TC-8001 | Upstream backport task (2.2.x) | Remediation tracking |
| Blocks | Upstream backport task (2.2.x) | Downstream propagation task (2.2.x) | Downstream blocked by upstream |
| Depend | TC-8001 | Downstream propagation task (2.2.x) | Remediation tracking |

### Preemptive remediation (2.1.x stream -- Case B)

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Related | TC-8001 | Preemptive upstream backport task (2.1.x) | Cross-stream preemptive |
| Blocks | Preemptive upstream task (2.1.x) | Preemptive downstream task (2.1.x) | Downstream blocked by upstream |
| Related | TC-8001 | Preemptive downstream task (2.1.x) | Cross-stream preemptive |

### Post-triage actions

- Add `ai-cve-triaged` label to TC-8001
- Transition TC-8001 to In Progress
- Post summary comment to TC-8001 with version impact table, Affects Versions correction, triage outcome, and links to all created remediation tasks
