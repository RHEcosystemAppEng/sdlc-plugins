# Step 8 -- Remediation

## Triage Outcome: Case B (Affected -- create remediation tasks)

The version impact analysis shows that supported versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Additionally, Case A applies because the 2.1.x stream is also affected (cross-stream impact).

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** are created per stream: an upstream backport task and a downstream propagation subtask.

---

## Remediation Tasks for Stream 2.2.x (scoped stream)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend on TC-8001 (Vulnerability issue)

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or verify via dependency chain analysis)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If quinn-proto is transitive, use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency,
  overriding the transitive resolution

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
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link**: Depend on TC-8001; Blocked by upstream backport task (Task 1)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case A: Cross-Stream Impact -- Remediation Tasks for Stream 2.1.x (proactive)

The version impact analysis reveals that stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since the current issue TC-8001 is scoped to 2.2.x, proactive remediation tasks are created for the 2.1.x stream with the `security-preemptive` label, linked via "Related" (not "Depend") to TC-8001.

### Task 3: Upstream Backport (2.1.x -- preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or verify via dependency chain analysis)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE from stream 2.2.x)

---

### Task 4: Downstream Propagation (2.1.x -- preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001; Blocked by upstream backport task (Task 3)

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for 2.1.x (must merge first)
- Depends on: TC-8001 (originating CVE from stream 2.2.x)

---

## Linkage Summary

| Task | Type | Link to TC-8001 | Blocked By |
|------|------|-----------------|------------|
| Task 1 (upstream 2.2.x) | Standard | Depend | -- |
| Task 2 (downstream 2.2.x) | Standard | Depend | Task 1 (Blocks) |
| Task 3 (upstream 2.1.x) | Preemptive | Related | -- |
| Task 4 (downstream 2.1.x) | Preemptive | Related | Task 3 (Blocks) |

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency) -- 2 for 2.2.x, 2 for 2.1.x = 4 total
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created (Tasks 3 and 4)
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x), "Related" for preemptive tasks (2.1.x), "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: Tasks 3 and 4 carry the `security-preemptive` label
- [x] **Coordination guidance**: deployment context defaults to `upstream` (no Deployment Context column in Source Repositories table)
