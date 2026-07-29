# Description Digest -- Task 3 (Optimize search query performance and add response caching)

This file represents the digest comment that would be posted on the created Jira task
immediately after creation, per the Description Digest Protocol.

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
          "text": "[sdlc-workflow] Description digest: sha256-md:<computed-after-refetch>"
        }
      ]
    }
  ]
}
```

## Digest Computation Steps

1. After creating the task issue via `jira.create_issue`, re-fetch the issue using
   `jira.get_issue(<created-task-key>)` to get the description as persisted by Jira.
2. Write the fetched description to `/tmp/desc-<task-key>.txt`.
3. Compute the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the digest comment as a standalone ADF comment on the created issue.

Note: The actual hex digest cannot be computed in eval mode because the description
is not persisted to Jira. In production, the script auto-detects the format (ADF or
markdown) and outputs `sha256-adf:<64-char-hex>` or `sha256-md:<64-char-hex>`.
