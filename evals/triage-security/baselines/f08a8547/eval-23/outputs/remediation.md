# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

The version impact analysis shows that supported versions in both the 2.2.x and 2.1.x streams are affected by CVE-2026-31812 (quinn-proto < 0.11.14). The issue is scoped to stream 2.2.x.

- **Case B** applies for stream 2.2.x (scoped): versions 2.2.0, 2.2.1, 2.2.2 are affected. Create remediation tasks.
- **Case A** applies for stream 2.1.x (cross-stream): versions 2.1.0, 2.1.1 are affected. Create preemptive remediation tasks (or skip if a sibling CVE Jira already exists for 2.1.x).

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case B: Remediation Tasks for Stream 2.2.x (Scoped)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend on TC-8001 (parent Vulnerability issue)

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

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14 and are NOT affected. The upstream branch release/0.4.z likely already contains the fix at HEAD.

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct dependency of the backend workspace)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The upstream fix PR (quinn-rs/quinn#2048) provides the patch -- verify compatibility

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

**Links**:
- Depend on TC-8001 (parent Vulnerability issue)
- Blocked by upstream backport task (Task 1 above)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

## Case A: Cross-Stream Preemptive Remediation for Stream 2.1.x

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but this issue (TC-8001) is scoped to 2.2.x. If no sibling CVE Jira exists for 2.1.x, create preemptive remediation tasks.

### Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
Versions 2.1.0 (quinn-proto 0.11.9) and 2.1.1 (quinn-proto 0.11.9) are affected.
These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
```

### Preemptive Task 3: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE Jira, different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

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

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct dependency of the backend workspace)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The upstream fix PR (quinn-rs/quinn#2048) provides the patch -- verify compatibility

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, cross-stream)

---

### Preemptive Task 4: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Links**:
- Related to TC-8001 (originating CVE Jira, different stream)
- Blocked by preemptive upstream backport task (Task 3 above)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, cross-stream)

---

## Preemptive Tasks Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
- 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Summary of All Remediation Tasks

| # | Stream | Type | Summary | Labels | Link to TC-8001 |
|---|--------|------|---------|--------|-----------------|
| 1 | 2.2.x | Upstream backport | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

### Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency ecosystem) -- 2 for 2.2.x + 2 preemptive for 2.1.x = 4 total
- [x] **Cross-stream coverage**: stream 2.1.x (outside issue scope) has preemptive tasks created
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001, "Related" for 2.1.x preemptive tasks linked to TC-8001, "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: each task includes "customer-shipped" coordination guidance (coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure)
