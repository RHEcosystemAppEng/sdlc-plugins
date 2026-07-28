# Description Digest Comment for Task 7

This comment would be posted on the created Jira task immediately after creation, before creating issue links or other comments.

The digest is computed by:
1. Re-fetching the created task from Jira: `jira.get_issue(<task-7-key>)`
2. Writing the description to a temp file: `/tmp/desc-<task-7-key>.txt`
3. Computing the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-7-key>.txt`
4. Posting as a standalone ADF comment:

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

Note: The actual hex digest would be computed from the Jira-persisted description content. The format tag (sha256-adf or sha256-md) depends on the Jira access method used.
