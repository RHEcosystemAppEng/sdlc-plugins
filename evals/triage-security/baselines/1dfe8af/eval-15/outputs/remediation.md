# Step 7 — Post-Triage Summary: TC-8001

## Triage Outcome

**Case A + Case B**: The 2.2.x stream (issue scope) has affected versions (2.2.0, 2.2.1, 2.2.2) that require remediation. Additionally, the 2.1.x stream is also affected (cross-stream impact).

However, the vulnerability is already **fixed in the 2.2.x stream** starting from version 2.2.3 (quinn-proto upgraded to 0.11.14 in build 0.4.11). No new remediation tasks are needed for the 2.2.x stream since the fix is already present in the latest releases.

Cross-stream impact: The 2.1.x stream (all versions: 2.1.0, 2.1.1) ships quinn-proto 0.11.9, which is vulnerable. This stream is outside the issue's scope and may require separate PSIRT triage or preemptive remediation.

## Actions Taken

1. **Affects Versions corrected**: Removed RHTPA 2.0.0; set to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Label added**: `ai-cve-triaged`
3. **Cross-stream impact identified**: 2.1.x stream also affected (quinn-proto 0.11.9 across all versions)

## Post-Triage Summary Comment

The following comment would be posted to TC-8001 (ADF format):

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
          "text": "Triage complete for "
        },
        {
          "type": "text",
          "text": "TC-8001",
          "marks": [{ "type": "strong" }]
        },
        {
          "type": "text",
          "text": ". CVE-2026-31812 affects quinn-proto versions before 0.11.14 (CVSS 7.5 High — Denial of Service via excessive stream counts in QUIC transport frames)."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Version Impact (2.2.x stream — issue scope)"
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Version" }] }]
            },
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "quinn-proto" }] }]
            },
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Affected?" }] }]
            },
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Notes" }] }]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9 < 0.11.14" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12 < 0.11.14" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.2" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12" }] }] },
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
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Fixed (>= 0.11.14)" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.4" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Fixed (>= 0.11.14)" }] }] }
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
          "text": "Cross-Stream Impact (2.1.x)"
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Version" }] }]
            },
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "quinn-proto" }] }]
            },
            {
              "type": "tableHeader",
              "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Affected?" }] }]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (all versions ship 0.11.9). The 2.1.x stream is tracked by a separate Konflux release repo (rhtpa-release.0.3.z) and may require separate PSIRT triage or preemptive remediation."
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
          "text": "PSIRT-assigned Affects Version "
        },
        {
          "type": "text",
          "text": "RHTPA 2.0.0",
          "marks": [{ "type": "strong" }]
        },
        {
          "type": "text",
          "text": " was incorrect (no 2.0.x stream exists). Corrected to: "
        },
        {
          "type": "text",
          "text": "RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2",
          "marks": [{ "type": "strong" }]
        },
        {
          "type": "text",
          "text": " based on lock file evidence."
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
          "text": "The vulnerability is already fixed in the 2.2.x stream starting from version 2.2.3 (quinn-proto upgraded to 0.11.14 in build 0.4.11). Versions 2.2.0, 2.2.1, and 2.2.2 remain affected but the fix is present in the latest supported versions. The 2.1.x stream requires attention as all versions remain vulnerable."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Label "
        },
        {
          "type": "text",
          "text": "ai-cve-triaged",
          "marks": [{ "type": "code" }]
        },
        {
          "type": "text",
          "text": " added to TC-8001."
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
