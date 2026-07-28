# Jira Comment: Attribution

## API Call: Add Comment

**Endpoint**: `/rest/api/3/issue/{issueKey}/comment`
**Method**: POST

### Request Body

```json
{
  "body": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This Feature was defined using the "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/define-feature",
            "marks": [{ "type": "strong" }]
          },
          {
            "type": "text",
            "text": " skill (v0.13.7) from the "
          },
          {
            "type": "text",
            "text": "SDLC Workflow Plugin",
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
            "text": "."
          }
        ]
      }
    ]
  }
}
```
