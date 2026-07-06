# Step 8 -- Post-Triage Summary: TC-8001

## Triage Outcome

- **Case A**: Affected -- remediation tasks needed for stream 2.2.x (versions 2.2.0, 2.2.1, 2.2.2)
- **Case B**: Cross-stream impact -- stream 2.1.x (versions 2.1.0, 2.1.1) is also affected

### Remediation Tasks (2.2.x stream -- in scope)

Ecosystem: Cargo (source dependency) -- two tasks per stream:

1. **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
   - Repository: backend
   - Target branch: release/0.4.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812

2. **Downstream propagation task**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Blocked by: upstream backport task

### Cross-Stream Impact (2.1.x -- out of scope)

Stream 2.1.x (versions 2.1.0, 2.1.1) ships quinn-proto 0.11.9 (vulnerable). Preemptive remediation tasks would be created with `security-preemptive` label and "Related" link type to TC-8001.

## Post-Triage Summary Comment (ADF)

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 3},
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
          "text": "Version Impact Analysis",
          "marks": [{"type": "strong"}]
        }
      ]
    },
    {
      "type": "table",
      "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
      "content": [
        {
          "type": "tableRow",
          "content": [
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Version"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Stream"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "quinn-proto"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Affected?"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.2"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES (retag of 2.2.1)"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.3"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.4"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]}
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions Correction",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": ": RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2. RHTPA 2.0.0 is not a valid version in any configured stream. Corrected based on lock file evidence."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage Outcome",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": ": Affected -- remediation tasks created for stream 2.2.x. Cross-stream impact detected in stream 2.1.x."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Remediation tasks (2.2.x):",
          "marks": [{"type": "strong"}]
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
                  "text": "Upstream backport: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)"
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
                  "text": "Downstream propagation: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)"
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
          "text": "Cross-stream impact (2.1.x):",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": " quinn-proto 0.11.9 in versions 2.1.0 and 2.1.1 is within the affected range (< 0.11.14). Preemptive remediation tasks created with security-preemptive label."
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
        },
        {
          "type": "text",
          "text": " Triage complete for CVE-2026-31812. Remediation tasks have been created for stream 2.2.x. Cross-stream impact identified in 2.1.x -- preemptive remediation tasks created."
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
          "text": " v0.12.2."
        }
      ]
    }
  ]
}
```
