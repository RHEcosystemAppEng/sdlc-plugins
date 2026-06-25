# Step 7 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome

The issue is scoped to the **2.2.x** stream. Within that scope, versions 2.2.0,
2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.

Cross-stream analysis reveals the **2.1.x** stream is also affected (all versions
ship quinn-proto 0.11.9). Since no stream-specific CVE Jira exists for 2.1.x,
proactive (preemptive) remediation tasks are created under Case B.

The ecosystem is **Cargo** (source dependency), so each stream requires **two tasks**:
an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for 2.2.x Stream (Issue Scope)

### Task 1: Upstream Backport Task (2.2.x)

#### 1. Create the upstream backport task

```
upstream_task_22 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description content:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- quinn-proto is a transitive dependency via: reqwest [http3] -> h3 -> quinn -> quinn-proto
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

#### 1a. Description Digest Comment for Upstream Backport Task (2.2.x)

Immediately after `create_issue`, the following steps are performed BEFORE creating
any issue links or other comments:

**Step 1 -- Re-fetch the created task description from Jira:**

```
upstream_desc_22 = jira.get_issue(<upstream_task_22_key>, fields=["description"])
```

This re-fetches the description as stored by Jira (which may have been normalized
during storage), rather than using the description string originally passed to
`create_issue`.

**Step 2 -- Write description to temp file and compute SHA-256 digest:**

```bash
# Write the re-fetched description to a temp file
echo "<re-fetched-description-content>" > /tmp/task-desc.md

# Compute the digest using the project script
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (if description returned as markdown)
# or:     sha256-adf:<64-char-hex-digest> (if description returned as ADF JSON)
```

The script auto-detects the format (ADF JSON vs markdown) and produces the
appropriate format-tagged digest.

**Step 3 -- Post the digest comment to the upstream task:**

```
jira.add_comment(<upstream_task_22_key>,
  "[sdlc-workflow] Description digest: <tagged-digest>"
)
```

Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`, e.g.,
`sha256-md:a3f7...` (64 hex chars). The comment is posted as ADF format:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
        }
      ]
    }
  ]
}
```

**Step 4 -- ONLY AFTER the digest comment is posted, create the issue link:**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream_task_22_key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

#### 2. Create the downstream propagation task

```
downstream_task_22 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description content:**

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream_task_22_key>.

The upstream backport (<upstream_task_22_key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream_task_22_key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### 2a. Description Digest Comment for Downstream Propagation Task (2.2.x)

Immediately after `create_issue`, the following steps are performed BEFORE creating
any issue links or other comments:

**Step 1 -- Re-fetch the created task description from Jira:**

```
downstream_desc_22 = jira.get_issue(<downstream_task_22_key>, fields=["description"])
```

**Step 2 -- Write description to temp file and compute SHA-256 digest:**

```bash
echo "<re-fetched-description-content>" > /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
```

**Step 3 -- Post the digest comment to the downstream task:**

```
jira.add_comment(<downstream_task_22_key>,
  "[sdlc-workflow] Description digest: <tagged-digest>"
)
```

**Step 4 -- ONLY AFTER the digest comment is posted, create the issue links:**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream_task_22_key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: <upstream_task_22_key>,
  outwardIssue: <downstream_task_22_key>,
  type: "Blocks"
)
```

---

## Case B: Preemptive Remediation Tasks for 2.1.x Stream (Cross-Stream Impact)

Cross-stream impact analysis reveals all 2.1.x versions (2.1.0, 2.1.1) ship
quinn-proto 0.11.9, which is within the affected range. No stream-specific CVE
Jira exists for the 2.1.x stream, so preemptive remediation tasks are created.

### Task 3: Upstream Backport Task (2.1.x -- Preemptive)

#### 3. Create the preemptive upstream backport task

```
upstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description content:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- quinn-proto is a transitive dependency via: reqwest [http3] -> h3 -> quinn -> quinn-proto
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

#### 3a. Description Digest Comment for Preemptive Upstream Backport Task (2.1.x)

Immediately after `create_issue`, the following steps are performed BEFORE creating
any issue links or other comments:

**Step 1 -- Re-fetch the created task description from Jira:**

```
upstream_desc_21 = jira.get_issue(<upstream_task_21_key>, fields=["description"])
```

This re-fetches the description as Jira stored it (post-normalization), NOT the
description string that was passed to `create_issue`.

**Step 2 -- Write description to temp file and compute SHA-256 digest:**

```bash
echo "<re-fetched-description-content>" > /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
```

**Step 3 -- Post the digest comment to the preemptive upstream task:**

```
jira.add_comment(<upstream_task_21_key>,
  "[sdlc-workflow] Description digest: <tagged-digest>"
)
```

**Step 4 -- ONLY AFTER the digest comment is posted, create the issue link:**

Preemptive tasks use "Related" link type (not "Depend"), since the originating
CVE Jira belongs to a different stream:

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream_task_21_key>,
  type: "Related"
)
```

---

### Task 4: Downstream Propagation Subtask (2.1.x -- Preemptive)

#### 4. Create the preemptive downstream propagation task

```
downstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description content:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream_task_21_key>.

The upstream backport (<upstream_task_21_key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
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

- Depends on: <upstream_task_21_key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### 4a. Description Digest Comment for Preemptive Downstream Propagation Task (2.1.x)

Immediately after `create_issue`, the following steps are performed BEFORE creating
any issue links or other comments:

**Step 1 -- Re-fetch the created task description from Jira:**

```
downstream_desc_21 = jira.get_issue(<downstream_task_21_key>, fields=["description"])
```

**Step 2 -- Write description to temp file and compute SHA-256 digest:**

```bash
echo "<re-fetched-description-content>" > /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
```

**Step 3 -- Post the digest comment to the preemptive downstream task:**

```
jira.add_comment(<downstream_task_21_key>,
  "[sdlc-workflow] Description digest: <tagged-digest>"
)
```

**Step 4 -- ONLY AFTER the digest comment is posted, create the issue links:**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream_task_21_key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: <upstream_task_21_key>,
  outwardIssue: <downstream_task_21_key>,
  type: "Blocks"
)
```

---

## Complete Sequence Summary

For every remediation task created, the full sequence is:

```
1. jira.create_issue(...)         -- Create the remediation task
2. jira.get_issue(<new-key>)      -- Re-fetch to get Jira-normalized description
3. python3 scripts/sha256-digest.py  -- Compute SHA-256 digest from re-fetched description
4. jira.add_comment(<new-key>,    -- Post digest comment with marker
     "[sdlc-workflow] Description digest: <tagged-digest>")
5. jira.create_link(...)          -- ONLY NOW create issue links (Depend/Blocks/Related)
```

The digest comment MUST come before any issue links or other comments. The digest
is computed from the re-fetched description (step 2), not the description originally
passed to create_issue (step 1), because Jira may normalize content during storage.

### Tasks Created

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

### Blocking Relationships

- Downstream propagation (2.2.x) is **Blocked by** Upstream backport (2.2.x)
- Downstream propagation (2.1.x) is **Blocked by** Upstream backport (2.1.x)

### Description Digest Comments Posted

Every task received a description digest comment with the marker
`[sdlc-workflow] Description digest:` immediately after creation and before
any issue links were created. Each digest was computed by:

1. Re-fetching the task description via `jira.get_issue`
2. Writing it to a temp file
3. Running `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Posting the format-tagged output (e.g., `sha256-md:<64-char-hex>`) as a comment
