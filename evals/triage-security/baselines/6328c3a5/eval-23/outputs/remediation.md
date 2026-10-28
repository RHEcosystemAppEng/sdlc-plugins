# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case B** (Affected -- create remediation tasks) for stream 2.2.x (in-scope).
**Case A** (Cross-stream impact) for stream 2.1.x (preemptive remediation).

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream.

For the 2.2.x stream, Step 2.5 confirms the upstream branch `release/0.4.z` already ships the fixed version (v0.4.11 and v0.4.12 include quinn-proto 0.11.14). The **dependency bump** variant applies.

For the 2.1.x stream, the latest release (v0.3.12) still ships quinn-proto 0.11.9 and the fix does not appear available on `release/0.3.z`. The **upstream backport** variant applies. These tasks are **preemptive** (security-preemptive label, Related link type).

---

## Task 1: Dependency Bump -- Stream 2.2.x (in-scope)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend (inward: TC-8001, outward: this task)

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of v0.4.8)
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

## Task 2: Downstream Propagation -- Stream 2.2.x (in-scope)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Links**:
- Blocks (inward: Task 1, outward: this task) -- blocked by upstream dependency bump
- Depend (inward: TC-8001, outward: this task)

### Description

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
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

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Task 3: Upstream Backport -- Stream 2.1.x (preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related (inward: TC-8001, outward: this task) -- preemptive, not Depend

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
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

## Task 4: Downstream Propagation -- Stream 2.1.x (preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Links**:
- Blocks (inward: Task 3, outward: this task) -- blocked by upstream backport
- Related (inward: TC-8001, outward: this task) -- preemptive

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
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

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Coordination Guidance Section

The Deployment Context for the affected repository `rhtpa-backend` is **customer-shipped**, as configured in the Source Repositories table of the project CLAUDE.md.

All remediation task descriptions include the following Coordination Guidance subsection under Implementation Notes:

> ### Coordination Guidance
>
> This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

This guidance was selected based on the `customer-shipped` deployment context value from the Source Repositories table. The three possible deployment context values and their guidance are:

| Deployment Context | Coordination Guidance |
|--------------------|-----------------------|
| internal | Develop and merge the fix within the repository. No public advisory or upstream coordination required. |
| upstream | Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs. |
| **customer-shipped** | **Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.** |

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo source dependency: upstream fix + downstream propagation) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: Stream 2.1.x (outside issue scope) has preemptive tasks created (Tasks 3 and 4)
- [x] **Link types**: "Depend" for in-scope tasks (2.2.x) linked to TC-8001; "Related" for preemptive tasks (2.1.x) linked to TC-8001; "Blocks" for upstream-to-downstream within each stream
- [x] **Preemptive labels**: Tasks 3 and 4 (stream 2.1.x) carry the `security-preemptive` label
- [x] **Coordination guidance**: Each task's Implementation Notes includes the `customer-shipped` coordination guidance
- [x] **Dedup consistency**: No dedup scenario detected -- all tasks are new

## Summary of Remediation Tasks

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Dependency bump: update quinn-proto to 0.11.14 (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.4.z (2.2.x) | 2.2.x | Standard (blocked by Task 1) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport: bump quinn-proto to 0.11.14 (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation: update backend ref in rhtpa-release.0.3.z (2.1.x) | 2.1.x | Preemptive (blocked by Task 3) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
