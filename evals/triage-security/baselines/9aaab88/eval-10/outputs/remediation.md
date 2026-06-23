# Step 7 -- Remediation

## Triage Decision

Affected supported versions exist in the issue's scoped stream (rhtpa-2.2) AND in another stream (rhtpa-2.1). This triggers both Case A (standard remediation for rhtpa-2.2) and Case B (preemptive remediation for rhtpa-2.1).

---

## Case A: Standard Remediation for rhtpa-2.2 (Issue Stream)

The issue TC-8020 is scoped to stream rhtpa-2.2. Both RHTPA 2.2.0 and RHTPA 2.2.1 ship tokio 1.41.1, which is below the fix threshold of 1.42.0. Since tokio is a Cargo (source dependency) ecosystem, two tasks are created.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio versions before 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

**Linkage:**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Task description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Linkage:**

```
# Link downstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
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

## Case B: Preemptive Remediation for rhtpa-2.1 (Cross-Stream, No CVE Jira)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no sibling CVE Jira for CVE-2026-55123. Per Step 7 Case B, preemptive remediation tasks are created with:

- Additional label: `security-preemptive`
- Link type: **"Related"** (not "Depend") to the originating CVE Jira TC-8020
- Preemptive prefix in description noting TC-8020 as originating CVE

### Task 3: Upstream Backport Task -- Preemptive (rhtpa-2.1)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio versions before 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

**Linkage (Related, not Depend):**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

### Task 4: Downstream Propagation Subtask -- Preemptive (rhtpa-2.1)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Task description:**

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Linkage (Related, not Depend):**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link downstream preemptive subtask as blocked by upstream preemptive task
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Summary of All Tasks

| # | Task | Stream | Type | Labels | Link to TC-8020 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport (rhtpa-2.2) | rhtpa-2.2 | Standard | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| 2 | Downstream propagation (rhtpa-2.2) | rhtpa-2.2 | Standard | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| 3 | Upstream backport (rhtpa-2.1) | rhtpa-2.1 | Preemptive | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| 4 | Downstream propagation (rhtpa-2.1) | rhtpa-2.1 | Preemptive | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

## Post-Remediation Actions

1. **Transition** TC-8020 to In Progress
2. **Assign** TC-8020 to current user
3. **Add `ai-cve-triaged` label** to TC-8020
4. **Post summary comment** to TC-8020 documenting the version impact table, Affects Versions status, and links to all created remediation tasks
