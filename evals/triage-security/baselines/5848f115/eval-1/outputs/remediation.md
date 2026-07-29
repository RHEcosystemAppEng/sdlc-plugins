# Step 8 -- Remediation

## Triage Outcome

- **Case A applies**: The issue is scoped to stream 2.2.x, but the version impact analysis reveals that the 2.1.x stream is also affected. Cross-stream impact comment and preemptive remediation tasks are needed for 2.1.x.
- **Case B applies**: Affected versions exist within the issue's scoped stream (2.2.x: versions 2.2.0, 2.2.1, 2.2.2). Remediation tasks are needed.
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact (2.1.x stream)

### Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x

Since no sibling CVE Jira exists for the 2.1.x stream (none found in Step 4), preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

---

## Remediation Task Descriptions

### Task 1: Upstream Backport -- 2.2.x stream (standard)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend (TC-8001 -> this task)

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: [to be determined via dependency chain analysis in Step 2.3.5]

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock
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

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

---

### Task 2: Downstream Propagation -- 2.2.x stream (standard)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Links**:
- Depend (TC-8001 -> this task)
- Blocks (upstream task -> this task) -- this task is blocked by the upstream backport task

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from [upstream-task-key].

The upstream backport ([upstream-task-key]) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: [carried forward from upstream task]
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

### Task 3: Upstream Backport -- 2.1.x stream (preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related (TC-8001 -> this task) -- preemptive tasks use "Related" not "Depend"

#### Description

```
## Repository

rhtpa-backend

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

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: [to be determined via dependency chain analysis in Step 2.3.5]

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock
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

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- Related link)
```

---

### Task 4: Downstream Propagation -- 2.1.x stream (preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Links**:
- Related (TC-8001 -> this task) -- preemptive tasks use "Related" not "Depend"
- Blocks (preemptive upstream task -> this task) -- this task is blocked by the preemptive upstream backport task

#### Description

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from [preemptive-upstream-task-key].

The upstream backport ([preemptive-upstream-task-key]) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: [carried forward from upstream task]
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [preemptive-upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- Related link)
```

---

## Preemptive Task Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (upstream backport, security-preemptive),
         [downstream-task-key] (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport (bump quinn-proto to 0.11.14) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation (update ref in rhtpa-release.0.4.z) | 2.2.x | Standard (blocked by Task 1) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (bump quinn-proto to 0.11.14) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (update ref in rhtpa-release.0.3.z) | 2.1.x | Preemptive (blocked by Task 3) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
