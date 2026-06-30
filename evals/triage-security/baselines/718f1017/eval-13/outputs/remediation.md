# Step 7 - Remediation for TC-8001

## Triage Outcome

The version impact analysis shows:
- **In-scope stream (2.2.x)**: versions 2.2.0, 2.2.1, 2.2.2 are affected -> **Case A: Create remediation tasks**
- **Cross-stream (2.1.x)**: versions 2.1.0, 2.1.1 are also affected -> **Case B: Cross-stream impact**

The ecosystem is **Cargo** (source dependency), so each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: In-scope remediation tasks (stream 2.2.x)

### Task 1: Upstream backport task (2.2.x)

**Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
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

#### Description Digest Comment for Task 1

After creating this task, the following steps are performed to post the description digest comment:

1. **Re-fetch the description** from Jira API after creation (since Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest using the sha256-digest.py script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. **Post the digest as a standalone comment** on the newly created task, using the exact marker prefix `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a3b1c9f0e2d4...` -- exactly 64 hex characters after the tag prefix).

   The comment is posted in ADF format:
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **This digest comment is posted BEFORE creating issue links or other comments** on the task, per the description digest protocol rules.

5. **The digest comment is a standalone comment** -- it is NOT embedded in other comments, NOT appended to the plan summary, and NOT combined with the comment footnote.

---

### Task 2: Downstream propagation subtask (2.2.x)

**Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
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

#### Description Digest Comment for Task 2

After creating this downstream propagation task, the following steps are performed to post the description digest comment:

1. **Re-fetch the description** from Jira API after creation:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects format and outputs a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest as a standalone comment** on the downstream task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Posted in ADF format:
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **This digest comment is posted BEFORE creating issue links or other comments** on the task.

5. **The digest comment is a standalone comment** -- not embedded in other comments.

---

### Jira Linkage (2.2.x tasks)

After creating both tasks and posting their description digest comments:

1. **Link upstream task to Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream task to Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream subtask as blocked by upstream task:**
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition** TC-8001 to In Progress.

5. **Assign** TC-8001 to current user.

6. **Add comment** to TC-8001:
   ```
   Remediation tasks created: <upstream-task-key> (upstream backport),
   <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   ```
   Comment includes the Comment Footnote (see below).

---

## Case B: Cross-stream impact (stream 2.1.x)

The version impact analysis shows that stream 2.1.x (versions 2.1.0, 2.1.1) is also affected by CVE-2026-31812 (quinn-proto 0.11.9 < 0.11.14). This stream is outside the current issue's scope (issue is scoped to 2.2.x via `[rhtpa-2.2]`).

### Step 1: Post cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

Comment includes the Comment Footnote.

### Step 2: Check for existing CVE Jiras for 2.1.x stream

Search for sibling Vulnerability issues with the same CVE label and stream suffix `[rhtpa-2.1]`:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001"
)
```

Parse each sibling's summary for a stream suffix matching 2.1.x.

### Step 3: If no sibling CVE Jira exists for 2.1.x -- create preemptive remediation tasks

#### Preemptive Task 1: Upstream backport (2.1.x, preemptive)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
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

##### Description Digest Comment for Preemptive Task 1

After creating this preemptive upstream task, the following steps are performed:

1. **Re-fetch the description** from Jira API after creation:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects format and outputs a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest as a standalone comment** on the preemptive task:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Posted in ADF format:
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **This digest comment is posted BEFORE creating issue links or other comments.**

5. **The digest comment is a standalone comment.**

---

#### Preemptive Task 2: Downstream propagation (2.1.x, preemptive)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

##### Description Digest Comment for Preemptive Task 2

After creating this preemptive downstream task, the following steps are performed:

1. **Re-fetch the description** from Jira API after creation:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest as a standalone comment** on the preemptive downstream task:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Posted in ADF format:
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **This digest comment is posted BEFORE creating issue links or other comments.**

5. **The digest comment is a standalone comment.**

---

### Preemptive Task Linkage (2.1.x)

After creating both preemptive tasks and posting their digest comments:

1. **Link preemptive upstream task to originating CVE Jira with "Related" (not "Depend"):**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

2. **Link preemptive downstream task to originating CVE Jira with "Related":**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   ```

3. **Link preemptive downstream subtask as blocked by preemptive upstream task:**
   ```
   jira.create_link(
     inwardIssue: <preemptive-upstream-task-key>,
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Add comment** to TC-8001 listing the preemptive tasks:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
     <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```
   Comment includes the Comment Footnote.

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8001

The summary comment documents:

1. **Version impact table** (from Step 2)
2. **Affects Versions correction**: `RHTPA 2.0.0` (PSIRT) -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (corrected, scoped to 2.2.x stream)
3. **Triage outcome**: Remediation tasks created for 2.2.x stream (Case A); preemptive remediation tasks created for 2.1.x stream (Case B)
4. **Links to all remediation tasks**:
   - 2.2.x: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation)
   - 2.1.x (preemptive): <preemptive-upstream-task-key>, <preemptive-downstream-task-key>
5. **@mention of the reporter** (the PSIRT analyst who created TC-8001) using ADF mention node:
   ```json
   { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
   ```

### Comment Footnote

Every comment posted to Jira by this skill ends with the Comment Footnote, using plugin version `0.11.0` and skill name `triage-security`:

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
      "text": " v0.11.0."
    }
  ]
}
```

This footnote is appended as the final two nodes in the ADF document's `content` array for every Jira comment posted during this triage: the post-triage summary, cross-stream notices, Affects Versions correction comments, and preemptive task comments. The description digest comments are standalone and do NOT include this footnote -- they contain only the marker line `[sdlc-workflow] Description digest: <tagged-digest>`.

---

## Description Digest Protocol Summary

For every remediation task created during this triage (both standard Case A tasks and preemptive Case B tasks), the description digest protocol is followed:

1. **After creating each task**, the description is re-fetched from Jira (not the string passed to `create_issue`, since Jira normalizes content during storage).
2. The re-fetched description is written to a temp file and the digest is computed using `python3 scripts/sha256-digest.py /tmp/task-desc.md`.
3. The script auto-detects format (ADF JSON -> `sha256-adf:<hex>`, markdown -> `sha256-md:<hex>`) and outputs a format-tagged digest with exactly 64 hexadecimal characters.
4. A standalone comment is posted on the task with the exact marker prefix `[sdlc-workflow] Description digest:` followed by the tagged digest value.
5. This digest comment is posted **before** creating issue links or other comments on the task.
6. The digest comment is a standalone comment -- not embedded in the footnote, not appended to any other comment, and not combined with the post-triage summary.
7. No placeholder text, abbreviated hashes, example hashes, or extra text is included -- only the exact marker line with the computed tagged digest.

Tasks receiving digest comments in this triage:
- Upstream backport task (2.2.x) -- standard remediation
- Downstream propagation task (2.2.x) -- standard remediation
- Preemptive upstream backport task (2.1.x) -- preemptive remediation
- Preemptive downstream propagation task (2.1.x) -- preemptive remediation
