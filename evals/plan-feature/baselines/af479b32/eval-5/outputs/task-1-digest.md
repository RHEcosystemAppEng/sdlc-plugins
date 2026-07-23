# Description Digest — Task 1: Create feature branch TC-9005 from main

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

Note: The `<64-char-hex-digest>` placeholder would be replaced with the actual SHA-256 hash computed from the Jira-normalized description content. The format tag (`sha256-adf` or `sha256-md`) depends on whether the description was fetched via REST API (ADF) or MCP (markdown).
