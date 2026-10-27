# Step 8 -- Post-Triage Summary

## Triage Outcome

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **Stream scope**: 2.2.x
- **Outcome**: Case B (affected versions exist) + Case A (cross-stream impact on 2.1.x)

## Affected Versions (in scope)

- RHTPA 2.2.0: quinn-proto 0.11.9 -- AFFECTED
- RHTPA 2.2.1: quinn-proto 0.11.12 -- AFFECTED
- RHTPA 2.2.2: retag of 2.2.1 -- AFFECTED

## Not Affected Versions

- RHTPA 2.2.3: quinn-proto 0.11.14 -- NOT AFFECTED (ships fixed version)
- RHTPA 2.2.4: quinn-proto 0.11.14 -- NOT AFFECTED (ships fixed version)

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but is
outside this issue's scope. Cross-stream impact comment posted. Companion issues for the
2.1.x stream should be tracked separately by PSIRT.

## Remediation Tasks

Ecosystem: Cargo (source dependency) -- 2 tasks per affected stream.

For stream 2.2.x:
1. **Upstream dependency bump task**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
   - Repository: backend
   - Target branch: release/0.4.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812
2. **Downstream propagation task**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Blocked by: upstream dependency bump task

## Post-Triage Summary Comment (ADF format)

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
          "text": "Triage Summary — CVE-2026-31812 (quinn-proto)"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Version impact analysis for quinn-proto (affected range: < 0.11.14, fixed: 0.11.14):"
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "outside issue scope (2.1.x)" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "outside issue scope (2.1.x)" }] }] }
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
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage outcome: ",
          "marks": [{ "type": "strong" }]
        },
        {
          "type": "text",
          "text": "Remediation required. Affected versions in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2) ship quinn-proto below the fix threshold (0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: ",
          "marks": [{ "type": "strong" }]
        },
        {
          "type": "text",
          "text": "The 2.1.x stream (2.1.0, 2.1.1) is also affected (quinn-proto 0.11.9). These versions are outside this issue's scope and are tracked by companion issues or may require separate PSIRT triage."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Remediation tasks created for stream 2.2.x:"
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
                  "text": "Upstream dependency bump: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x) — bump quinn-proto on release/0.4.z in backend repo"
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
                  "text": "Downstream propagation: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x) — blocked by upstream task"
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
