# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

The version impact analysis shows that the **2.1.x stream** is affected (h2 0.4.5 < 0.4.8) while the **2.2.x stream** is NOT affected (ships h2 >= 0.4.8). Since TC-8004 is unscoped, remediation tasks are created only for the actually affected stream (2.1.x).

No cross-stream impact notice is needed because this issue is **unscoped** -- it covers all streams by definition. Cross-stream notices (Case B) only apply to scoped issues where impact is found outside the issue's scope.

## Ecosystem: Cargo (source dependency)

For Cargo ecosystem, **two tasks** are required per affected stream:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update Konflux release repo reference, blocked by upstream task)

---

## Task 1: Upstream Backport (2.1.x stream)

### Proposed Jira Issue Creation

```
PROPOSAL: Create upstream backport task

jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- may require bumping
  hyper or adjusting dependency resolution
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x stream)

### Proposed Jira Issue Creation

```
PROPOSAL: Create downstream propagation subtask

jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Proposed Jira Linkage

```
PROPOSAL: Link remediation tasks to vulnerability issue

# 1. Link upstream task to vulnerability
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<upstream-task-key>",
  type: "Depend"
)

# 2. Link downstream task to vulnerability
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<downstream-task-key>",
  type: "Depend"
)

# 3. Downstream blocked by upstream
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

## Proposed Post-Triage Actions

```
PROPOSAL: Add ai-cve-triaged label to TC-8004

jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

```
PROPOSAL: Transition TC-8004 to In Progress

jira.transition_issue("TC-8004", transition_id=<in-progress-transition-id>)
```

```
PROPOSAL: Assign TC-8004 to current user

jira.edit_issue("TC-8004", fields={
  "assignee": {"accountId": "<current-user-id>"}
})
```

## Proposed Post-Triage Summary Comment

```
PROPOSAL: Add summary comment to TC-8004

## Triage Summary for CVE-2026-33501 (h2 < 0.4.8)

### Version Impact

| Version | Stream | h2 | Affected? | Notes |
|---------|--------|----|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

RHTPA 2.2.0 removed (not affected -- ships h2 0.4.8).
RHTPA 2.1.1 added (affected -- ships h2 0.4.5).

### Triage Outcome

Remediation required for stream 2.1.x only. Stream 2.2.x is not affected.

### Remediation Tasks

- <upstream-task-key>: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x) -- upstream backport
- <downstream-task-key>: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) -- downstream propagation, blocked by <upstream-task-key>

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.9.2.
```

## Notes

- **No cross-stream impact notice**: This issue is unscoped (covers all streams by definition), so no Case B cross-stream notice is needed. Cross-stream notices apply only to scoped issues where impact is discovered outside the issue's scope.
- **No remediation for 2.2.x**: The 2.2.x stream ships h2 >= 0.4.8 in all versions and is not affected. No tasks are created for this stream.
- **All Jira mutations are PROPOSALS**: Per the skill's Guardrails, every Jira mutation requires explicit engineer confirmation before execution. None of the above actions have been executed.
