# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Decision

**Case B applies**: Supported versions within the issue's stream scope (2.2.x) are affected (2.2.0, 2.2.1, 2.2.2).

**Case A also applies**: The issue is scoped to stream 2.2.x, but stream 2.1.x is also affected. Cross-stream impact must be reported and preemptive remediation tasks created for 2.1.x (if no sibling CVE Jira exists for that stream).

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Upstream fix available on `release/0.4.z`**: YES (quinn-proto 0.11.14 at HEAD)
- **Remediation type**: Dependency bump + downstream propagation (2 tasks for stream 2.2.x)

## Remediation Tasks -- Stream 2.2.x (In-Scope)

### Task 1: Dependency Bump (Source Repository)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Link to TC-8001**: Depend

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed
upstream -- a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

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

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

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

### Task 2: Downstream Propagation (Konflux Release Repo)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Blocked by**: Task 1 (dependency bump)
**Link to TC-8001**: Depend

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
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [dependency-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Jira Linkage for Stream 2.2.x Tasks

1. **Depend**: TC-8001 (inward) -> Task 1 / dependency bump (outward)
2. **Depend**: TC-8001 (inward) -> Task 2 / downstream propagation (outward)
3. **Blocks**: Task 1 / dependency bump (inward) -> Task 2 / downstream propagation (outward)
4. **Blocks**: Task 1 (inward) -> release Task (outward) (if release Jira active from Step 7.5)
5. **Blocks**: Task 2 (inward) -> release Task (outward) (if release Jira active from Step 7.5)
6. **Related**: release Task (inward) -> TC-8001 (outward) (if release Jira active from Step 7.5)

---

## Case A: Cross-Stream Impact -- Stream 2.1.x

### Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream
2.1.x based on lock file analysis.

Version impact in 2.1.x:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- AFFECTED

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for Stream 2.1.x

If no sibling CVE Jira exists for stream 2.1.x (i.e., no issue with label CVE-2026-31812 and summary suffix `[rhtpa-2.1]`), create preemptive remediation tasks:

**Note**: Upstream fix is NOT available on `release/0.3.z` (still at 0.11.9). This requires the upstream backport + downstream propagation pattern (not dependency bump).

#### Preemptive Task 1: Upstream Backport (Source Repository)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link to TC-8001**: Related (not Depend, because this is preemptive for a different stream)

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto denial of service via excessive stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

#### Preemptive Task 2: Downstream Propagation (Konflux Release Repo)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Blocked by**: Preemptive Task 1 (upstream backport)
**Link to TC-8001**: Related

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

### Preemptive Task Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [preemptive-task-1-key] (upstream backport), [preemptive-task-2-key]
  (downstream propagation) (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Affects Versions Correction (Step 3)

Current: [RHTPA 2.0.0]
Proposed (scoped to stream 2.2.x): [RHTPA 2.2.0, RHTPA 2.2.1]

PSIRT assigned RHTPA 2.0.0, which does not correspond to any configured version stream. Based on lock file evidence, the affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (retag of 2.2.1). Version 2.2.2 should be included in Affects Versions if a matching Jira version exists.

## Post-Triage Summary

1. **Version impact**: quinn-proto < 0.11.14 affects RHTPA 2.1.0, 2.1.1 (stream 2.1.x) and RHTPA 2.2.0, 2.2.1, 2.2.2 (stream 2.2.x). Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14).
2. **Affects Versions correction**: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1 (scoped to 2.2.x stream).
3. **Triage outcome**: Case B (remediation needed) + Case A (cross-stream impact on 2.1.x).
4. **Remediation tasks (2.2.x)**: dependency bump task + downstream propagation task (2 tasks).
5. **Preemptive remediation tasks (2.1.x)**: upstream backport task + downstream propagation task (2 tasks, security-preemptive).
6. **Label added**: ai-cve-triaged
