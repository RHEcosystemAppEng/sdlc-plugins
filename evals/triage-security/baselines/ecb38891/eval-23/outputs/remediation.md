# Step 8 -- Remediation

## Version Impact Summary

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Cross-stream impact: 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Case A cross-stream notice would be posted since this is a scoped issue.

## Case B: Affected -- Create Remediation Tasks

Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the 2.2.x stream. Remediation tasks are created for this stream.

Ecosystem: Cargo (source dependency) -- two tasks per stream.

---

## Task 1: Upstream Backport Task

**Proposed Jira create_issue:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.8, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

### Post-creation steps for upstream task

1. **Description digest**: After `create_issue` returns the new task key, re-fetch the task description from Jira via `jira.get_issue(<upstream-task-key>, fields=["description"])`. Write the description to a temp file and compute the digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Post a digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`. This digest comment MUST be posted BEFORE creating issue links or other comments.

2. **Link to vulnerability issue**: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")`

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira create_issue:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
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

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

### Post-creation steps for downstream task

1. **Description digest**: After `create_issue` returns the new task key, re-fetch the task description from Jira via `jira.get_issue(<downstream-task-key>, fields=["description"])`. Write the description to a temp file and compute the digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Post a digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`. This digest comment MUST be posted BEFORE creating issue links or other comments.

2. **Link to vulnerability issue**: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`

3. **Block downstream by upstream**: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Linkage Summary

After both tasks are created:

1. Upstream task linked to TC-8001 via "Depend"
2. Downstream task linked to TC-8001 via "Depend"
3. Downstream task linked to upstream task via "Blocks" (downstream blocked by upstream)
4. Transition TC-8001 to In Progress (if not already)
5. Add `ai-cve-triaged` label to TC-8001

## Post-Triage Summary Comment

A summary comment would be posted to TC-8001 documenting:

1. The version impact table (2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected)
2. The Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
3. The triage outcome (remediation tasks created)
4. Links to upstream backport task and downstream propagation subtask
5. @mention of the vulnerability issue's reporter using an ADF mention node

The comment MUST include the Comment Footnote:

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7.
