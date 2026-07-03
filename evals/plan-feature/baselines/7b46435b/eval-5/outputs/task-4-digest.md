# Description Digest — Task 4 (Update advisory model structs for direct enum status)

This file represents the digest comment that would be posted to the created Jira task immediately after creation, per the description-digest-protocol.

## Digest Comment (ADF)

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

## Protocol Notes

1. After creating the task in Jira, re-fetch the issue to get the description as persisted by the API.
2. Compute the tagged digest using `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`.
3. Post the digest as a standalone ADF comment (no footer appended).
