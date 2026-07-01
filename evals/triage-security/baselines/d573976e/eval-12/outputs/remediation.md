# Step 3 -- Affects Versions Correction

## 3.1 -- Discover available Jira versions

(Would call `getJiraIssueTypeMetaWithFields` for project TC, issue type 10024 to discover available Jira versions dynamically. Filtering by prefix `RHTPA`.)

Based on the version impact table and supported versions, the expected Jira version registry matching "RHTPA" would include entries for RHTPA 2.1.0, RHTPA 2.1.1, RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4, and any unreleased development versions.

## 3.2 -- Compare and correct Affects Versions

Issue TC-8030 is **scoped** to stream **2.2.x** (suffix `[rhtpa-2.2]`).

Stream-scoped version impact for 2.2.x:
- RHTPA 2.2.0: h2 0.4.5 -- **YES** (affected)
- RHTPA 2.2.1: h2 0.4.8 -- NO (at fix threshold)
- RHTPA 2.2.2: retag of 2.2.1 -- NO
- RHTPA 2.2.3: h2 0.4.9 -- NO
- RHTPA 2.2.4: h2 0.4.9 -- NO

Only RHTPA 2.2.0 is affected within the scoped stream.

**Current Affects Versions**: [RHTPA 2.2.0]
**Proposed Affects Versions**: [RHTPA 2.2.0]

**Result**: Affects Versions are already correct. PSIRT assigned RHTPA 2.2.0, and lock file analysis confirms that only RHTPA 2.2.0 ships h2 0.4.5 (within the affected range < 0.4.8). No correction needed.

(Note: The 2.1.x versions are also affected but belong to the 2.1.x stream scope and are not included in this scoped issue's Affects Versions. Cross-stream impact is addressed in Step 8 Case B.)

---

# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

(Would search JQL: `project = TC AND labels = 'CVE-2026-48901' AND issuetype = 10024 AND key != TC-8030`)

No specific sibling data was provided in the eval fixtures. Assuming no siblings found, proceeding to Step 4.3.

### Step 4.3 -- Cross-CVE overlap detection

Upstream Affected Component custom field is not configured in Security Configuration. **Step 4.3 skipped entirely.**

### Step 4.4 -- Preemptive task reconciliation

(Would search JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-48901' ORDER BY created DESC`)

No preemptive task data provided in fixtures. Assuming no matching preemptive tasks found. Proceeding to Step 5.

---

# Step 5 -- Version Lifecycle Check

(Would fetch product lifecycle page from https://access.example.com/product-life-cycle/rhtpa)

No lifecycle data provided in fixtures. Assuming all affected versions (2.2.0, 2.1.0, 2.1.1) are within support lifecycle. Proceeding to Step 6.

---

# Step 6 -- Already Fixed Check

No resolved sibling issues found. Proceeding to Step 7.

---

# Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is not configured in Security Configuration. **Step 7 skipped entirely.**

---

# Step 8 -- Remediation

## Triage Decision

Version impact summary for scoped stream (2.2.x):
- **RHTPA 2.2.0**: AFFECTED (h2 0.4.5, within range < 0.4.8)
- **RHTPA 2.2.1 through 2.2.4**: NOT AFFECTED (h2 >= 0.4.8)

Cross-stream impact for stream 2.1.x:
- **RHTPA 2.1.0**: AFFECTED (h2 0.4.5)
- **RHTPA 2.1.1**: AFFECTED (h2 0.4.5)

### Case A: Affected -- create remediation tasks (stream 2.2.x)

The scoped stream (2.2.x) has affected version 2.2.0. Remediation tasks are needed.

Since the ecosystem is **Cargo** (source dependency), **two tasks** are created:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in the Konflux release repo)

### Case B: Cross-stream impact -- proactive remediation (stream 2.1.x)

Stream 2.1.x is also affected but is outside this issue's scope. Search for sibling CVE Jiras with label CVE-2026-48901 and stream suffix matching 2.1.x. If no sibling CVE Jira exists for stream 2.1.x, create preemptive remediation tasks with the `security-preemptive` label.

---

## Remediation Task Descriptions

### Task 1: Upstream Backport Task (stream 2.2.x)

**Proposed Jira creation**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

**Task description**:

---

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.2.0 (tag v0.4.5, h2 0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask (stream 2.2.x)

**Proposed Jira creation**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

**Task description**:

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

## Description Digest Protocol

After creating each remediation task, the following digest procedure would be performed:

### For the upstream backport task:
1. Re-fetch the task description from Jira API after `create_issue`: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest using `scripts/sha256-digest.py`: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment **before** creating issue links or other comments:
   `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
   Where `<tagged-digest>` is the full output from the script (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)

### For the downstream propagation subtask:
1. Re-fetch the task description from Jira API after `create_issue`: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest using `scripts/sha256-digest.py`: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment **before** creating issue links or other comments:
   `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`

**Important**: The digest is computed from the re-fetched description (via Jira API after create_issue), NOT from the description string passed to create_issue. This is because Jira normalizes content during storage.

## Jira Linkage (proposed)

After creating remediation tasks and posting digest comments:

1. Link upstream backport task to CVE Jira:
   ```
   jira.create_link(inwardIssue: "TC-8030", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Transition TC-8030 to In Progress (if not already).

4. Assign TC-8030 to the current user.

5. Add comment to TC-8030:
   ```
   Remediation tasks created: <upstream-task-key> (upstream backport),
   <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   ```

---

## Cross-Stream Impact (Case B) -- Stream 2.1.x

Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
Both RHTPA 2.1.0 and RHTPA 2.1.1 ship h2 0.4.5, which is within the affected range.

**Proposed cross-stream comment on TC-8030**:
```
Cross-stream impact: h2 < 0.4.8 also affects stream(s) 2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no sibling CVE Jira exists for stream 2.1.x, create **preemptive remediation tasks**:

### Preemptive Upstream Backport Task (stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

The preemptive task description would include the standard upstream backport template with a preemptive remediation prefix:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Target Branch: release/0.3.z (from 2.1.x stream Ecosystem Mappings)

Link type: **Related** (not Depend) to the originating CVE Jira TC-8030.

### Preemptive Downstream Propagation Subtask (stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

Link type: **Related** to the originating CVE Jira TC-8030.

**Proposed preemptive task comment on TC-8030**:
```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

### 1. Add the `ai-cve-triaged` label

**Proposed**: Add the `ai-cve-triaged` label to TC-8030 to mark it as triaged.

### 2. Post summary comment

**Proposed summary comment on TC-8030**:

```
Triage summary for CVE-2026-48901 (h2 < 0.4.8):

Version Impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

Fix threshold: 0.4.8 (enriched from MITRE CVE API and OSV.dev -- Jira description was imprecise)

Affects Versions: Already correct [RHTPA 2.2.0] -- no correction needed.

Triage outcome: Remediation created.
- <upstream-task-key>: upstream backport (bump h2 to >= 0.4.8 on release/0.4.z)
- <downstream-task-key>: downstream propagation (update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream: Stream 2.1.x also affected. Preemptive remediation tasks created (security-preemptive label).
```

The summary comment would include:
- An @mention of the vulnerability issue's reporter using an ADF mention node:
  ```json
  { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
  ```
- The Comment Footnote at the end (horizontal rule followed by the AI-generated attribution):
  ```
  ---
  This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
  ```

All proposed actions above require explicit engineer confirmation before execution. No Jira mutations have been performed.
