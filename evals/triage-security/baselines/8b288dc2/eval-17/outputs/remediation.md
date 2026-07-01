# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected** -- The 2.2.x stream (the issue's scoped stream) has affected versions (2.2.0, 2.2.1, 2.2.2). Remediation tasks are needed.

**Case B: Cross-stream impact** -- The 2.1.x stream is also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted, and proactive remediation tasks would be created for 2.1.x if no companion CVE Jira exists for that stream.

## Remediation Tasks -- 2.2.x Stream (Scoped)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created for the 2.2.x stream:

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.2.x)

1. Link upstream task to TC-8001 with link type "Depend"
2. Link downstream subtask to TC-8001 with link type "Depend"
3. Link downstream subtask as blocked by upstream task with link type "Blocks"
4. Transition TC-8001 to In Progress
5. Assign TC-8001 to current user
6. Add `ai-cve-triaged` label to TC-8001

---

## Proactive Remediation Tasks -- 2.1.x Stream (Cross-stream, Case B)

The 2.1.x stream is also affected but has no stream-scoped CVE Jira. Proactive remediation tasks are created with the `security-preemptive` label.

### Cross-Stream Impact Comment (posted to TC-8001):

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 ship quinn-proto
0.11.9 which is within the affected range.
This stream may be tracked by a companion issue or may require separate
PSIRT triage.
```

### Task 3: Upstream Backport Task (Preemptive, 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

#### Description:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Note: upstream branch release/0.3.z currently has quinn-proto 0.11.9 --
  an upstream PR is needed first to bump the dependency
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- Related link, not Depend)
```

### Task 4: Downstream Propagation Subtask (Preemptive, 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

#### Description:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- Related link, not Depend)
```

### Jira Linkage (2.1.x Preemptive)

1. Link upstream task (preemptive) to TC-8001 with link type "Related" (not "Depend")
2. Link downstream subtask (preemptive) to TC-8001 with link type "Related" (not "Depend")
3. Link downstream subtask as blocked by upstream task with link type "Blocks"
4. Post preemptive task comment to TC-8001 listing all preemptive tasks created

### Preemptive Task Comment (posted to TC-8001):

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream task key (security-preemptive), downstream task key (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
