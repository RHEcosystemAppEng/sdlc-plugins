# Step 3 -- Affects Versions Correction

## 3.1 -- Jira Version Discovery

**Proposed action** (requires engineer confirmation): Query `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type (ID: 10024) in project TC to discover available Jira versions filtered by prefix `RHTPA`.

## 3.2 -- Affects Versions Correction

Current PSIRT-assigned Affects Versions: `[RHTPA 2.0.0]`

The version impact table shows the following versions are affected within the scoped stream (2.2.x):
- RHTPA 2.2.0 (quinn-proto 0.11.9 -- affected)
- RHTPA 2.2.1 (quinn-proto 0.11.12 -- affected)
- RHTPA 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12 -- affected)

Versions RHTPA 2.2.3 and RHTPA 2.2.4 ship quinn-proto 0.11.14 and are NOT affected.

**PSIRT version is wrong**: RHTPA 2.0.0 does not correspond to any version in the supportability matrix.

**Proposed correction** (requires engineer confirmation):
```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. Versions from stream 2.1.x are excluded from this issue's Affects Versions -- they are tracked by companion issues (see Step 4).

**Proposed Jira mutation** (after engineer confirmation):
```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]
})
```
Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1), not hardcoded.

**Proposed comment** (after engineer confirmation):
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

Note: No ProdSec Jira account ID is configured in this CLAUDE.md, so no @mention is appended.

---

# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## 4.1-4.2 -- Sibling Search

**Proposed action**: Search for sibling Vulnerability issues with JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

No sibling issues are specified in this eval scenario. Proceeding to Step 4.3.

## 4.3 -- Cross-CVE Overlap Detection

**Skipped**: The Upstream Affected Component custom field is not configured in this CLAUDE.md's Security Configuration. Step 4.3 requires this field and is skipped entirely when not configured.

## 4.4 -- Preemptive Task Reconciliation

**Proposed action**: Search for preemptive tasks with JQL:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks are specified in this eval scenario. Proceeding to Step 5.

---

# Step 5 -- Version Lifecycle Check

**Proposed action**: Fetch product lifecycle page from https://access.example.com/product-life-cycle/rhtpa to verify affected versions (2.2.0, 2.2.1, 2.2.2) are within support lifecycle.

For this eval, assuming all affected versions are actively supported. Proceeding to Step 6.

---

# Step 6 -- Already Fixed Check

Reusing JQL results from Step 4: no resolved sibling issues found for the same CVE.
No already-fixed scenario detected. Proceeding to Step 7.

---

# Step 7 -- Concurrent Triage Detection

**Skipped**: The Upstream Affected Component custom field is not configured in this CLAUDE.md's Security Configuration. Step 7 requires this field and is skipped entirely when not configured.

---

# Step 8 -- Remediation

## Case Assessment

- **Stream 2.2.x** (scoped stream): Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected.
- **Stream 2.1.x** (other stream): Versions 2.1.0 and 2.1.1 are affected. This is a cross-stream impact.

**Case A applies**: The issue's scoped versions (2.2.x) include affected versions. Create remediation tasks for stream 2.2.x.

**Case B applies**: Stream 2.1.x is also affected and is outside this issue's scope. Post cross-stream impact comment and check for companion CVE Jiras.

## Case A -- Remediation Tasks for Stream 2.2.x

Since the ecosystem is **Cargo** (source dependency), two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task

**Proposed Jira creation** (requires engineer confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```markdown
## Repository

backend

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

#### Description Digest Protocol (Task 1)

After creating the upstream backport task:

1. **Re-fetch the description** from Jira API after `create_issue` completes:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   The digest is computed from the re-fetched description (as stored by Jira after normalization), NOT from the description string passed to `create_issue`.

2. **Write the description to a temp file** and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** BEFORE creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

### Task 2: Downstream Propagation Subtask

**Proposed Jira creation** (requires engineer confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```markdown
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

#### Description Digest Protocol (Task 2)

After creating the downstream propagation subtask:

1. **Re-fetch the description** from Jira API after `create_issue` completes:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** BEFORE creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Jira Linkage (after digest comments are posted)

**Proposed Jira mutations** (require engineer confirmation):

1. Link upstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Link downstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

4. Transition TC-8001 to In Progress.

5. Assign TC-8001 to the current user.

## Case B -- Cross-Stream Impact

The version impact analysis reveals that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9).

**Proposed cross-stream impact comment** on TC-8001 (requires engineer confirmation):
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

**Proposed action**: Search for existing CVE Jiras for stream 2.1.x:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

If no sibling CVE Jira exists for stream 2.1.x, create preemptive remediation tasks:

### Preemptive Upstream Backport Task (stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

The description includes the preemptive remediation prefix:
```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.
```

Linked to TC-8001 with "Related" (not "Depend") since the originating CVE belongs to a different stream.

### Preemptive Downstream Propagation Subtask (stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

Also linked to TC-8001 with "Related" link type.

**Proposed comment** on TC-8001 (after preemptive tasks are created):
```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

# Post-Triage Summary

## 1. Add `ai-cve-triaged` label

**Proposed action** (requires engineer confirmation):
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## 2. Post Summary Comment

**Proposed comment** on TC-8001 (requires engineer confirmation):

```
AI Triage Summary for CVE-2026-31812 (quinn-proto < 0.11.14):

Version Impact Table:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to stream 2.2.x per issue suffix)

Triage outcome: Remediation required (Case A + Case B)

Remediation tasks created:
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream preemptive tasks:
- <preemptive-upstream-task-key> (2.1.x, security-preemptive)
- <preemptive-downstream-task-key> (2.1.x, security-preemptive, downstream propagation)

@<reporter-name> (reporter @mention via ADF mention node with account ID from issue reporter field)
```

The @mention of the reporter uses an ADF mention node:
```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```

This summary comment MUST include the Comment Footnote (see below).

### Comment Footnote

All Jira comments posted by this skill include the following ADF footnote appended at the end:

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

Plugin version `0.11.1` is read from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.
