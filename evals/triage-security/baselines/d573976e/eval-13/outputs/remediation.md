# Step 8 -- Remediation

## Triage Decision

The issue TC-8001 is scoped to stream **2.2.x**. The version impact table shows:
- **2.2.0** (quinn-proto 0.11.9): AFFECTED
- **2.2.1** (quinn-proto 0.11.12): AFFECTED
- **2.2.2** (retag of 2.2.1): AFFECTED
- **2.2.3** (quinn-proto 0.11.14): NOT affected
- **2.2.4** (quinn-proto 0.11.14): NOT affected

Supported versions 2.2.0, 2.2.1, and 2.2.2 are affected. This is **Case A: Affected -- create remediation tasks**.

The ecosystem is **Cargo** (source dependency), so **two tasks** are created: an upstream backport task and a downstream propagation subtask.

Additionally, **Case B: Cross-stream impact** applies because stream 2.1.x is also affected but is outside this issue's scope.

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task

**Proposed Jira creation:**

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

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 from supportability matrix

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

#### Description Digest Protocol for Upstream Task

After creating the upstream backport task, the following description digest procedure is performed **before** creating issue links or any other comments:

1. **Re-fetch the task description from the Jira API** after `create_issue` returns the new task key (e.g., TC-8050). This is critical because Jira normalizes content during storage -- the description passed to `create_issue` may differ from what Jira stores:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute the SHA-256 digest using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. **Post a standalone digest comment** on the newly created task with the marker `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is replaced with the actual output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...` -- full 64-character hex). The comment body uses ADF contentFormat:
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

4. **Only after the digest comment is posted**, proceed to create issue links and other comments on this task.

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira creation:**

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

#### Description Digest Protocol for Downstream Subtask

After creating the downstream propagation subtask, the following description digest procedure is performed **before** creating issue links or any other comments:

1. **Re-fetch the task description from the Jira API** after `create_issue` returns the new task key (e.g., TC-8051). The digest must be computed from the re-fetched description, not from the description string passed to `create_issue`, because Jira normalizes content during storage:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute the SHA-256 digest using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. **Post a standalone digest comment** on the newly created task with the marker `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is replaced with the actual output from `scripts/sha256-digest.py` (full 64-character hex digest). The comment body uses ADF contentFormat:
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

4. **Only after the digest comment is posted**, proceed to create issue links and other comments on this task.

---

## Complete Procedure Sequence for Both Tasks

The full sequence of Jira operations after version impact analysis is:

### Upstream Backport Task
1. `jira.create_issue(...)` -- create the upstream backport task
2. `jira.get_issue(<upstream-task-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest from re-fetched description
4. `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. `jira.create_link(inwardIssue: TC-8001, outwardIssue: <upstream-task-key>, type: "Depend")` -- link to vulnerability

### Downstream Propagation Subtask
6. `jira.create_issue(...)` -- create the downstream propagation subtask
7. `jira.get_issue(<downstream-task-key>, fields=["description"])` -- re-fetch description
8. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest from re-fetched description
9. `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
10. `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")` -- link to vulnerability
11. `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")` -- blocks dependency

### Post-Triage Actions
12. Transition TC-8001 to In Progress
13. Assign TC-8001 to current user
14. Add `ai-cve-triaged` label to TC-8001
15. Post summary comment on TC-8001 with version impact table, remediation task links, and reporter @mention

**Key sequencing constraint**: For each task, the description digest comment (steps 4 and 9) is posted **before** issue links (steps 5, 10, 11) or any other comments. This is mandated by `shared/description-digest-protocol.md` Rules: "Producers must post the digest comment immediately after creating the task issue, before creating issue links or other comments."

**Key computation constraint**: The digest is computed from the **re-fetched** description (steps 2-3 and 7-8), not from the description string passed to `create_issue`. This is because Jira normalizes content during storage, and the stored description may differ from the input. Per `shared/description-digest-protocol.md` Hashing: "Do not hash the description string passed to create_issue -- always re-fetch from the API after creation, since Jira normalizes content during storage."

---

## Case B: Cross-Stream Impact

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9, which is within the affected range < 0.11.14). Since this issue is scoped to stream 2.2.x, a cross-stream impact notice is posted and preemptive remediation tasks may be created for stream 2.1.x if no sibling CVE Jira exists for that stream.

**Proposed cross-stream impact comment on TC-8001:**

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

---

## Comment Footnote

All Jira comments posted by this skill include the following footnote (plugin version 0.11.1):

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
