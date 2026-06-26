# Jira Comment — ADF Structure

The following comment would be posted to the created Feature issue using `mcp__jira__add_comment`.

## Comment Footnote (ADF)

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
```

## Rendered Text

> This Feature was defined with the assistance of [sdlc-workflow/define-feature](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
