# Step 8 -- Remediation

## Triage Outcome

The issue TC-8001 is scoped to the **2.2.x** stream. Version impact analysis shows:
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected (Case A -- create remediation tasks)
- **2.1.x stream**: versions 2.1.0, 2.1.1 are affected (Case B -- cross-stream impact, proactive remediation)

Ecosystem: **Cargo** (source dependency) -- each stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for 2.2.x Stream (Scoped)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- The upstream branch release/0.4.z already ships quinn-proto 0.11.14 at v0.4.11+. Verify that the fix is present at branch HEAD before creating a new backport.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

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

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case B: Cross-Stream Impact -- Proactive Remediation for 2.1.x

The issue TC-8001 is scoped to the 2.2.x stream, but version impact analysis reveals that the **2.1.x** stream is also affected (all versions ship quinn-proto 0.11.9, which is within the vulnerable range).

### Cross-stream impact comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x versions 2.1.0 and 2.1.1
both ship quinn-proto 0.11.9.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

Since no existing CVE Jira was found for CVE-2026-31812 scoped to the 2.1.x stream, preemptive remediation tasks are created.

### Preemptive Task 3: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend)

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

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The upstream branch release/0.3.z still ships quinn-proto 0.11.9. An upstream backport PR is required to bump quinn-proto to >= 0.11.14 on this branch.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE issue, cross-stream)

---

### Preemptive Task 4: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend)

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the preemptive upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: preemptive upstream backport task for 2.1.x (upstream backport must merge first)
- Related to: TC-8001 (originating CVE issue, cross-stream)

---

## Preemptive Tasks Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive, upstream backport)
- 2.1.x: [downstream-task-key] (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Task Summary

| # | Type | Stream | Summary | Labels | Link to TC-8001 |
|---|------|--------|---------|--------|-----------------|
| 1 | Upstream backport | 2.2.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation | 2.2.x | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (preemptive) | 2.1.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (preemptive) | 2.1.x | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
