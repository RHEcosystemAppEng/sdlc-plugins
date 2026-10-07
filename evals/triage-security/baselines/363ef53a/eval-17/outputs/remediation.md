# Step 8 -- Remediation for CVE-2026-31812

## Triage Outcome: Case B (Affected) with Case A (Cross-stream impact)

The issue is scoped to stream 2.2.x. Within that stream, versions 2.2.0, 2.2.1,
and 2.2.2 are affected. Stream 2.1.x is also affected but outside this issue's
scope, triggering Case A cross-stream handling.

---

## Case A: Cross-Stream Impact Comment

Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected by CVE-2026-31812
(quinn-proto < 0.11.14) but is outside this issue's scope (scoped to 2.2.x).

Cross-stream impact comment posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
> based on lock file analysis. This stream is tracked by companion issues
> (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks
are created (see Preemptive Tasks below).

---

## Case B: Remediation Tasks for Stream 2.2.x (scoped stream)

Since Step 2.5 confirms the upstream branch `release/0.4.z` already ships
quinn-proto 0.11.14 (the fix), the dependency bump variant is used instead
of upstream backport.

### Task 1: Dependency Bump -- Stream 2.2.x

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Issue Type**: Task
**Link**: Depend on TC-8001

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9 (retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: [direct or transitive -- determined by Cargo.toml inspection]
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

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

### Task 2: Downstream Propagation -- Stream 2.2.x

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Issue Type**: Task
**Link**: Depend on TC-8001; Blocked by Task 1 (dependency bump)

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

---

## Case A: Preemptive Remediation Tasks for Stream 2.1.x

These tasks are created proactively because stream 2.1.x is affected but has no
stream-specific CVE Jira (assuming no sibling found in Step 4). They carry the
`security-preemptive` label and use "Related" link type to TC-8001.

Since Step 2.5 shows the upstream branch `release/0.3.z` does NOT yet ship the
fix (still at 0.11.9), the upstream backport variant is used.

### Preemptive Task 1: Upstream Backport -- Stream 2.1.x

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Issue Type**: Task
**Link**: Related to TC-8001 (not Depend, because TC-8001 belongs to a different stream)

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

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: [direct or transitive -- determined by Cargo.toml inspection]
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- The upstream branch release/0.3.z does NOT yet ship the fix -- this requires
  a backport of the fix to the 0.3.z release branch

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- Related link)
```

### Preemptive Task 2: Downstream Propagation -- Stream 2.1.x

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Issue Type**: Task
**Link**: Related to TC-8001; Blocked by Preemptive Task 1 (upstream backport)

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

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- Related link)
```

---

## Jira Linkage Summary

### Stream 2.2.x (scoped -- standard remediation)
- Task 1 (dependency bump) --> TC-8001: **Depend**
- Task 2 (downstream propagation) --> TC-8001: **Depend**
- Task 1 (dependency bump) --> Task 2 (downstream propagation): **Blocks**
- Task 1 --> release Task: **Blocks** (if release Jira active from Step 7.5)
- Task 2 --> release Task: **Blocks** (if release Jira active from Step 7.5)
- TC-8001 --> release Task: **Related** (if release Jira active from Step 7.5)

### Stream 2.1.x (preemptive -- cross-stream)
- Preemptive Task 1 (upstream backport) --> TC-8001: **Related** (not Depend)
- Preemptive Task 2 (downstream propagation) --> TC-8001: **Related** (not Depend)
- Preemptive Task 1 --> Preemptive Task 2: **Blocks**

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x = 2 tasks (dependency bump + downstream propagation); 2.1.x = 2 tasks (upstream backport + downstream propagation). Matches Cargo ecosystem classification (source dependency = 2 tasks).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created.
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks to TC-8001); "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x tasks to TC-8001); "Blocks" for upstream/bump to downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: omitted -- Source Repositories table does not include a Deployment Context column (backward compatibility).
- [x] **Release Jira linking**: if Step 7.5 produced a release Task, non-preemptive remediation tasks are linked to it (Blocks) and CVE is linked to it (Related).
- [x] **Dedup consistency**: no dedup flags from Step 7.5.3 in this triage scenario.
