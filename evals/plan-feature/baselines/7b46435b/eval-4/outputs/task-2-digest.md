# Description Digest — Task 2

This would be posted as a standalone ADF comment on the created Task 2 issue immediately after creation.

## Process

1. After creating the task, re-fetch the issue from Jira: `jira.get_issue(<task-2-key>)`
2. Extract the `description` field and write to `/tmp/desc-<task-2-key>.txt`
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-2-key>.txt`
4. Post comment with the tagged digest

## Comment Body (ADF)

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

Note: The `<64-char-hex-digest>` is a placeholder. The actual digest would be computed from the Jira-stored description content using `scripts/sha256-digest.py`. The format tag (`sha256-md` or `sha256-adf`) depends on the Jira access method used.
