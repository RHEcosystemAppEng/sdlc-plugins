# Jira Comment: Footnote

## API Call: Add Comment

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

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
            "text": "This issue was created using "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/define-feature",
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
