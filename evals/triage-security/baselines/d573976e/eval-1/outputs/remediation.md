# Step 8 -- Remediation

## Triage Decision: Case A -- Affected

The issue is scoped to stream 2.2.x. Within this stream, versions 2.2.0, 2.2.1,
and 2.2.2 are affected (ship quinn-proto < 0.11.14). Remediation tasks are needed.

### Cross-stream impact (Case B check)

The version impact table also shows that stream 2.1.x is affected:
- 2.1.0 (quinn-proto 0.11.9) -- affected
- 2.1.1 (quinn-proto 0.11.9) -- affected

Since this issue is scoped to 2.2.x, the 2.1.x impact would be reported via
a cross-stream impact comment on TC-8001. In a real triage, the skill would:

1. Search for sibling CVE Jiras for stream 2.1.x with label CVE-2026-31812
2. If a sibling exists for 2.1.x, link as "Related" and skip preemptive tasks
3. If no sibling exists for 2.1.x, create preemptive remediation tasks with
   the `security-preemptive` label

**Proposed cross-stream comment** (on TC-8001):
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. These streams are tracked by companion issues (see Related
links) or may require separate PSIRT triage.
```

For this eval, remediation tasks are created for the **2.2.x stream only** (Case A).

---

## Ecosystem: Cargo (Source Dependency)

Since quinn-proto is a Cargo (Rust) source dependency, remediation creates **two tasks**:
1. Upstream backport task -- fix in the source repo (rhtpa-backend)
2. Downstream propagation subtask -- update the reference in the Konflux release repo

The downstream subtask is blocked by the upstream task.

---

## Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of v0.4.8)
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

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

Note: Source Repositories table has no Deployment Context column. Coordination
Guidance subsection is omitted (backward compatibility).

---

## Task 2: Downstream Propagation Subtask

### Proposed Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
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

---

## Jira Linkage (Proposed Actions)

After creating both tasks, the following Jira mutations are proposed (each
requires engineer confirmation):

### 1. Link upstream task to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### 2. Link downstream subtask as blocked by upstream task

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### 3. Link downstream subtask to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

### 4. Transition TC-8001 to In Progress

```
jira.transition_issue("TC-8001", status: "In Progress")
```

### 5. Assign TC-8001 to current user

```
jira.edit_issue("TC-8001", fields={ "assignee": { "accountId": "<current-user-id>" } })
```

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label

**Proposed action**: Add the `ai-cve-triaged` label to TC-8001:
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment

**Proposed comment** on TC-8001:

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

**Version Impact Table:**

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | (cross-stream) |
| 2.1.1 | 2.1.x | 0.11.9 | YES | (cross-stream) |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

**Affects Versions Correction:**
[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

**Triage Outcome:**
Remediation tasks created:
- <upstream-task-key> (upstream backport: bump quinn-proto to >= 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: stream 2.1.x is also affected (quinn-proto 0.11.9 < 0.11.14).

@<reporter-name> (reporter @mention via ADF mention node: { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } })

---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```

The reporter @mention uses the reporter's Jira account ID from the issue data
extracted in Step 1, formatted as an ADF mention node in the actual Jira comment.

---

## Description Digest Protocol

After creating each remediation task, the following digest protocol steps would
be performed (before creating issue links or other comments):

### For upstream backport task:

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   (The script auto-detects the format and outputs `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
3. Post a digest comment on the upstream task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### For downstream propagation subtask:

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post a digest comment on the downstream task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

**Important**: The digest is computed from the re-fetched description (via Jira
API after `create_issue`), not from the description string passed to `create_issue`.
Jira normalizes content during storage, so the stored description may differ from
the input. Digest comments are posted BEFORE issue links (Depend, Blocks) or
other comments to comply with the protocol's sequencing requirement.
