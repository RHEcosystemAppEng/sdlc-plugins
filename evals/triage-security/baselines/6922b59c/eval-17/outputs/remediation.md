# Step 8 -- Remediation

## Triage Decision

**Case B (Affected)**: Supported versions within the issue's scope (2.2.x) are affected. Remediation tasks are needed.

**Case A (Cross-stream impact)**: Stream 2.1.x is also affected but is outside this issue's scope (issue is scoped to 2.2.x via `[rhtpa-2.2]`). Preemptive remediation tasks are created for stream 2.1.x.

## Ecosystem Classification

- Ecosystem: **Cargo** (source dependency)
- Tasks per stream: **2** (dependency bump or upstream backport + downstream propagation)
- Stream 2.2.x: upstream fix IS available at `release/0.4.z` (v0.4.11+ ships quinn-proto 0.11.14) -- use **dependency bump** variant
- Stream 2.1.x: upstream fix is NOT available at `release/0.3.z` (v0.3.12 ships quinn-proto 0.11.9) -- use **upstream backport** variant

---

## Stream 2.2.x Remediation Tasks (Standard -- within issue scope)

### Task 1: Dependency Bump (Stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: source dependency (Cargo crate)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira links**:
- Link to TC-8001 with type "Depend" (CVE inward, task outward)

---

### Task 2: Downstream Propagation (Stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: source dependency (carried forward from upstream task)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira links**:
- Link to TC-8001 with type "Depend"
- Link to Task 1 (dependency bump) with type "Blocks" (upstream inward, downstream outward)

---

## Stream 2.1.x Preemptive Remediation Tasks (Cross-stream -- Case A)

These tasks carry the `security-preemptive` label and use "Related" link type to the originating CVE (TC-8001) because the originating CVE belongs to a different stream (2.2.x).

### Task 3: Upstream Backport (Stream 2.1.x, Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

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
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo crate)
- The upstream fix is NOT yet available on release/0.3.z (latest tag v0.3.12
  ships quinn-proto 0.11.9). A backport or dependency bump is required on
  this branch.
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
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

- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

**Jira links**:
- Link to TC-8001 with type "Related" (preemptive -- not "Depend")

---

### Task 4: Downstream Propagation (Stream 2.1.x, Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

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
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: source dependency (carried forward from upstream task)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

**Jira links**:
- Link to TC-8001 with type "Related" (preemptive)
- Link to Task 3 (upstream backport) with type "Blocks" (upstream inward, downstream outward)

---

## Post-Triage Actions Summary

1. **Affects Versions correction**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Cross-stream impact comment**: Post to TC-8001 noting that stream 2.1.x is also affected
3. **Preemptive task comment**: Post to TC-8001 listing preemptive tasks created for stream 2.1.x
4. **Add label**: `ai-cve-triaged` to TC-8001
5. **Post-triage summary comment**: Document version impact table, Affects Versions correction, triage outcome, and links to all 4 remediation tasks

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 tasks (upstream backport + downstream propagation) -- matches Cargo (source dependency) classification
- [x] **Cross-stream coverage**: stream 2.1.x (outside issue scope) gets preemptive tasks
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks); "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x tasks); "Blocks" for upstream to downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: each task includes upstream coordination guidance (deployment context: upstream)
