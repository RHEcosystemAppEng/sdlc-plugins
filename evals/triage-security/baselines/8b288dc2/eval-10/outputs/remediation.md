# Remediation — CVE-2026-55123 (TC-8020)

## Triage Outcome

- **Case A**: Create standard remediation tasks for stream rhtpa-2.2 (issue scope)
- **Case B**: Create preemptive remediation tasks for stream rhtpa-2.1 (no CVE Jira exists)

---

## Case A: Standard Remediation Tasks for rhtpa-2.2

Ecosystem: Cargo (source dependency) -- creates **two** tasks: upstream backport + downstream propagation.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Jira Creation:**

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
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

**Jira Creation:**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Linkage:**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Preemptive Remediation Tasks for rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira**.
Preemptive tasks are created with the `security-preemptive` label and linked via "Related" (not "Depend") to TC-8020.

Ecosystem: Cargo (source dependency) -- creates **two** preemptive tasks: upstream backport + downstream propagation.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Jira Creation:**

```
upstream_task_preemptive = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

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

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
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
  outwardIssue: <upstream-task-preemptive-key>,
  type: "Related"
)
```

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Jira Creation:**

```
downstream_task_preemptive = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

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
CVE-2026-55123 fix from <upstream-task-preemptive-key>.

The upstream backport (<upstream-task-preemptive-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-preemptive-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Linkage (Related, not Depend):**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-preemptive-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: <upstream-task-preemptive-key>,
  outwardIssue: <downstream-task-preemptive-key>,
  type: "Blocks"
)
```

---

## Summary of All Tasks

| Task | Stream | Type | Labels | Link to TC-8020 |
|------|--------|------|--------|-----------------|
| Upstream backport (rhtpa-2.2) | rhtpa-2.2 | Standard | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| Downstream propagation (rhtpa-2.2) | rhtpa-2.2 | Standard | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| Upstream backport (rhtpa-2.1) | rhtpa-2.1 | Preemptive | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation (rhtpa-2.1) | rhtpa-2.1 | Preemptive | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
