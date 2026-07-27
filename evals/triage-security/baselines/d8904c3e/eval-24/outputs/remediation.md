# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per affected stream
- **Case B**: Create remediation tasks for the 2.2.x stream (within scope)
- **Case A**: Cross-stream impact -- 2.1.x stream is also affected; create preemptive remediation tasks

---

## Case B: Remediation Tasks for 2.2.x Stream (Scoped)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend on TC-8001

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Note: The upstream branch at v0.4.11+ already ships quinn-proto 0.11.14. The fix exists on the release/0.4.z branch at later commits. Backporting to earlier release tags may involve cherry-picking or rebasing the dependency bump.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

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

**Link**: Depend on TC-8001; Blocked by upstream backport task (Task 1 above)

#### Description

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case A: Cross-Stream Impact -- Preemptive Tasks for 2.1.x Stream

The version impact analysis reveals that the 2.1.x stream (outside the issue's scope) is also fully affected:
- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

Cross-stream impact comment (to be posted on TC-8001):
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Since no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (not Depend, because this is a preemptive task for a different stream)

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Note: The upstream branch release/0.3.z does NOT yet have the fix (latest tag v0.3.12 still ships quinn-proto 0.11.9). An upstream PR is required to bump the dependency on this branch.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001; Blocked by upstream backport task (Task 3 above)

#### Description

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
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport: bump quinn-proto to 0.11.14 (2.2.x) | 2.2.x | Upstream backport | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) | 2.2.x | Downstream propagation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport: bump quinn-proto to 0.11.14 (2.1.x) -- preemptive | 2.1.x | Upstream backport (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) -- preemptive | 2.1.x | Downstream propagation (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

**Total tasks**: 4 (2 per affected stream x 2 streams)

### Linkage

- Tasks 1 and 2: linked to TC-8001 with "Depend" (standard remediation within scope)
- Task 2 blocked by Task 1 (downstream blocked by upstream) with "Blocks" link
- Tasks 3 and 4: linked to TC-8001 with "Related" (preemptive, cross-stream)
- Task 4 blocked by Task 3 (downstream blocked by upstream) with "Blocks" link
