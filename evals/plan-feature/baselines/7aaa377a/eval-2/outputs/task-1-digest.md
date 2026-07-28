# Description Digest — Task 1 (Add search performance indexes via database migration)

This comment would be posted on the created Jira task immediately after creation.

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
          "text": "[sdlc-workflow] Description digest: sha256-adf:<computed-after-refetch>"
        }
      ]
    }
  ]
}
```

## Digest Computation Steps

1. After creating the task in Jira, re-fetch the issue via `jira.get_issue(<created-task-key>)` to get the description as persisted by the API.
2. Write the fetched description to `/tmp/desc-<task-key>.txt`.
3. Run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt` to compute the format-tagged digest.
4. Post the digest comment with the computed value replacing `<computed-after-refetch>`.

Note: The digest cannot be pre-computed because Jira normalizes content during storage. The actual digest value depends on the ADF representation returned by the Jira API after creation.
