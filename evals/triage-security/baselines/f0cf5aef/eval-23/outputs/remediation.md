# Step 8 -- Remediation (TC-8001: CVE-2026-31812)

## Triage Outcome

- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
- **Affected versions in scope**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in scope**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)
- **Cross-stream impact**: 2.1.x stream also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per affected stream
- **Deployment context**: customer-shipped

## Case A: Cross-Stream Impact Comment

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
Stream 2.1.x is tracked by companion issues (see Related links) or may require
separate PSIRT triage.
```

Preemptive remediation tasks are created for the 2.1.x stream (no stream-specific CVE Jira exists).

---

## Case B: Remediation Tasks for 2.2.x Stream (In-Scope)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend -> TC-8001

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is already present at v0.4.11+ on this branch (quinn-proto 0.11.14). The upstream backport may already be merged. Verify the current state of release/0.4.z before proceeding.

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Lock file: Cargo.lock
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend -> TC-8001, Blocked by Task 1 (upstream backport)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case A: Preemptive Remediation Tasks for 2.1.x Stream (Cross-Stream)

These tasks are created proactively because the 2.1.x stream is affected but has no stream-specific CVE Jira.

### Task 3 (Preemptive): Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related -> TC-8001 (not Depend, because this is a preemptive task for a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is NOT yet present on release/0.3.z (latest tag v0.3.12 ships quinn-proto 0.11.9). An upstream backport PR is required.

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Lock file: Cargo.lock
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE tracking issue)

---

### Task 4 (Preemptive): Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related -> TC-8001, Blocked by Task 3 (upstream backport for 2.1.x)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream. 2.2.x: 2 tasks (upstream + downstream). 2.1.x: 2 preemptive tasks (upstream + downstream). Total: 4 tasks.
- [x] **Cross-stream coverage**: Issue is scoped to 2.2.x. Stream 2.1.x (outside scope) is affected and has no sibling CVE Jira -- preemptive tasks created with `security-preemptive` label.
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001. "Related" for 2.1.x preemptive tasks linked to TC-8001. "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: All task Implementation Notes include `### Coordination Guidance` subsection with customer-shipped guidance: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."

## Post-Triage Summary

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: Task 3 (upstream backport, security-preemptive), Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
