# Step 8 -- Remediation

## Triage Decision

- **Issue scope**: 2.2.x stream (scoped via suffix `[rhtpa-2.2]`)
- **Affected versions in-scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream
- **Upstream fix status (2.2.x)**: FIXED on release/0.4.z (latest tags ship quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x stream is also affected (Case A applies)

Since the upstream branch `release/0.4.z` already ships the fixed version,
the 2.2.x remediation uses the **dependency bump + downstream propagation**
variant (2 tasks).

The 2.1.x stream is also affected but is outside this issue's scope.
Case A applies: post a cross-stream impact comment and create preemptive
remediation tasks for the 2.1.x stream (assuming no sibling CVE Jira exists
for 2.1.x).

---

## Case B: In-scope remediation (2.2.x stream)

### Task 1: Dependency bump -- quinn-proto on release/0.4.z

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

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
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

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

**Jira creation:**
```
bump_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <dependency-bump-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")
```

---

### Task 2: Downstream propagation -- update backend ref in rhtpa-release.0.4.z

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira creation:**
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Case A: Cross-stream impact -- preemptive remediation (2.1.x stream)

The version impact analysis shows that 2.1.x versions (2.1.0, 2.1.1) are also
affected (quinn-proto 0.11.9 < 0.11.14). Since this issue is scoped to
the 2.2.x stream and no sibling CVE Jira exists for the 2.1.x stream,
preemptive remediation tasks are created with the `security-preemptive` label.

The upstream branch `release/0.3.z` does NOT have the fix (both tags v0.3.8 and
v0.3.12 ship quinn-proto 0.11.9). Therefore the 2.1.x remediation uses the
**upstream backport + downstream propagation** variant.

### Cross-stream impact comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.
This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Task 3 (preemptive): Upstream backport -- quinn-proto on release/0.3.z

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

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 on release/0.3.z.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira creation:**
```
upstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-backport-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Linkage (preemptive -- Related, not Depend):**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-21-key>, type: "Related")
```

---

### Task 4 (preemptive): Downstream propagation -- update backend ref in rhtpa-release.0.3.z

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
CVE-2026-31812 fix from <upstream-task-21-key>.

The upstream backport (<upstream-task-21-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-21-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira creation:**
```
downstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Linkage (preemptive -- Related to CVE, Blocks from upstream):**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-21-key>, type: "Related")
jira.create_link(inwardIssue: <upstream-task-21-key>, outwardIssue: <downstream-task-21-key>, type: "Blocks")
```

---

## Pre-creation checklist

- [x] **Task count per stream**: 2.2.x = 2 tasks (dependency bump + downstream), 2.1.x = 2 tasks (upstream backport + downstream) -- matches Cargo source dependency classification
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) covered by preemptive tasks
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks), "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x tasks), "Blocks" for upstream -> downstream within a stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: each task includes upstream coordination guidance (deployment context: upstream)
- [x] **Release Jira linking**: would be linked after Step 7.5 release Jira orchestration (not simulated in this eval)
- [x] **Dedup consistency**: no dedup detected -- all tasks are newly created

## Task summary

| # | Stream | Task Type | Summary | Labels |
|---|--------|-----------|---------|--------|
| 1 | 2.2.x | Dependency bump | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
