# Step 8 -- Remediation

## Triage Decision

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14). This is **Case B** (affected -- create remediation tasks).

Additionally, the 2.1.x stream (2.1.0, 2.1.1) is also affected -- this triggers **Case A** (cross-stream impact) since the issue is scoped to [rhtpa-2.2] and the 2.1.x stream is outside its scope.

## Case A -- Cross-Stream Impact

The issue is scoped to stream 2.2.x. The version impact analysis reveals that stream 2.1.x is also affected (both versions ship quinn-proto 0.11.9, which is within the affected range < 0.11.14).

**Proposed cross-stream impact comment on TC-8001:**

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
```

A search for sibling CVE Jiras with label CVE-2026-31812 in stream 2.1.x would determine whether preemptive tasks are needed for that stream.

## Case B -- Remediation Tasks for 2.2.x

Cargo is a source dependency ecosystem, so two tasks are created per the ecosystem classification table:

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

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

**Post-creation steps:**
1. Re-fetch the task description from Jira after `create_issue`
2. Compute SHA-256 digest using `scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Then create issue links (Depend to TC-8001)

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

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

**Post-creation steps:**
1. Re-fetch the task description from Jira after `create_issue`
2. Compute SHA-256 digest using `scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Then create issue links:
   - Depend: TC-8001 -> <downstream-task-key>
   - Blocks: <upstream-task-key> -> <downstream-task-key>

## Jira Linkage

After creating both tasks and posting their digest comments:

1. Link upstream task to TC-8001 with "Depend"
2. Link downstream task to TC-8001 with "Depend"
3. Link downstream task as blocked by upstream task with "Blocks"
4. Transition TC-8001 to In Progress
5. Add `ai-cve-triaged` label to TC-8001

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8001 after all triage actions complete. The comment includes an @mention of the vulnerability issue reporter (psirt-analyst, account ID 557058:psirt-analyst-mock-id) using an ADF mention node. This @mention is mandatory and uses the reporter field from the Jira issue -- it requires no ProdSec configuration and works by default on every issue.

**Comment (ADF format):**

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
          "text": "Triage Summary -- CVE-2026-31812 (quinn-proto)"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):"
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "ships fixed version" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.4" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "ships fixed version" }] }] }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage outcome: Remediation tasks created (Case B -- affected versions found in 2.2.x stream)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Remediation tasks created:"
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
                  "text": "<upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)"
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
                  "text": "<downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)"
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
          "text": "Cross-stream impact: stream 2.1.x is also affected (quinn-proto 0.11.9 < 0.11.14 in versions 2.1.0, 2.1.1)."
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

### Key @mention Details

**Reporter @mention (Step 8 -- mandatory, no configuration needed):**
- The post-triage summary comment includes an ADF mention node for the vulnerability issue's reporter
- Account ID: `557058:psirt-analyst-mock-id` (from the Jira issue's reporter field)
- This @mention is present by default on every post-triage summary -- it uses the reporter field from the Jira issue data extracted in Step 1, not any ProdSec configuration
- The mention node: `{ "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }`

**ProdSec @mention (Step 3 -- configuration-dependent):**
- The Affects Versions correction comment (see outputs/affects-versions.md) includes an ADF mention node for the ProdSec contact
- Account ID: `557058:prodsec-mock-account-id` (from Security Configuration's ProdSec Jira account ID)
- This @mention only appears when the ProdSec Jira account ID is configured in Security Configuration
- The mention node: `{ "type": "mention", "attrs": { "id": "557058:prodsec-mock-account-id", "text": "@prodsec-team" } }`

### Post-Triage Actions

1. Added `ai-cve-triaged` label to TC-8001
2. Posted the summary comment above to TC-8001
3. The reporter @mention notifies the PSIRT analyst (psirt-analyst) who created the vulnerability issue
