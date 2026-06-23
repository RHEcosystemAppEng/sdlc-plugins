# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are required: an upstream backport task and a downstream propagation subtask.

**Note**: The latest builds in the 2.2.x stream (2.2.3 at v0.4.11 and 2.2.4 at v0.4.12) already ship quinn-proto 0.11.14. The upstream fix is already present on the `release/0.4.z` branch. The upstream backport task may already be satisfied -- the downstream propagation task ensures the affected earlier versions are covered if z-stream rebuilds are needed.

## Cross-Stream Impact Notice (Case B)

The version impact analysis reveals that the **2.1.x** stream (versions 2.1.0 and 2.1.1, both shipping quinn-proto 0.11.9) is also affected. This is outside TC-8001's scope. A comment would be posted:

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The latest builds on release/0.4.z (v0.4.11, v0.4.12) already ship quinn-proto 0.11.14. This task may already be satisfied by existing commits on the branch. Verify that the fix is present at the branch HEAD before creating a new PR.

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

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Operations (would execute after engineer confirmation)

### Task Creation

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Linkage

```
# Link upstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")

# Link downstream as blocked by upstream
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Transition TC-8001 to In Progress
3. Assign TC-8001 to current user
4. Post summary comment with version impact table, Affects Versions correction, and links to created tasks
