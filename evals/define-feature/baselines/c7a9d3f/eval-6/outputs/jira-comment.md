# Jira Comment

## API Call

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

## Comment Body

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
            "text": "This Feature was defined with the assistance of "
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

## Footnote

> This Feature was defined with the assistance of [sdlc-workflow/define-feature](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
