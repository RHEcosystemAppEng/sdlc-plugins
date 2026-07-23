# Step 8 -- Post-Triage Summary: TC-8001

## Triage Outcome

**Case A + Case B**: Stream 2.2.x is affected (versions 2.2.0, 2.2.1, 2.2.2).
Cross-stream impact detected: stream 2.1.x is also affected (versions 2.1.0, 2.1.1).

### Remediation Tasks (Stream 2.2.x -- in scope)

Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are created:

1. **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
   - Repository: backend
   - Target branch: release/0.4.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend on TC-8001

2. **Downstream propagation task**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Blocked by upstream task; Depend on TC-8001

### Cross-Stream Impact (Stream 2.1.x -- out of scope)

Stream 2.1.x is also affected (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9) but
is outside this issue's stream scope [rhtpa-2.2]. Cross-stream impact comment posted
to TC-8001. If no companion CVE Jira exists for stream 2.1.x, preemptive remediation
tasks would be created with the security-preemptive label.

### Label Added

- `ai-cve-triaged` added to TC-8001

## Post-Triage Summary Comment (ADF format)

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
          "text": "Version Impact"
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
          "text": "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. PSIRT-assigned RHTPA 2.0.0 does not match any configured version stream. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
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
          "text": "Case A: Affected — remediation tasks created for stream 2.2.x. quinn-proto is a Cargo dependency (source dependency ecosystem), so two tasks were created: upstream backport + downstream propagation."
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
                  "text": "Upstream backport (2.2.x): Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 on release/0.4.z"
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
                  "text": "Downstream propagation (2.2.x): Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (blocked by upstream task)"
                }
              ]
            }
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
          "text": "Cross-Stream Impact"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
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
          "text": " v0.13.4."
        }
      ]
    }
  ]
}
```
