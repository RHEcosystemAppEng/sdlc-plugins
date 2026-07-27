# Jira Comment

## API Call

```
addCommentToJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  issueIdOrKey="<created-issue-key>",
  comment=<see below>,
  contentFormat="adf"
)
```

## Comment Body (ADF)

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
          "text": "Feature created via define-feature skill"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This Feature was created interactively using the define-feature skill."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 4 },
      "content": [
        {
          "type": "text",
          "text": "Sections included"
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
                  "text": "Feature Overview"
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
                  "text": "Requirements"
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
          "text": "Sections skipped"
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
                  "text": "Background and Strategic Fit"
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
                  "text": "Goals"
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
                  "text": "Non-Functional Requirements"
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
                  "text": "Use Cases"
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
                  "text": "Customer Considerations"
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
                  "text": "Customer Information/Supportability"
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
                  "text": "Documentation Considerations"
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
          "text": "Unverified API claims"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "The following claim could not be verified (web tools unavailable) and should be checked manually before implementation:"
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
                  "text": "\"The GitHub API does not support modifying a submitted review\" (in Requirements section)"
                }
              ]
            }
          ]
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
          "text": "sdlc-workflow/define-feature",
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
