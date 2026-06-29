# Jira Comment (ADF Format)

The following comment would be posted to the newly created Feature issue using `add_comment`.

## Comment Content

**Sections included in this Feature definition:**

1. Feature Overview
2. Background and Strategic Fit
3. Goals
4. Requirements
5. Non-Functional Requirements
6. Use Cases (User Experience & Workflow)
7. Customer Considerations
8. Customer Information/Supportability
9. Documentation Considerations

All 9 template sections were provided.

---

### ADF Representation

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
          "text": "Sections included in this Feature definition:",
          "marks": [{"type": "strong"}]
        }
      ]
    },
    {
      "type": "orderedList",
      "content": [
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Feature Overview"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Background and Strategic Fit"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Goals"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Requirements"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Non-Functional Requirements"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Use Cases (User Experience & Workflow)"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Customer Considerations"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Customer Information/Supportability"}]}]
        },
        {
          "type": "listItem",
          "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Documentation Considerations"}]}]
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
          "text": "Created with "
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
          "text": " v0.11.0"
        }
      ]
    }
  ]
}
```

## Comment Footnote

> Created with [sdlc-workflow/define-feature](https://github.com/mrizzi/sdlc-plugins) v0.11.0
