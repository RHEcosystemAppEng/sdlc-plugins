# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

The issue is scoped to stream **2.2.x**. Within that stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14).

Cross-stream analysis reveals that stream **2.1.x** (versions 2.1.0, 2.1.1) is also affected. Since no companion CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created (Case B).

Ecosystem: **Cargo** (source dependency) -- two tasks per stream: upstream backport + downstream propagation.

---

## Case A: Remediation Tasks for Stream 2.2.x (scoped)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend on TC-8001

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency of backend workspace)

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

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend on TC-8001, Blocked by upstream backport task (Task 1)

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

## Case B: Preemptive Remediation Tasks for Stream 2.1.x (cross-stream)

The 2.1.x stream is also affected (quinn-proto 0.11.9 in both 2.1.0 and 2.1.1), but no companion CVE Jira exists for this stream. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link to the originating CVE Jira TC-8001.

### Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.
```

### Preemptive Task 3: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001

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

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency of backend workspace)

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

- Depends on: TC-8001 (originating tracking issue, Related link)

---

### Preemptive Task 4: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001, Blocked by preemptive upstream backport task (Task 3)

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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, Related link)

---

## Preemptive Tasks Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task + downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Summary of All Remediation Tasks

| # | Type | Stream | Summary | Labels | Link to TC-8001 |
|---|------|--------|---------|--------|-----------------|
| 1 | Upstream backport | 2.2.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation | 2.2.x | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (preemptive) | 2.1.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (preemptive) | 2.1.x | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

All remediation task descriptions include the **Coordination Guidance** subsection under Implementation Notes with the **customer-shipped** deployment context guidance: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
