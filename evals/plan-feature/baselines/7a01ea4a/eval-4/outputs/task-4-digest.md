# Description Digest — Task 4

Per the description digest protocol (`shared/description-digest-protocol.md`), after creating the task in Jira, the skill would:

1. Re-fetch the created issue from Jira to get the persisted description
2. Write the description to `/tmp/desc-<task-key>.txt`
3. Compute the digest using `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post a standalone comment on the created issue:

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

This comment is posted immediately after task creation, before creating issue links or other comments. The digest is computed from the Jira-persisted description (not the submitted markdown), and the format tag (`sha256-adf` or `sha256-md`) depends on the API access method used.
