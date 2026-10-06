# Step 8 -- Remediation

## Triage Outcome

- **Case B (standard remediation)**: Stream rhtpa-2.2 -- the issue's own stream. Create remediation tasks linked to TC-8020 with "Depend" link type.
- **Case A (preemptive remediation)**: Stream rhtpa-2.1 -- affected but no CVE Jira exists. Create preemptive remediation tasks linked to TC-8020 with "Related" link type and `security-preemptive` label.

Ecosystem: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case B: Standard Remediation for rhtpa-2.2

### Task 1: Upstream Backport (rhtpa-2.2)

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

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (tokio is a direct runtime dependency)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
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

### Task 2: Downstream Propagation (rhtpa-2.2)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

```markdown
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
- **Dependency type**: direct -- carried forward from upstream task
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
# Link downstream to CVE Jira
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case A: Preemptive Remediation for rhtpa-2.1

No CVE Jira exists for CVE-2026-55123 in stream rhtpa-2.1. Creating preemptive remediation tasks with `security-preemptive` label and "Related" link type to the originating CVE Jira TC-8020.

### Task 3: Upstream Backport -- Preemptive (rhtpa-2.1)

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

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (tokio is a direct runtime dependency)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira -- different stream)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

### Task 4: Downstream Propagation -- Preemptive (rhtpa-2.1)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

```markdown
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
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira -- different stream)
```

**Linkage:**
```
# Link preemptive downstream to originating CVE Jira
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo is a source dependency ecosystem -- 2 tasks per stream (upstream backport + downstream propagation). rhtpa-2.2 gets 2 tasks, rhtpa-2.1 gets 2 tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 (the only affected stream outside the issue's scope) gets preemptive tasks since no sibling CVE Jira exists.
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020; "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020; "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Omitted -- Source Repositories table has no Deployment Context column.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8020.
2. Transition TC-8020 to In Progress.
3. Post summary comment to TC-8020 with version impact table, Affects Versions correction, and links to all 4 remediation tasks.
