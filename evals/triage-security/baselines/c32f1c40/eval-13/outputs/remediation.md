# Step 7.5 — Release Jira Orchestration

Before creating remediation tasks, release Jira orchestration is performed. Since this eval prohibits external tool calls, the following confirmations would be required in an interactive triage:

1. **Resolve stream-to-version mapping** for the 2.2.x stream:
   - Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`.
   - If no Epic exists, propose creating one (e.g., `RHTPA 2.2.5 Release Tasks` based on latest released version 2.2.4).
   - The exact release Epic version requires engineer confirmation (version decision is high-stakes).

2. **Find or create the release Task** (`"RHTPA <version> CVE triage"`) as a child of the release Epic.
   - Requires individual engineer confirmation for Task creation.

3. **Cross-CVE dedup check** — since the Upstream Affected Component custom field is not configured in the Security Configuration, the dedup step is **skipped**. No dedup check is performed because the field configuration is absent.

Release orchestration confirmations and release Jira creation are pending — they cannot be completed without interactive engineer confirmation and Jira access.

---

# Step 8 — Remediation

## Triage Decision

**Case B: Affected — create remediation tasks**

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a Cargo source dependency, the ecosystem classification table specifies **two tasks per affected stream**: an upstream backport task + a downstream propagation subtask.

## Case A: Cross-Stream Impact

The version impact analysis reveals that the **2.1.x stream** is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since the current issue is scoped to `[rhtpa-2.2]`, a cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis.
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

A search for sibling CVE Jiras with label `CVE-2026-31812` would determine whether preemptive tasks are needed for 2.1.x.

---

## Remediation Task 1: Upstream Backport Task (2.2.x stream)

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

### Description Digest Protocol — Upstream Backport Task

After creating the upstream backport task, the following description digest procedure is performed **before** creating any issue links or other comments:

1. **Re-fetch the task description from Jira** after `create_issue` returns the new task key (e.g., `<upstream-task-key>`). The description is re-fetched because Jira normalizes content during storage, and the digest must reflect the actual stored representation — not the description string passed to `create_issue`.

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file** and compute the SHA-256 digest using `scripts/sha256-digest.py`. The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest.

   ```bash
   # Write the re-fetched description to a temp file
   echo "<re-fetched-description>" > /tmp/task-desc.md

   # Compute the digest
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** on the newly created upstream backport task using the exact marker prefix `[sdlc-workflow] Description digest:` followed by the tagged digest value:

   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64-hex-chars`).

   The digest comment is posted as an ADF document:
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
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>"
           }
         ]
       }
     ]
   }
   ```

4. **Only after the digest comment is posted**, proceed to create issue links and other comments on the upstream backport task.

---

## Remediation Task 2: Downstream Propagation Subtask (2.2.x stream)

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
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

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

### Description Digest Protocol — Downstream Propagation Subtask

After creating the downstream propagation subtask, the following description digest procedure is performed **before** creating any issue links or other comments:

1. **Re-fetch the task description from Jira** after `create_issue` returns the new task key (e.g., `<downstream-task-key>`). The description is re-fetched because Jira normalizes content during storage, and the digest must reflect the actual stored representation — not the description string passed to `create_issue`.

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file** and compute the SHA-256 digest using `scripts/sha256-digest.py`. The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest.

   ```bash
   # Write the re-fetched description to a temp file
   echo "<re-fetched-description>" > /tmp/task-desc.md

   # Compute the digest
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** on the newly created downstream propagation subtask using the exact marker prefix `[sdlc-workflow] Description digest:` followed by the tagged digest value:

   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64-hex-chars`).

   The digest comment is posted as an ADF document:
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
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>"
           }
         ]
       }
     ]
   }
   ```

4. **Only after the digest comment is posted**, proceed to create issue links and other comments on the downstream propagation subtask.

---

## Post-Digest Jira Linkage Sequence

After **both** tasks are created and **both** digest comments are posted, the following linkage operations are performed in order:

### 1. Link upstream backport task to CVE Vulnerability issue (Depend)

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### 2. Link downstream propagation subtask to CVE Vulnerability issue (Depend)

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

### 3. Link downstream subtask as blocked by upstream task (Blocks)

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### 4. Release Jira Linking (if release Task active from Step 7.5)

```
jira.create_link(
  inwardIssue: <remediation-task-key>,
  outwardIssue: <release-task-key>,
  type: "Blocks"
)

jira.create_link(
  inwardIssue: <release-task-key>,
  outwardIssue: "TC-8001",
  type: "Related"
)
```

### 5. Transition CVE to In Progress

```
jira.transition_issue("TC-8001", <in-progress-transition-id>)
```

### 6. Add ai-cve-triaged label

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 7. Post summary comment to CVE issue

Post a summary comment to TC-8001 documenting the triage outcome, version impact table, remediation task keys, and an @mention of the vulnerability reporter. The comment includes the Comment Footnote.

---

## Digest Protocol Summary

The description digest protocol ensures integrity verification by `/implement-task`. The critical ordering is:

1. `create_issue` -- create the remediation task
2. `get_issue` -- **re-fetch** the description from Jira (not the input string)
3. `scripts/sha256-digest.py` -- compute SHA-256 digest from the re-fetched description
4. `add_comment` -- post digest comment with marker `[sdlc-workflow] Description digest: <tagged-digest>`
5. **Then** create issue links (Depend, Blocks) and other comments

This sequence is followed for **each** remediation task independently:
- Upstream backport task: create -> re-fetch description -> compute digest -> post digest comment -> then links
- Downstream propagation subtask: create -> re-fetch description -> compute digest -> post digest comment -> then links

The re-fetch step is essential because Jira normalizes content during storage. Hashing the input string passed to `create_issue` would produce a different digest than what `/implement-task` would compute when verifying, causing false integrity mismatches.

---

## Comment Footnote

All Jira comments posted by this skill include the Comment Footnote using ADF:

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
            "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins"
          }
        }
      ]
    },
    {
      "type": "text",
      "text": " v0.13.10."
    }
  ]
}
```
