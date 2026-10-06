# Description Digest Comment — Task 3

This comment would be posted to the created Jira task immediately after creation
via `jira.add_comment`, per the Description Digest Protocol.

## Process

1. After creating the task, re-fetch it from Jira: `jira.get_issue(<task-3-key>)`
2. Extract the `description` field and write to `/tmp/desc-<task-3-key>.txt`
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-3-key>.txt`
4. Post the digest comment (ADF format):

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
          "text": "[sdlc-workflow] Description digest: <tagged-digest-from-script>"
        }
      ]
    }
  ]
}
```

Note: The actual digest value is computed from the Jira-normalized description
(not the submitted markdown), so it cannot be pre-computed here.
