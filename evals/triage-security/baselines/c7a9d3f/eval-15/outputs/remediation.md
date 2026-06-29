# Step 7 -- Post-Triage Summary

## Triage Outcome

**Case A + Case B**: The issue's scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), and the cross-stream analysis shows that stream 2.1.x is also affected.

### Scoped stream (2.2.x) -- Case A: Remediation tasks

Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks would be created:

1. **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
   - Repository: rhtpa-backend
   - Target branch: release/0.4.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812

2. **Downstream propagation task**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Blocked by: upstream backport task
   - Labels: ai-generated-jira, Security, CVE-2026-31812

### Cross-stream impact (2.1.x) -- Case B: Preemptive remediation

Stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) but is outside this issue's scope. If no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would be created:

1. **Preemptive upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link type: Related (to TC-8001)

2. **Preemptive downstream propagation task**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link type: Related (to TC-8001)

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8001
2. Transition TC-8001 to In Progress
3. Assign TC-8001 to the current user

## Post-Triage Summary Comment

The following comment would be posted to TC-8001. It includes a mandatory @mention of the reporter (psirt-analyst, account ID `557058:psirt-analyst-mock-id`) using an ADF mention node.

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Triage Summary for CVE-2026-31812"
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Version Impact Table"
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "stream 2.1.x" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "stream 2.1.x" }] }] }
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
          "text": "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
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
          "text": "Case A (Affected) + Case B (Cross-stream impact): Remediation tasks created for stream 2.2.x. Cross-stream impact detected for stream 2.1.x."
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
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Stream 2.2.x (scoped):"
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
                  "text": "Upstream backport: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2) -- linked with Depend"
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
                  "text": "Downstream propagation: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2) -- blocked by upstream task"
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
          "text": "Stream 2.1.x (cross-stream preemptive):"
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
                  "text": "Preemptive upstream backport: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) -- linked with Related, label security-preemptive"
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
                  "text": "Preemptive downstream propagation: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) -- linked with Related, label security-preemptive"
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
