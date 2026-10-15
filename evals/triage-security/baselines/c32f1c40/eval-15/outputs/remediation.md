# Step 8 -- Remediation and Post-Triage Summary

## Triage Outcome

The version impact table shows that within the issue's scoped stream (2.2.x):
- **Affected**: 2.2.0, 2.2.1, 2.2.2
- **Not affected**: 2.2.3, 2.2.4

This is **Case A/B** -- affected versions exist, remediation tasks are needed.

### Cross-Stream Impact (Case A)

The issue is scoped to `[rhtpa-2.2]`. The version impact analysis also shows that stream 2.1.x is affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). A cross-stream impact comment would be proposed on TC-8001.

### Step 7.5 -- Release Jira Orchestration

Release Jira orchestration confirmations would be required before creating remediation tasks:

1. **Resolve stream-to-version mapping**: Search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"`. If found, use it; if not, prompt the engineer to confirm the release version (default: next patch bump from latest released version 2.2.4, i.e., RHTPA 2.2.5).

2. **Find or create release Task**: Search for a release Task `"RHTPA <version> CVE triage"` under the release Epic. If not found, prompt the engineer to confirm creation.

3. **Cross-CVE dedup check (Step 7.5.3)**: The Upstream Affected Component custom field configuration is not present in this CLAUDE.md (no `customfield_10632` configured). Therefore, dedup is skipped per the prerequisite requirement.

> **Note**: Release evidence and confirmations are not available in this eval context. The release orchestration steps are described as pending proposed work -- no Jira operations were performed and no release Epic or Task creation is claimed.

## Remediation Tasks (Case B)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks would be created for the 2.2.x stream:

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9 (retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z (from Ecosystem Mappings)
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol

After creating each remediation task, the following description digest steps would be performed:

1. **Re-fetch the task description** from Jira after `create_issue` (the description is re-fetched from the API, not the string passed to create_issue, since Jira normalizes content during storage)
2. **Compute a SHA-256 digest** using `scripts/sha256-digest.py` on the re-fetched description
3. **Post a digest comment** with the marker `[sdlc-workflow] Description digest: <tagged-digest>` (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. The digest comment is posted **before** creating issue links (Depend, Blocks) or other comments on the task

This applies to both the upstream backport task and the downstream propagation subtask.

### Jira Linkage (proposed)

After task creation (and after description digest comments):

1. Link upstream task to TC-8001 (Depend)
2. Link downstream task to TC-8001 (Depend)
3. Link upstream task to downstream task (Blocks -- upstream blocks downstream)
4. If release Task exists from Step 7.5: link remediation tasks to release Task (Blocks), link TC-8001 to release Task (Related)
5. Transition TC-8001 to In Progress
6. Add `ai-cve-triaged` label to TC-8001

---

## Post-Triage Summary Comment

The following summary comment would be posted on TC-8001 after all triage actions are complete. This comment includes an @mention of the vulnerability issue's reporter (psirt-analyst) using an ADF mention node.

### Summary Comment Content

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version impact:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | (2.1.x stream) |
| 2.1.1 | 0.11.9 | YES | (2.1.x stream) |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].

Triage outcome: Remediation tasks created for stream 2.2.x.
- Upstream backport task: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- Downstream propagation subtask: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

Cross-stream impact: Stream 2.1.x is also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9).
```

### Reporter @mention (ADF mention node)

The post-triage summary comment includes an @mention of the vulnerability issue's reporter. This @mention is mandatory and requires no ProdSec configuration -- it uses the reporter field from the Jira issue data extracted in Step 1.

```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:psirt-analyst-mock-id",
    "text": "@psirt-analyst"
  }
}
```

### Full ADF Document for Post-Triage Summary Comment

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
          "text": "Version impact:",
          "marks": [{ "type": "strong" }]
        }
      ]
    },
    {
      "type": "table",
      "attrs": { "isNumberColumnEnabled": false, "layout": "default" },
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.x stream" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.x stream" }] }] }
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "—" }] }] },
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
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions correction: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage outcome: Remediation tasks created for stream 2.2.x (Cargo ecosystem, source dependency -- 2 tasks)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: Stream 2.1.x is also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9). These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
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
          "text": " v0.13.10."
        }
      ]
    }
  ]
}
```

### Key @mention Details

1. **Reporter @mention (Step 8 -- post-triage summary)**:
   - Account ID: `557058:psirt-analyst-mock-id`
   - Display text: `@psirt-analyst`
   - ADF node type: `mention`
   - This @mention is present by default without any ProdSec configuration. It uses the `reporter` field from the Jira issue data extracted in Step 1. The reporter is always available on the Jira issue.

2. **ProdSec @mention (Step 3 -- Affects Versions correction)**:
   - Account ID: `557058:prodsec-mock-account-id`
   - Display text: `@prodsec-team`
   - ADF node type: `mention`
   - This @mention is included because the Security Configuration contains `ProdSec Jira account ID: 557058:prodsec-mock-account-id`. It appears before the Comment Footnote in the Affects Versions correction comment (see outputs/affects-versions.md).
   - If no ProdSec Jira account ID were configured, this @mention would be omitted silently.

> **Note**: All actions described above are proposed -- no Jira operations were performed. External tool invocation is prohibited in this eval.
