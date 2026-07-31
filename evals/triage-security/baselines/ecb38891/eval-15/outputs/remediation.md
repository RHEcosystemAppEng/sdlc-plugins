# Step 8 -- Remediation

## Triage Decision

The version impact table shows that 2.2.x versions 2.2.0, 2.2.1, and 2.2.2 are affected (ship quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14). This is **Case B: Affected -- create remediation tasks**.

Cross-stream impact (Case A): Stream 2.1.x is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since this issue is scoped to [rhtpa-2.2], a cross-stream impact comment would be posted and sibling issue handling applies.

**Ecosystem**: Cargo (source dependency) -- creates **two tasks** per the ecosystem classification table: upstream backport + downstream propagation.

---

## Remediation Task 1: Upstream Backport Task

### Jira Issue Creation

```
upstream_task = jira.create_issue(
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

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
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

### Description Digest Protocol

After creating the upstream backport task, the following digest procedure is performed:

1. **Re-fetch the task description** from Jira after `create_issue` (since Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the re-fetched description** to a temp file and compute the digest using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
3. **Post the digest comment** on the upstream task **before** creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The `<tagged-digest>` is the full output from `scripts/sha256-digest.py` including the format tag.

The digest comment uses the marker `[sdlc-workflow] Description digest:` and is posted as a standalone comment. It is sequenced **before** the Depend link to TC-8001 and the Blocks link to the downstream task.

---

## Remediation Task 2: Downstream Propagation Subtask

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
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

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

### Description Digest Protocol

After creating the downstream propagation subtask, the same digest procedure is performed:

1. **Re-fetch the task description** from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Compute the digest** from the re-fetched description (not the description string passed to create_issue):
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. **Post the digest comment** on the downstream task **before** creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

The digest comment is posted before:
- The Depend link to TC-8001
- The Blocks link from the upstream task
- Any other comments on the task

---

## Jira Linkage (after digest comments)

After digest comments are posted on both tasks, create the issue links:

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

3. **Link downstream as blocked by upstream:**
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition TC-8001 to In Progress** (if not already).

---

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post-Triage Summary Comment

The post-triage summary comment includes an **@mention of the vulnerability issue's reporter** (psirt-analyst). This @mention is mandatory and requires no configuration -- it uses the reporter field from the Jira issue data extracted in Step 1. The reporter's account ID (`557058:psirt-analyst-mock-id`) is available from the issue's `reporter` field.

#### Comment Content

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version impact (2.2.x stream):
| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | fixed |
| 2.2.4   | 0.11.14     | NO        | fixed |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Triage outcome: Remediation tasks created (Case B -- affected versions found).

Remediation tasks:
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: Stream 2.1.x is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). See companion issues or cross-stream notice.
```

#### Reporter @mention (ADF mention node)

The post-triage summary comment includes an @mention of the reporter using an ADF mention node. This @mention is present by default without any ProdSec configuration -- it uses the reporter field from the Jira issue:

```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:psirt-analyst-mock-id",
    "text": "@psirt-analyst"
  }
}
```

#### Full ADF Comment Structure

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
          "text": "Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Version impact (2.2.x stream):\n| Version | quinn-proto | Affected? | Notes |\n|---------|-------------|-----------|-------|\n| 2.2.0   | 0.11.9      | YES       |       |\n| 2.2.1   | 0.11.12     | YES       |       |\n| 2.2.2   | --          | YES       | retag of 2.2.1 |\n| 2.2.3   | 0.11.14     | NO        | fixed |\n| 2.2.4   | 0.11.14     | NO        | fixed |"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage outcome: Remediation tasks created (Case B -- affected versions found)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Remediation tasks:\n- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)\n- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: Stream 2.1.x is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). See companion issues or cross-stream notice."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {
            "id": "557058:psirt-analyst-mock-id",
            "text": "@psirt-analyst"
          }
        }
      ]
    },
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
          "text": " v0.13.7."
        }
      ]
    }
  ]
}
```

The reporter @mention is included **by default** without any ProdSec configuration requirement. The reporter field is always available on the Jira issue. The @mention uses the reporter's account ID from the issue data extracted in Step 1.

The Comment Footnote (rule + footer paragraph) appears at the very end, after the reporter @mention.
