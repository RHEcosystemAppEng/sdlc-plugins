# Step 8 -- Remediation and Post-Triage Summary

## Triage Outcome: Case A -- Affected (create remediation tasks)

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x
stream are affected by CVE-2026-31812 (quinn-proto < 0.11.14). Remediation tasks are
required.

Since quinn-proto is a **Cargo** ecosystem (source dependency), two tasks are created:
an upstream backport task and a downstream propagation subtask.

---

## Proposed Remediation Task 1: Upstream Backport Task

**Jira creation call (proposed):**

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description (following task-description-template.md):

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
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

### Description Digest Protocol (upstream task):

After creating the upstream task, the following digest protocol steps would be executed:

1. **Re-fetch the description** from Jira API after create_issue:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   Note: The digest is computed from the re-fetched description (via Jira API after
   create_issue), NOT from the description string passed to create_issue. Jira
   normalizes content during storage, so the stored version may differ from the input.

2. **Write description to temp file and compute SHA-256 digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex-digest>` or `sha256-adf:<64-char-hex-digest>`

3. **Post digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The comment body is exactly one line:
   `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` (or `sha256-adf:<64-char-hex>`)

4. **After the digest comment**, create issue links:
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Proposed Remediation Task 2: Downstream Propagation Subtask

**Jira creation call (proposed):**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description (following task-description-template.md):

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

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (downstream task):

After creating the downstream task, the following digest protocol steps would be executed:

1. **Re-fetch the description** from Jira API after create_issue:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   Note: The digest is computed from the re-fetched description (via Jira API after
   create_issue), NOT from the description string passed to create_issue. Jira
   normalizes content during storage, so the stored version may differ from the input.

2. **Write description to temp file and compute SHA-256 digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex-digest>` or `sha256-adf:<64-char-hex-digest>`

3. **Post digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The comment body is exactly one line:
   `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` (or `sha256-adf:<64-char-hex>`)

4. **After the digest comment**, create issue links:
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Jira Linkage Summary (proposed)

After both tasks are created and their digest comments are posted:

1. Upstream task linked to TC-8001 with "Depend" link type
2. Downstream task linked to TC-8001 with "Depend" link type
3. Downstream task linked to upstream task with "Blocks" link type
   (downstream is blocked by upstream -- upstream backport must merge first)

---

## Post-Triage Actions (proposed)

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Transition**: TC-8001 to "In Progress"
3. **Assign**: TC-8001 to current user

---

## Post-Triage Summary Comment (proposed for TC-8001)

The following summary comment would be posted to TC-8001. It includes an @mention
of the vulnerability issue's reporter (psirt-analyst) using an ADF mention node.
The reporter @mention is mandatory and requires no configuration -- the reporter
field is always available on the Jira issue.

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Triage Summary"
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Version Impact"
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Version" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "quinn-proto" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Affected?" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Notes" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.2" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "--" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "retag of 2.2.1" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.3" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.4" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Affects Versions Correction"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Triage Outcome"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Case A: Affected versions found. Remediation tasks created."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Remediation Tasks"
        }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "<upstream-task-key> -- Upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z (rhtpa-backend)"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "<downstream-task-key> -- Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z (blocked by <upstream-task-key>)"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": ""
        },
        {
          "type": "mention",
          "attrs": {
            "id": "557058:psirt-analyst-mock-id",
            "text": "@psirt-analyst"
          }
        },
        {
          "type": "text",
          "text": " FYI -- triage complete for CVE-2026-31812."
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
  ]
}
```

### @Mention Details

**Reporter @mention (Step 8 post-triage summary):**
- Account ID: `557058:psirt-analyst-mock-id`
- Display text: `@psirt-analyst`
- ADF node: `{ "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }`
- This @mention is mandatory and requires no ProdSec configuration -- it uses the reporter
  field from the Jira issue. The reporter is always available on the Jira issue data
  extracted in Step 1.

**ProdSec @mention (Step 3 Affects Versions correction):**
- Account ID: `557058:prodsec-mock-account-id`
- Display text: `@prodsec-team`
- ADF node: `{ "type": "mention", "attrs": { "id": "557058:prodsec-mock-account-id", "text": "@prodsec-team" } }`
- This @mention is conditional on ProdSec Jira account ID being configured in Security
  Configuration. In this case, it IS configured (557058:prodsec-mock-account-id) and is
  included in the Affects Versions correction comment (see outputs/affects-versions.md).

### Triage Actions Summary

All triage actions are presented as **proposals** for engineer confirmation. No Jira
mutations are executed without explicit approval:

1. **Proposed**: Correct Affects Versions from [RHTPA 2.0.0] to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
2. **Proposed**: Create upstream backport task (bump quinn-proto to 0.11.14 on release/0.4.z)
3. **Proposed**: Create downstream propagation subtask (update ref in rhtpa-release.0.4.z)
4. **Proposed**: Add ai-cve-triaged label to TC-8001
5. **Proposed**: Transition TC-8001 to In Progress
6. **Proposed**: Assign TC-8001 to current user
7. **Proposed**: Post summary comment with reporter @mention to TC-8001
