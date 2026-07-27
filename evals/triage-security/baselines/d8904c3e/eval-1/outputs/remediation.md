# Step 8 -- Remediation

## Triage Outcome

- **Case A** (cross-stream impact): The 2.1.x stream is also affected but outside this issue's scope (issue is scoped to 2.2.x).
- **Case B** (affected -- create remediation tasks): Versions 2.2.0, 2.2.1, and 2.2.2 within the 2.2.x stream are affected.
- Ecosystem: **Cargo** (source dependency) --> **2 tasks per affected stream** (upstream backport + downstream propagation)

---

## Stream 2.2.x -- Standard Remediation Tasks (within issue scope)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct or transitive (to be confirmed via dependency chain analysis)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

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

**Link**: Depend (TC-8001 --> this task)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Links**:
- Depend (TC-8001 --> this task)
- Blocks (upstream backport task --> this task)

---

## Stream 2.1.x -- Preemptive Remediation Tasks (Case A, cross-stream impact)

The 2.1.x stream is affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9) but has no stream-specific CVE Jira for CVE-2026-31812. Preemptive remediation tasks are created proactively.

### Task 3: Preemptive Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

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

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (to be confirmed via dependency chain analysis)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

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

**Link**: Related (TC-8001 --> this task) -- uses "Related" not "Depend" because this is a preemptive task linked to another stream's CVE Jira

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

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

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Links**:
- Related (TC-8001 --> this task) -- preemptive link type
- Blocks (preemptive upstream backport task --> this task)

---

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Upstream backport | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Downstream propagation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Preemptive upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Upstream backport (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Preemptive downstream propagation: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Downstream propagation (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

## Cross-Stream Impact Comment (Case A)

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> This stream is not tracked by a companion CVE Jira.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <task-3-key> (upstream backport, security-preemptive), <task-4-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
