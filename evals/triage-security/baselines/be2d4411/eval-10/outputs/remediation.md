# Remediation Tasks — CVE-2026-55123 (TC-8020)

## Case A: Standard Remediation Tasks for rhtpa-2.2

The issue TC-8020 is scoped to stream rhtpa-2.2. Versions RHTPA 2.2.0 and RHTPA 2.2.1
ship tokio 1.41.1, which is below the fix threshold of 1.42.0. Two tasks are created
for this Cargo ecosystem vulnerability: an upstream backport task and a downstream
propagation subtask.

### Task 1 — Upstream Backport (rhtpa-2.2)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link to TC-8020**: Depend
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in task abort in tokio.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
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

### Task 2 — Downstream Propagation (rhtpa-2.2)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Link to TC-8020**: Depend
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

**Link to upstream task**: Blocks (downstream blocked by upstream)
```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

**Task description:**

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

---

## Case B: Preemptive Remediation Tasks for rhtpa-2.1

Stream rhtpa-2.1 is also affected (tokio 1.40.0, threshold 1.42.0) but has no
CVE Jira of its own. No sibling Vulnerability issue was found for CVE-2026-55123
in stream rhtpa-2.1. Proactive preemptive remediation tasks are created with the
`security-preemptive` label and "Related" link type.

### Task 3 — Upstream Backport (rhtpa-2.1, preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link to TC-8020**: Related (not Depend, since different stream)
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

**Task description:**

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

Remediate CVE-2026-55123: use-after-free in task abort in tokio.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
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

- Depends on: TC-8020 (originating CVE issue, cross-stream)
```

### Task 4 — Downstream Propagation (rhtpa-2.1, preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Link to TC-8020**: Related (not Depend, since different stream)
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)
```

**Link to preemptive upstream task**: Blocks (downstream blocked by upstream)
```
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE issue, cross-stream)
```
