# Description Digest — Task 7: Update internal architecture documentation for advisory status enum migration

Per the description digest protocol (`shared/description-digest-protocol.md`), this comment would be posted on the created Jira task immediately after creation, before creating issue links or other comments.

## Digest Computation

1. Re-fetch the task description from Jira after creation to get the API-normalized content
2. Write the description to `/tmp/desc-<task-key>.txt`
3. Compute the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the digest comment

## Comment Content (ADF format)

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
          "text": "[sdlc-workflow] Description digest: sha256-adf:<64-char-hex-digest>"
        }
      ]
    }
  ]
}
```

Note: The `<64-char-hex-digest>` placeholder would be replaced with the actual SHA-256 hash computed from the Jira-normalized description content.
