# Jira Comment

## API Call: Add Comment

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

### Request Payload

```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This bug was filed using "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/report-bug",
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
            "text": " v0.13.9."
          }
        ]
      }
    ]
  }
}
```
