# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Outcome Summary

- **Case B (Affected)**: Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2). Fix already present in 2.2.3+ (upstream branch `release/0.4.z` has quinn-proto 0.11.14).
- **Case A (Cross-stream impact)**: Stream 2.1.x is also affected (2.1.0, 2.1.1). No stream-specific CVE Jira exists for 2.1.x. Preemptive remediation tasks created.
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Stream 2.2.x -- Standard Remediation Tasks

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Link**: Depend on TC-8001

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1/2.2.2)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is already present on branch release/0.4.z as of tag v0.4.11 (quinn-proto 0.11.14). This task documents the remediation that was picked up in build 0.4.11 (version 2.2.3). No new code change is required unless the fix needs to be verified or backported to an earlier point on the branch.

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Upstream fix is already merged on this branch (v0.4.11+)

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

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

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

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

Note: The fix is already present as of build 0.4.11 (version 2.2.3, tag v0.4.11). Verify that the current source pinning references a tag >= v0.4.11.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Upstream backport task (Task 1) (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Stream 2.1.x -- Preemptive Remediation Tasks

These tasks are created proactively from cross-stream impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists yet for stream 2.1.x.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (not Depend, because TC-8001 belongs to a different stream)

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

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream branch release/0.3.z does NOT yet have the fix. The latest tag v0.3.12 still ships quinn-proto 0.11.9. An upstream backport PR is required to bump quinn-proto to >= 0.11.14 on this branch.

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Upstream fix is NOT yet on this branch -- a backport PR is required

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

- Depends on: TC-8001 (parent tracking issue, cross-stream)

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

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

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Upstream backport task (Task 3) (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue, cross-stream)

---

## Jira Linkage Summary

| Task | Type | Stream | Link to TC-8001 | Blocked By | Labels |
|------|------|--------|-----------------|------------|--------|
| Task 1 (upstream backport) | Standard | 2.2.x | Depend | -- | ai-generated-jira, Security, CVE-2026-31812 |
| Task 2 (downstream propagation) | Standard | 2.2.x | Depend | Task 1 (Blocks) | ai-generated-jira, Security, CVE-2026-31812 |
| Task 3 (upstream backport) | Preemptive | 2.1.x | Related | -- | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| Task 4 (downstream propagation) | Preemptive | 2.1.x | Related | Task 3 (Blocks) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

## Cross-Stream Impact Comment (for TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x does not have a stream-specific
CVE Jira.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: Task 3 (upstream backport, security-preemptive)
- 2.1.x: Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Affects Versions correction**: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Post summary comment** to TC-8001 with version impact table, Affects Versions correction, remediation task links, and @mention of the reporter
