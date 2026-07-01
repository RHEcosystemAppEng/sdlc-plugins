# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. The issue is scoped to stream **2.2.x**, but per Important Rule 4, all versions across all streams are checked.

## 2.3 -- Dependency Version Extraction

Using the mock lock file data for quinn-proto at each pinned commit tag:

| Version | Stream | Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

For 2.2.x: the upstream branch already ships the fix at HEAD (0.11.14). Remediation is a downstream propagation to update the source pinning reference.

---

# Step 3 -- Affects Versions Correction

The issue is scoped to stream **2.2.x**. Only 2.2.x versions are included in the Affects Versions correction.

Affected versions within scope (2.2.x stream): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Proposed correction:**

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

PSIRT assigned `RHTPA 2.0.0` which does not exist in the supportability matrix. The lock file analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are affected. Versions 2.2.3 and 2.2.4 ship 0.11.14 (the fixed version) and are not affected.

**Proposed Jira action (requires engineer confirmation):**
```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]
})
```

**Proposed comment:**
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

(ProdSec @mention not configured -- omitted silently.)

---

# Step 4 -- Duplicate, Sibling, and Overlap Check

**Proposed JQL:**
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

For this eval, assume no sibling issues are found. Proceeding to Step 4.3.

### Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in Security Configuration. **Skipping Step 4.3 entirely.**

### Step 4.4 -- Preemptive Task Reconciliation

**Proposed JQL:**
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

For this eval, assume no preemptive tasks are found. Proceeding to Step 5.

---

# Step 5 -- Version Lifecycle Check

**Proposed action:** Fetch product lifecycle page at https://access.example.com/product-life-cycle/rhtpa. (Skipped for eval -- no external tools called. Assuming all affected versions are within support lifecycle.)

---

# Step 6 -- Already Fixed Check

No resolved sibling issues exist (from Step 4). Proceeding to Step 7.

---

# Step 7 -- Concurrent Triage Detection

The Upstream Affected Component custom field is not configured in Security Configuration. **Skipping Step 7 entirely.**

---

# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected

The version impact table shows that 2.2.x stream versions 2.2.0, 2.2.1, and 2.2.2 are affected (ship quinn-proto < 0.11.14). The ecosystem is **Cargo** (source dependency), so **two tasks** are created: an upstream backport task and a downstream propagation subtask.

## Cross-Stream Impact (Case B Check)

The version impact table also shows that stream 2.1.x (versions 2.1.0 and 2.1.1) is affected. However, this issue is scoped to stream 2.2.x. A cross-stream impact comment would be posted:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

Since no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created per Case B. (The preemptive task details are not the focus of this eval but would follow the preemptive variant template with `security-preemptive` label and `Related` link type.)

---

## Remediation Task 1: Upstream Backport Task (2.2.x stream)

**Proposed Jira creation (requires engineer confirmation):**

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

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

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

Note: The **Coordination Guidance** subsection is intentionally **omitted** from Implementation Notes. The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Per the remediation-templates.md backward compatibility rule: "When the Deployment Context column is absent from the Source Repositories table (backward compatibility), omit the coordination guidance entirely -- do not add the subsection."

### Description Digest (planned procedure)

After creating the upstream task:
1. Re-fetch the task description from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`

The digest comment is posted **before** creating issue links or other comments.

---

## Remediation Task 2: Downstream Propagation Subtask (2.2.x stream)

**Proposed Jira creation (requires engineer confirmation):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

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
```

Note: The **Coordination Guidance** subsection is intentionally **omitted** from Implementation Notes for the same backward compatibility reason -- the Deployment Context column is absent from the Source Repositories table.

### Description Digest (planned procedure)

After creating the downstream task:
1. Re-fetch the task description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`

The digest comment is posted **before** creating issue links or other comments.

---

## Jira Linkage (proposed actions, require engineer confirmation)

1. Link upstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Link downstream subtask to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

4. Transition TC-8001 to In Progress.

5. Assign TC-8001 to current user.

---

## Post-Triage Summary

### 1. Add the `ai-cve-triaged` label

**Proposed:**
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8001

**Proposed comment:**

```
Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14):

Version Impact:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        |       |
| 2.2.4   | 0.11.14     | NO        |       |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to stream 2.2.x per issue suffix)

Triage outcome: Remediation tasks created.

Remediation tasks:
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: stream 2.1.x also affected (quinn-proto 0.11.9). Companion CVE Jira
or preemptive tasks track remediation for that stream.

@<reporter-name> (ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}})
```

The summary comment includes the Comment Footnote:

```json
{
  "type": "rule"
},
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "This comment was AI-generated by "},
    {"type": "text", "text": "sdlc-workflow/triage-security", "marks": [{"type": "link", "attrs": {"href": "https://github.com/mrizzi/sdlc-plugins"}}]},
    {"type": "text", "text": " v0.11.1."}
  ]
}
```

---

## Backward Compatibility Summary

The following aspects confirm backward compatibility when the Deployment Context column is absent:

1. **Step 0**: The Source Repositories table has columns `Repository | URL | Local Path` with no Deployment Context column. All repositories default to `upstream` internally.
2. **Step 1**: Deployment context lookup records `upstream` as the default, but since the column was absent (not just empty), this is a backward-compatibility scenario.
3. **Step 8 remediation tasks**: Neither the upstream backport task nor the downstream propagation subtask includes a `### Coordination Guidance` subsection in Implementation Notes. The subsection is omitted entirely -- not populated with the `upstream` template text.
4. **All other steps**: Proceed normally without errors. The absence of the Deployment Context column does not affect version impact analysis, Affects Versions correction, duplicate detection, lifecycle checks, or any other triage step.
