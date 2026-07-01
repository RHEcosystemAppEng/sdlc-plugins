# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome: Case A + Case B

- **Case A (Affected)**: Stream 2.2.x versions 2.2.0, 2.2.1, and 2.2.2 are affected. Create remediation tasks for the 2.2.x stream.
- **Case B (Cross-stream impact)**: Stream 2.1.x (all versions: 2.1.0, 2.1.1) is also affected but outside this issue's stream scope. Post cross-stream impact comment and create preemptive remediation tasks if no companion CVE Jira exists for stream 2.1.x.

The ecosystem is **Cargo** (source dependency), so **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task (2.2.x)

**PROPOSAL**: Create Jira Task with the following details:

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5: quinn-proto 0.11.9), 2.2.1 (v0.4.8: quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

**Proposed Jira API call**:
```
PROPOSAL: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task 2: Downstream Propagation Subtask (2.2.x)

**PROPOSAL**: Create Jira Task with the following details:

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
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Proposed Jira API call**:
```
PROPOSAL: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Linkage for 2.2.x Tasks

```
PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

PROPOSAL: jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Impact (2.1.x)

### Cross-Stream Impact Comment

**PROPOSAL**: Post comment to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.

  - 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- affected
  - 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- affected

The 2.1.x stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x

If no companion CVE Jira exists for stream 2.1.x (checked via JQL search for CVE-2026-31812 label with `[rhtpa-2.1]` suffix), create preemptive remediation tasks:

#### Preemptive Task 1: Upstream Backport (2.1.x)

**PROPOSAL**: Create Jira Task with the following details:

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8: quinn-proto 0.11.9), 2.1.1 (v0.3.12: quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- NOTE: Upstream branch release/0.3.z currently ships quinn-proto 0.11.9 --
  the fix has NOT landed on this branch yet. An upstream PR is required first.

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

- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

**Proposed Jira API call**:
```
PROPOSAL: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <preemptive-upstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Preemptive Task 2: Downstream Propagation (2.1.x)

**PROPOSAL**: Create Jira Task with the following details:

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
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, cross-stream)
```

**Proposed Jira API call**:
```
PROPOSAL: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <preemptive-downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Preemptive Task Linkage (2.1.x)

Preemptive tasks use "Related" link type (not "Depend") since they are linked to a different stream's CVE Jira:

```
PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

PROPOSAL: jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

### Preemptive Task Summary Comment

**PROPOSAL**: Post comment to TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Actions

### Add ai-cve-triaged Label

**PROPOSAL**: Add `ai-cve-triaged` label to TC-8001 to mark it as triaged.

### Transition Issue

**PROPOSAL**: Transition TC-8001 to "In Progress" status.

### Post-Triage Summary Comment

**PROPOSAL**: Post summary comment to TC-8001:

```
## Triage Summary for CVE-2026-31812 (quinn-proto < 0.11.14)

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(Scoped to stream 2.2.x per issue suffix [rhtpa-2.2])

### Triage Outcome

Case A + Case B: Remediation tasks created for stream 2.2.x (in scope);
preemptive remediation tasks created for stream 2.1.x (cross-stream impact).

### Remediation Tasks

Stream 2.2.x:
- <upstream-task-key>: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.4.z
- <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by upstream task)

Stream 2.1.x (preemptive):
- <preemptive-upstream-task-key>: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (security-preemptive)
- <preemptive-downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (security-preemptive)

@<reporter-name> (reporter)
```

All proposed Jira mutations require engineer confirmation before execution.
