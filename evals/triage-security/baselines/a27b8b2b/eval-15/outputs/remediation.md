# Step 8 -- Post-Triage Summary

## Triage Outcome

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x
stream are affected. This is **Case B** (affected versions exist) with **Case A**
cross-stream impact (the 2.1.x stream is also affected).

### Remediation Tasks Created (2.2.x stream -- in scope)

Since quinn-proto is a Cargo ecosystem dependency (source dependency), two tasks are
created for the 2.2.x stream:

1. **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
   - Repository: backend
   - Target Branch: release/0.4.z
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Depend (TC-8001 -> upstream-task)

2. **Downstream propagation subtask**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
   - Repository: rhtpa-release.0.4.z
   - Target Branch: main
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Depend (TC-8001 -> downstream-task)
   - Link: Blocks (upstream-task -> downstream-task)

### Cross-Stream Impact (Case A -- 2.1.x)

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9). A cross-stream
impact comment is posted, and sibling CVE Jira existence is checked. If no sibling CVE
Jira exists for stream 2.1.x, preemptive remediation tasks are created with the
`security-preemptive` label.

### Label Addition

The `ai-cve-triaged` label is added to TC-8001 to mark it as triaged.

---

## Post-Triage Summary Comment

The following comment is posted to TC-8001 as the post-triage summary. It includes
an @mention of the vulnerability issue's reporter (psirt-analyst) using an ADF mention
node. This @mention is mandatory and requires no ProdSec configuration -- it uses the
reporter field from the Jira issue, which is always available.

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
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Version Impact (stream 2.2.x)"
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
          "text": "Corrected: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md, scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
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
          "text": "Remediation tasks created for stream 2.2.x (Cargo — source dependency, 2 tasks):"
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
                  "text": "<upstream-task-key> — Upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z"
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
                  "text": "<downstream-task-key> — Downstream propagation: update backend ref in rhtpa-release.0.4.z (blocked by <upstream-task-key>)"
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
          "text": "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (all versions ship 0.11.9). See Related links for companion issues."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "cc "
        },
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
          "text": " v0.13.6."
        }
      ]
    }
  ]
}
```

### Reporter @mention Explanation

The post-triage summary comment includes an @mention of the vulnerability issue's reporter
(**psirt-analyst**, account ID `557058:psirt-analyst-mock-id`) using an ADF `mention` node:

```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:psirt-analyst-mock-id",
    "text": "@psirt-analyst"
  }
}
```

This @mention is **mandatory by default** and does not require any ProdSec configuration.
It uses the `reporter` field from the Jira issue data extracted in Step 1 -- the reporter
field is always available on every Jira issue. The reporter account ID
(`557058:psirt-analyst-mock-id`) is taken directly from the issue's reporter field, not
from any Security Configuration setting.

This ensures the PSIRT analyst who created the vulnerability issue is notified when triage
is complete, regardless of whether ProdSec contact configuration exists.

### Comment Footnote

The comment ends with the standard Comment Footnote per `shared/comment-footnote.md`:
a horizontal rule (`"type": "rule"`) followed by the AI-generated attribution with a
link to the sdlc-plugins repository and plugin version v0.13.6.
