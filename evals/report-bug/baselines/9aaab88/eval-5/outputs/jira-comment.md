# Jira Comment

## API Call: Add Comment

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

**Request Body**:

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
            "text": "This bug was created using "
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
