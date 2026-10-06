# Description Digest Comment (posted to created task for Task 3)

This comment would be posted immediately after creating the task in Jira,
before creating issue links or other comments.

## Comment Format (ADF)

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
          "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
        }
      ]
    }
  ]
}
```

## Computation Steps

1. After creating the task in Jira, re-fetch the issue to get the description as persisted by the API
2. Write the fetched description to a temp file (`/tmp/desc-<task-key>.txt`)
3. Compute the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the digest comment with the full output (e.g., `sha256-md:a1b2c3...` — 64 hex chars)

The digest is computed from the Jira-persisted description (not the submitted markdown),
because Jira normalizes content during storage.
