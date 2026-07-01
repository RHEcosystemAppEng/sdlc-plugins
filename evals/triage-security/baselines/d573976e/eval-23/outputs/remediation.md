# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.8 | -- | YES | retag of 2.2.1 (same source commit v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Note: Triage is scoped to stream 2.2.x per the issue suffix `[rhtpa-2.2]`. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected (quinn-proto 0.11.9 at both v0.3.8 and v0.3.12), but are tracked by a separate stream-scoped CVE Jira or handled via cross-stream impact (Case B).

### Cross-stream impact (2.1.x)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

### Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)
  Lock file: Cargo.lock

  Present in: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag), 2.2.3 (v0.4.11), 2.2.4 (v0.4.12)
  Affected versions: 2.2.0, 2.2.1, 2.2.2 (quinn-proto < 0.11.14)
  Fixed versions: 2.2.3, 2.2.4 (quinn-proto = 0.11.14)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

The upstream branch `release/0.4.z` already contains the fix (quinn-proto 0.11.14). Remediation is a Konflux release repo change: bump the source tag/commit reference to pick up the fix.

---

# Step 3 -- Affects Versions Correction

The issue is scoped to stream 2.2.x. Only versions from the 2.2.x stream are included in the correction.

**Current (PSIRT-assigned)**: `[RHTPA 2.0.0]`
**Proposed (lock-file-verified)**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

PSIRT assigned `RHTPA 2.0.0`, which does not exist as a valid version in the 2.2.x stream. The lock file analysis confirms versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (the affected range). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.

**Proposed Jira mutation** (requires engineer confirmation):
```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```
Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`, not hardcoded.

**Proposed Affects Versions correction comment**:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

Note: ProdSec Jira account ID is not configured in this project -- @mention omitted silently.

---

# Steps 4-6 -- Jira Triage Operations

(Assuming no sibling issues found via JQL, no preemptive tasks found, lifecycle check passes, no already-fixed scenarios.)

---

# Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is not configured in Security Configuration. Step 7 is skipped entirely.

---

# Step 8 -- Remediation

## Case A: Affected -- create remediation tasks

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected. Since the ecosystem is **Cargo** (a source dependency ecosystem), two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task

**Proposed Jira creation** (requires engineer confirmation):

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.8 retag)
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

This component is shipped to customers. Coordinate fix with Product
Security for CVE assignment, advisory preparation, and formal disclosure.
Fix must be released via a security advisory with explicit CVE-to-component
mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation steps (planned procedure):**

1. **Description digest comment**: After creating the upstream task, re-fetch the task description from the Jira API:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   Write the re-fetched description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Post the digest comment (before creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The digest is computed from the re-fetched description (after Jira normalizes the content), not from the description string passed to `create_issue`.

2. **Link to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira creation** (requires engineer confirmation):

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate fix with Product
Security for CVE assignment, advisory preparation, and formal disclosure.
Fix must be released via a security advisory with explicit CVE-to-component
mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation steps (planned procedure):**

1. **Description digest comment**: After creating the downstream task, re-fetch the task description from the Jira API:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   Write the re-fetched description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Post the digest comment (before creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The digest is computed from the re-fetched description (after Jira normalizes the content), not from the description string passed to `create_issue`.

2. **Link to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Block by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Case B: Cross-Stream Impact

The version impact analysis reveals that stream **2.1.x** is also affected:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- affected
- 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- affected

**Proposed cross-stream impact comment** on TC-8001:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with the `security-preemptive` label and `Related` link to TC-8001 (see remediation-templates.md Preemptive Task Variant).

---

## Jira Linkage Summary

After creating remediation tasks (with engineer confirmation):

1. Link upstream task to TC-8001 with "Depend"
2. Link downstream task to TC-8001 with "Depend"
3. Link downstream task as blocked by upstream task with "Blocks"
4. Transition TC-8001 to In Progress
5. Assign TC-8001 to current user
6. Add `ai-cve-triaged` label to TC-8001

---

## Post-Triage Summary Comment

**Proposed comment** on TC-8001 (requires engineer confirmation):

```
Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14):

Version Impact (2.2.x stream):
| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        |       |
| 2.2.4   | 0.11.14     | NO        |       |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Triage outcome: Remediation tasks created (Case A -- affected versions in 2.2.x stream).
- <upstream-task-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key>: downstream propagation (update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (see Case B above).

@<reporter-name> (account ID from issue reporter field)
```

The @mention of the reporter uses an ADF mention node:
```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```

The comment includes the Comment Footnote (sdlc-workflow/triage-security v0.11.1):
```json
{
  "type": "rule"
},
{
  "type": "paragraph",
  "content": [
    {
      "type": "text",
      "text": "This comment was AI-generated by "
    },
    {
      "type": "text",
      "text": "sdlc-workflow/triage-security",
      "marks": [
        {
          "type": "link",
          "attrs": {
            "href": "https://github.com/mrizzi/sdlc-plugins"
          }
        }
      ]
    },
    {
      "type": "text",
      "text": " v0.11.1."
    }
  ]
}
```
