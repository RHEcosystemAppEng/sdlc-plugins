# Step 8 -- Remediation

## Triage Outcome

This is **Case B** (affected -- create remediation tasks) combined with **Case A** (cross-stream impact).

### Case Assessment

- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Affected versions in scoped stream (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in scoped stream**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x stream is also affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation)

## Case A: Cross-Stream Impact

The 2.1.x stream is affected but outside this issue's scope. A cross-stream impact comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship
quinn-proto 0.11.9 which is within the vulnerable range.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

A JQL search for sibling CVE Jiras with label `CVE-2026-31812` and stream suffix `[rhtpa-2.1]` would determine whether preemptive tasks are needed for the 2.1.x stream. If no sibling exists, preemptive remediation tasks (with `security-preemptive` label and "Related" link type) would be created for stream 2.1.x.

---

## Case B: Remediation Tasks for Stream 2.2.x (Scoped)

### Task 1: Upstream Backport Task (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12),
2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
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

## Preemptive Tasks for Stream 2.1.x (Cross-Stream, Case A)

If no sibling CVE Jira exists for stream 2.1.x, create preemptive remediation tasks:

### Preemptive Task 1: Upstream Backport (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

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

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage (preemptive -- uses "Related" not "Depend"):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
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
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage (preemptive -- uses "Related" not "Depend"):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) = 2 tasks per stream (upstream backport + downstream propagation). 2.2.x gets 2 standard tasks; 2.1.x gets 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: The 2.1.x stream (outside issue scope) is covered by preemptive tasks (if no sibling CVE Jira exists).
- [x] **Link types**: "Depend" for standard tasks linked to TC-8001; "Related" for preemptive tasks linked to TC-8001; "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: No Deployment Context column in Source Repositories table (backward compatibility) -- coordination guidance subsection is omitted.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001.
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (standard for 2.2.x, preemptive for 2.1.x)
   - @mention of the vulnerability issue reporter
3. Transition TC-8001 to In Progress.
