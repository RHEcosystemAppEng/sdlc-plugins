# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two** remediation tasks are created: an upstream backport task and a downstream propagation task with a Blocks dependency.

### Cross-Stream Impact Notice (Case B)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This is outside the scope of TC-8001 (scoped to 2.2.x). A comment would be posted to TC-8001 noting the cross-stream impact, but no tasks are created for 2.1.x -- PSIRT manages per-stream Vulnerability tracking.

---

## PROPOSAL: Task 1 -- Upstream Backport (not executed)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

---

## PROPOSAL: Task 2 -- Downstream Propagation (not executed)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
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
- Depends on: TC-8001 (parent tracking issue)

---

## PROPOSAL: Jira Linkage (not executed)

### 1. Link upstream task to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### 2. Link downstream task as blocked by upstream task

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### 3. Link downstream task to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

---

## PROPOSAL: Cross-Stream Impact Comment (not executed)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- affected
- 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- affected

This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```

## PROPOSAL: Post-Triage Summary Comment (not executed)

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version impact (2.2.x stream):
| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | (0.11.12)   | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation tasks created:
- <upstream-task-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key>: downstream propagation (update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (quinn-proto 0.11.9).
```

## PROPOSAL: Add Label (not executed)

Add `ai-cve-triaged` label to TC-8001 to mark it as triaged.
