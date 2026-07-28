# Description Digest — Task 1

This file represents the description digest comment that would be posted on the created Jira task immediately after creation, per the description-digest-protocol.

## Digest Comment (ADF format)

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "[sdlc-workflow] Description digest: sha256-adf:<computed-after-jira-creation>"
        }
      ]
    }
  ]
}
```

## Protocol Notes

- The digest would be computed by re-fetching the task description from Jira after creation (not from the submitted markdown)
- The script `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt` auto-detects format and outputs a tagged digest
- The digest comment is posted as a standalone comment, separate from any other comments
- No Comment Footnote is appended to digest comments
