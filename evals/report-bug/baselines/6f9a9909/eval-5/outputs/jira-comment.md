# Jira Comment

## API Call

`POST /rest/api/3/issue/TC-42/comment`

## Request Body

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

## Response

```json
{
  "id": "67890",
  "self": "https://your-domain.atlassian.net/rest/api/3/issue/12345/comment/67890"
}
```

Comment added to **TC-42** with skill attribution.
