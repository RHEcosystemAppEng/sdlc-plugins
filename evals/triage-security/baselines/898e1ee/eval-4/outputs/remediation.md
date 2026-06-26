# Step 7 -- Remediation: TC-8004

## Triage Outcome: Case A -- Affected (create remediation tasks)

The version impact analysis shows that the **2.1.x stream** is affected (ships h2 0.4.5, below the fix threshold of 0.4.8). The **2.2.x stream** is not affected (ships h2 >= 0.4.8).

Since the issue is **unscoped**, remediation tasks are created only for actually affected streams. No cross-stream impact notice (Case B) is generated because the issue already covers all streams by definition.

## Remediation Tasks for Stream 2.1.x

The h2 crate is a Cargo (source dependency) ecosystem package. Per the remediation templates, this requires **two tasks**: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
> The vulnerable dependency (h2 versions before 0.4.8) must be updated
> to the fixed version (0.4.8+).
>
> Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/hyperium/h2/pull/812
> Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7
>
> ## Implementation Notes
>
> - Update h2 dependency to >= 0.4.8 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
> - The fix adds a configurable maximum header list size defaulting to 16 KiB
>
> ## Acceptance Criteria
>
> - [ ] h2 dependency is >= 0.4.8
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8004 (parent tracking issue)

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-33501 fix from the upstream backport task.
>
> The upstream backport bumps h2 to 0.4.8
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: upstream backport task (upstream backport must merge first)
> - Depends on: TC-8004 (parent tracking issue)

## Jira Operations (would be executed after engineer confirmation)

### 1. Create upstream backport task

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### 2. Create downstream propagation subtask

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### 3. Link tasks

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Downstream blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### 4. Transition and assign

```
# Transition TC-8004 to In Progress
jira.transition_issue("TC-8004", transition: "In Progress")

# Assign TC-8004 to current user
jira.edit_issue("TC-8004", fields={"assignee": {"accountId": "<current-user-id>"}})
```

### 5. Add ai-cve-triaged label

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 6. Post triage summary comment

> Triage complete for TC-8004 (CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames).
>
> **Version Impact:**
>
> | Version | h2 version | Affected? | Notes |
> |---------|------------|-----------|-------|
> | 2.1.0 | 0.4.5 | YES | |
> | 2.1.1 | 0.4.5 | YES | |
> | 2.2.0 | 0.4.8 | NO | at fix threshold |
> | 2.2.1 | 0.4.8 | NO | |
> | 2.2.2 | 0.4.8 | NO | retag of 2.2.1 |
> | 2.2.3 | 0.4.9 | NO | |
> | 2.2.4 | 0.4.9 | NO | |
>
> **Affects Versions corrected**: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
>
> **Outcome**: Remediation tasks created for stream 2.1.x:
> - <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
> - <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)
>
> Stream 2.2.x is not affected -- all versions ship h2 >= 0.4.8.
>
> @<reporter-name> (reporter)

## Why No Cross-Stream Impact Notice

The issue TC-8004 is **unscoped** -- it has no stream suffix in the summary. An unscoped issue covers all streams by definition. Cross-stream impact notices (Case B) are only generated for **scoped** issues where the analysis reveals impact on streams outside the issue's scope. Since an unscoped issue has no scope boundary, there is no "outside" to report on.

## Why No Remediation for 2.2.x

The version impact analysis confirms that all 2.2.x versions ship h2 >= 0.4.8 (the fix threshold). The earliest 2.2.x version (2.2.0, built from tag v0.4.5) already includes h2 0.4.8. Therefore, the 2.2.x stream does not require any remediation.
