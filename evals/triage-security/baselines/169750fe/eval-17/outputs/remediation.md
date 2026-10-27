# Step 8 -- Remediation

## Triage Outcome

The version impact analysis shows that supported versions ARE affected within the issue's scoped stream (2.2.x) and also in the 2.1.x stream. This triggers:

- **Case A** (Cross-stream impact): the 2.1.x stream is also affected but outside this issue's scope
- **Case B** (Affected -- create remediation tasks): for stream 2.2.x (the issue's scope)

Since the 2.2.x stream's latest versions (2.2.3, 2.2.4) already ship the fix (quinn-proto 0.11.14), and earlier versions (2.2.0, 2.2.1, 2.2.2) are affected, remediation tasks are needed. For the 2.1.x stream, preemptive tasks would be created (Case A) unless a sibling CVE Jira already exists.

## Ecosystem Classification

- Ecosystem: **Cargo** (source dependency)
- Tasks per stream: **2** (dependency bump or upstream backport + downstream propagation)
- Since versions 2.2.3+ already ship the fix, the upstream `release/0.4.z` branch likely has the fix available, which means the **dependency bump** variant applies for stream 2.2.x.

---

## Remediation Tasks for Stream 2.2.x (Issue Scope)

### Task 1: Dependency Bump -- quinn-proto (2.2.x)

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

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
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

### Task 2: Downstream Propagation -- quinn-proto fix (2.2.x)

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
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [dependency-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.2.x)

1. Link dependency bump task to TC-8001 with type **Depend** (CVE inward, task outward)
2. Link downstream propagation task to TC-8001 with type **Depend**
3. Link downstream propagation task as blocked by dependency bump task with type **Blocks**
4. If release Jira is active: link both remediation tasks to the release Task with type **Blocks**; link TC-8001 to the release Task with type **Related**

---

## Preemptive Remediation Tasks for Stream 2.1.x (Case A -- Cross-Stream Impact)

Since the issue is scoped to 2.2.x but the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), preemptive remediation tasks are created for the 2.1.x stream unless a sibling CVE Jira already exists for that stream.

### Task 3: Dependency Bump -- quinn-proto (2.1.x, preemptive)

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
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
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

- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

### Task 4: Downstream Propagation -- quinn-proto fix (2.1.x, preemptive)

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
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: [preemptive-upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

### Jira Linkage (2.1.x -- Preemptive)

1. Link preemptive upstream task to TC-8001 with type **Related** (not Depend -- because TC-8001 is scoped to a different stream)
2. Link preemptive downstream propagation task to TC-8001 with type **Related**
3. Link downstream propagation task as blocked by upstream task with type **Blocks**

---

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** to TC-8001 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created for stream 2.2.x (dependency bump + downstream propagation)
   - Preemptive remediation tasks created for stream 2.1.x
   - Cross-stream impact notice
   - Reporter mention (from issue data)
   - Comment Footnote
3. **Transition** TC-8001 to In Progress
