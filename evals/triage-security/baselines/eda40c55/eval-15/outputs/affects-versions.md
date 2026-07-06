# Step 3 -- Affects Versions Correction: TC-8001

## Proposed Change

**Current Affects Versions**: RHTPA 2.0.0
**Corrected Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

PSIRT assigned "RHTPA 2.0.0" as the Affects Version, but lock file analysis shows:
- RHTPA 2.0.0 does not exist in any configured version stream
- The issue is scoped to stream 2.2.x (from summary suffix [rhtpa-2.2])
- Within stream 2.2.x, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (vulnerable)
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed) and are NOT affected

## Jira Comment (ADF)

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": ": RHTPA 2.0.0 "
        },
        {
          "type": "text",
          "text": "->"
        },
        {
          "type": "text",
          "text": " RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Lock file analysis shows quinn-proto versions per release:"
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
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "quinn-proto"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Affected?"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.2"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12 (retag of 2.2.1)"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.3"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.4"}]}]},
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
          "text": "RHTPA 2.0.0 is not a valid version in any configured stream. The correct Affects Versions for the 2.2.x stream are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2 (all ship quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {
            "id": "557058:prodsec-mock-account-id",
            "text": "@prodsec-team"
          }
        },
        {
          "type": "text",
          "text": " FYI -- Affects Versions have been corrected based on lock file evidence."
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
