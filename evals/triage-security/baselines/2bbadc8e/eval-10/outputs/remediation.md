# Remediation -- Step 8

## Triage Decision

- **Case A** applies: the issue is stream-scoped to rhtpa-2.2, and cross-stream analysis reveals rhtpa-2.1 is also affected with no sibling CVE Jira.
- **Case B** applies for the current stream (rhtpa-2.2): create standard remediation tasks.
- **Case A preemptive** applies for the other stream (rhtpa-2.1): create preemptive remediation tasks.

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream fix + downstream propagation).

---

## Case B: Standard Remediation Tasks for rhtpa-2.2 (Current Stream)

### Task 1: Upstream Dependency Bump (rhtpa-2.2)

**PROPOSAL -- not executed**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

#### Proposed Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+). tokio versions before 1.42.0 are vulnerable to a
use-after-free when a spawned task is aborted while holding a borrowed
reference, leading to memory corruption and potential code execution.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (tokio is a direct dependency of the backend workspace)
- **Remediation action**: run `cargo update -p tokio` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

#### Proposed Jira Links

```
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**PROPOSAL -- not executed**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

#### Proposed Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream dependency bump (<upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

#### Proposed Jira Links

```
# Link downstream task to CVE
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case A: Preemptive Remediation Tasks for rhtpa-2.1 (Cross-Stream)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira. Preemptive remediation tasks are created with the `security-preemptive` label and linked via "Related" (not "Depend") to the originating CVE TC-8020.

### Task 3: Preemptive Upstream Dependency Bump (rhtpa-2.1)

**PROPOSAL -- not executed**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

#### Proposed Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: bump tokio to 1.42.0 via dependency update.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+). tokio versions before 1.42.0 are vulnerable to a
use-after-free when a spawned task is aborted while holding a borrowed
reference, leading to memory corruption and potential code execution.

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (tokio is a direct dependency of the backend workspace)
- **Remediation action**: run `cargo update -p tokio` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating CVE -- cross-stream, Related link)
```

#### Proposed Jira Links

```
# Link preemptive task to originating CVE with "Related" (not "Depend")
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

---

### Task 4: Preemptive Downstream Propagation (rhtpa-2.1)

**PROPOSAL -- not executed**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

#### Proposed Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream dependency bump (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <preemptive-upstream-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8020 (originating CVE -- cross-stream, Related link)
```

#### Proposed Jira Links

```
# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive downstream as blocked by preemptive upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (upstream bump + downstream propagation). rhtpa-2.2: 2 tasks. rhtpa-2.1: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 has no sibling CVE Jira -- preemptive tasks created for it.
- [x] **Link types**: "Depend" for standard tasks linked to TC-8020, "Related" for preemptive tasks linked to TC-8020, "Blocks" for upstream to downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Deployment context defaults to `upstream` (no Deployment Context column in Source Repositories table).
- [x] **Release Jira linking**: Not shown here (depends on Step 7.5 release Epic/Task resolution).
- [x] **Dedup consistency**: No dedup applies (no existing remediation tasks found).

## Post-Triage Actions (PROPOSALS)

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Post summary comment** to TC-8020 documenting version impact, Affects Versions status, remediation tasks, and cross-stream preemptive tasks
