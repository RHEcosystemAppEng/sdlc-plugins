# Jira Comment: Traceability

## API Call: Add Comment

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

**Request Body**:

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
            "text": "This bug was reported using "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/report-bug",
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
}
```
