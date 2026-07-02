# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A** (Affected): Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2). Create remediation tasks for this stream.
- **Case B** (Cross-stream impact): Stream 2.1.x is also affected (all versions: 2.1.0, 2.1.1). No existing CVE Jira for 2.1.x stream. Create preemptive remediation tasks for 2.1.x.

Ecosystem: Cargo (source dependency) -- two tasks per stream (upstream backport + downstream propagation).

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task (2.2.x)

**Jira Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
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

**Description Digest Comment (posted immediately after task creation, before links or other comments):**

1. Re-fetch the created task description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temp file:
   ```
   # Write fetched description to /tmp/task-desc.md
   ```
3. Compute the digest using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by the Jira API.
4. Post the digest as a standalone comment on the upstream task:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64chars`).

**Jira Linkage:**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
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

**Description Digest Comment (posted immediately after task creation, before links or other comments):**

1. Re-fetch the created task description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temp file:
   ```
   # Write fetched description to /tmp/task-desc.md
   ```
3. Compute the digest using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by the Jira API.
4. Post the digest as a standalone comment on the downstream task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64chars`).

**Jira Linkage:**

```
# Link downstream to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Preemptive Remediation Tasks for Stream 2.1.x

Cross-stream impact detected: stream 2.1.x (all versions 2.1.0, 2.1.1) ships quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. No existing CVE Jira found for stream 2.1.x (no sibling issue with CVE-2026-31812 label and `[rhtpa-2.1]` suffix).

**Cross-stream impact comment on TC-8001:**

```
Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Task 3: Upstream Backport Task -- Preemptive (2.1.x)

**Jira Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
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

**Description Digest Comment (posted immediately after task creation, before links or other comments):**

1. Re-fetch the created task description from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temp file:
   ```
   # Write fetched description to /tmp/task-desc.md
   ```
3. Compute the digest using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by the Jira API.
4. Post the digest as a standalone comment on the preemptive upstream task:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64chars`).

**Jira Linkage (preemptive -- uses "Related" not "Depend"):**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

---

### Task 4: Downstream Propagation Subtask -- Preemptive (2.1.x)

**Jira Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Description Digest Comment (posted immediately after task creation, before links or other comments):**

1. Re-fetch the created task description from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temp file:
   ```
   # Write fetched description to /tmp/task-desc.md
   ```
3. Compute the digest using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by the Jira API.
4. Post the digest as a standalone comment on the preemptive downstream task:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64chars`).

**Jira Linkage (preemptive -- uses "Related" not "Depend"):**

```
# Link preemptive downstream to originating CVE Jira
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive downstream as blocked by preemptive upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, post this comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (security-preemptive, upstream backport),
         <preemptive-downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Actions

### 1. Add ai-cve-triaged Label

```
jira.edit_issue("TC-8001", labels: [...existing-labels, "ai-cve-triaged"])
```

### 2. Post Summary Comment on TC-8001

The summary comment documents:

1. **Version impact table** (from Step 2 -- both 2.2.x and 2.1.x streams)
2. **Affects Versions correction**: Removed RHTPA 2.0.0; added RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Triage outcome**: Remediation tasks created for 2.2.x (Case A); preemptive tasks created for 2.1.x (Case B)
4. **Remediation task links**:
   - 2.2.x: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - 2.1.x (preemptive): <preemptive-upstream-task-key> (upstream backport), <preemptive-downstream-task-key> (downstream propagation)
5. **@mention of reporter**: ADF mention node with the reporter's account ID from the original TC-8001 issue data

### 3. Comment Footnote

Every Jira comment posted by this skill (summary comment, cross-stream impact comment, preemptive tasks comment, Affects Versions correction comment) MUST end with the comment footnote. The footnote uses ADF contentFormat:

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
      "text": " v0.12.0."
    }
  ]
}
```

These two ADF nodes are appended at the end of the ADF document's `content` array for every comment.

---

## Description Digest Protocol Summary

For each of the 4 remediation tasks created, the following description digest protocol steps are performed **immediately after task creation and before creating issue links or other comments**:

1. **Re-fetch** the task description from the Jira API (do NOT hash the description string passed to `create_issue` -- Jira normalizes content during storage)
2. **Write** the fetched description to a temporary file (e.g., `/tmp/task-desc.md`)
3. **Compute** the digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   - If the API returned markdown text: outputs `sha256-md:<64-char-hex-digest>`
   - If the API returned ADF JSON: outputs `sha256-adf:<64-char-hex-digest>`
4. **Post** a standalone comment on the task with exactly this format:
   ```
   [sdlc-workflow] Description digest: <tagged-digest>
   ```
   Where `<tagged-digest>` is the full output from step 3 (including the format tag).

Rules:
- The digest comment is a standalone comment, not appended to any other comment
- The digest comment is posted BEFORE creating issue links or other comments on the task
- The digest value must be the full 64-character hex digest (no abbreviation)
- The format tag (`sha256-md:` or `sha256-adf:`) must not be stripped
- No placeholder or example hashes -- always freshly computed from the actual description
- No extra text after the hash on the marker line
