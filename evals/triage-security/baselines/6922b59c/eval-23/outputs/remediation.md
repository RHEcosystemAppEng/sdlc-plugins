# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Deployment context**: customer-shipped
- **Affected versions (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected (2.2.x)**: 2.2.3, 2.2.4 (already ship quinn-proto 0.11.14)
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 (both ship quinn-proto 0.11.9)

## Case A: Cross-Stream Impact

The issue is scoped to 2.2.x, but lock file analysis reveals that the 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created below.

### Cross-stream impact comment (for TC-8001)

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by preemptive remediation tasks (see Related links) or may require separate PSIRT triage.

---

## Remediation Tasks -- 2.2.x Stream

Since the upstream branch `release/0.4.z` already ships the fix (quinn-proto 0.11.14 as of v0.4.11), and versions 2.2.3+ already include the fix, the fix is already shipped for the 2.2.x stream. The Affects Versions are corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

### Task 1: Dependency Bump -- quinn-proto on release/0.4.z (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend (inward: TC-8001, outward: this task)

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

**Note**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14
as of tag v0.4.11. Versions 2.2.3 and 2.2.4 already include the fix. This task
may already be complete -- verify that the current branch HEAD includes
quinn-proto >= 0.11.14 in Cargo.lock.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

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

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.4.z (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Links**:
- Depend (inward: TC-8001, outward: this task)
- Blocks (inward: Task 1, outward: this task) -- blocked by upstream dependency bump

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream dependency bump task.

The upstream dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

**Note**: The latest released tag (v0.4.12, build 0.4.12) already ships
quinn-proto 0.11.14. If the current source pinning already references v0.4.11
or later, this propagation is already complete.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Tasks -- 2.1.x Stream (Preemptive)

The 2.1.x stream has no sibling CVE Jira for CVE-2026-31812. These tasks are created proactively from cross-stream impact analysis of TC-8001 (2.2.x stream). When PSIRT creates a stream-specific CVE Jira for 2.1.x, these tasks will be linked and the `security-preemptive` label removed.

### Task 3: Upstream Backport -- quinn-proto on release/0.3.z (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related (inward: TC-8001, outward: this task) -- preemptive, linked as Related not Depend

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- The upstream branch `release/0.3.z` currently ships quinn-proto 0.11.9
  (at both v0.3.8 and v0.3.12). The fix is NOT yet available on this branch.
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version. If the semver range does not include 0.11.14, update the
  version requirement in `Cargo.toml` and then run `cargo update`.
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

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

### Task 4: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Links**:
- Related (inward: TC-8001, outward: this task) -- preemptive
- Blocks (inward: Task 3, outward: this task) -- blocked by upstream backport

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Coordination Guidance Summary

All remediation tasks for this CVE include the following coordination guidance based on the `customer-shipped` deployment context of rhtpa-backend:

> **This component is shipped to customers.** Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

This guidance applies to all four remediation tasks (Tasks 1-4) because rhtpa-backend has deployment context `customer-shipped` in the Source Repositories table of the CLAUDE.md Security Configuration.

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 tasks (upstream backport + downstream propagation) -- matches Cargo source dependency ecosystem classification
- [x] **Cross-stream coverage**: 2.1.x stream (outside the issue's 2.2.x scope) has preemptive tasks created since no sibling CVE Jira exists
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x), "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x), "Blocks" for upstream -> downstream within a stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: each task's Implementation Notes includes guidance for `customer-shipped` deployment context
- [x] **Dedup consistency**: no dedup detected -- all tasks are new

## Post-Triage Summary

### Triage outcome for TC-8001 (CVE-2026-31812)

**CVE**: CVE-2026-31812 -- quinn-proto panic on large stream counts
**CVSS**: 7.5 (High)
**Library**: quinn-proto (Cargo)
**Fixed version**: 0.11.14

**Affects Versions correction**: RHTPA 2.0.0 (PSIRT-assigned, incorrect) -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Version impact**:

| Stream | Versions affected | Versions not affected | Fix status |
|--------|-------------------|----------------------|------------|
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | Fix shipped in 2.2.3+ |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | -- | Fix not yet on release/0.3.z |

**Remediation tasks created**:

| Task | Stream | Type | Summary |
|------|--------|------|---------|
| Task 1 | 2.2.x | Dependency bump | Update quinn-proto to 0.11.14 (release/0.4.z) |
| Task 2 | 2.2.x | Downstream propagation | Update backend ref in rhtpa-release.0.4.z (blocked by Task 1) |
| Task 3 | 2.1.x | Upstream backport (preemptive) | Bump quinn-proto to 0.11.14 (release/0.3.z) |
| Task 4 | 2.1.x | Downstream propagation (preemptive) | Update backend ref in rhtpa-release.0.3.z (blocked by Task 3) |

**Label**: `ai-cve-triaged` added to TC-8001
