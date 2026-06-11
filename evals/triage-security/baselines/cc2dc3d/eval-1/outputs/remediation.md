# Step 7 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks.**

The issue is scoped to the 2.2.x stream, and versions 2.2.0, 2.2.1, and 2.2.2 are affected. quinn-proto is a Cargo (source dependency) ecosystem package, so **two tasks** are required: one upstream backport task and one downstream propagation subtask.

The upstream fix is already available on the 2.2.x stream's release branch (tag v0.4.11 ships quinn-proto 0.11.14), which means the upstream backport task may already be partially or fully resolved. However, the affected versions (2.2.0, 2.2.1, 2.2.2) were built from earlier tags that ship vulnerable versions.

---

## Task 1: Upstream Backport Task

**Proposed Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Proposed Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream branch release/0.4.z already includes the fix as of tag v0.4.11
(quinn-proto 0.11.14). This task may already be resolved -- verify that the fix
is present on the branch HEAD and that no additional backport is needed.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: tag v0.4.11 already ships 0.11.14, so the fix may already
  be on the branch -- verify before making changes

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Proposed Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Proposed Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

Affected versions that need a rebuild: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
  that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully
- Note: Since tag v0.4.11 already includes the fix, the downstream
  propagation may involve pointing affected version rebuilds to
  v0.4.11 or later

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Proposed Jira Operations (require engineer confirmation)

### 1. Create upstream backport task

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 2. Create downstream propagation subtask

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 3. Link tasks to vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

### 4. Link downstream as blocked by upstream

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### 5. Transition and assign

- Transition TC-8001 to "In Progress"
- Assign TC-8001 to current user

### 6. Add ai-cve-triaged label

Add the `ai-cve-triaged` label to TC-8001 to mark it as triaged.

### 7. Post summary comment to TC-8001

```
Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14):

Version Impact:
| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation tasks created:
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (RHTPA 2.1.0, RHTPA 2.1.1 ship quinn-proto 0.11.9).

---
_Comment generated by `/sdlc-workflow:triage-security`_
```
