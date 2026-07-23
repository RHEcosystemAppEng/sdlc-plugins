# Description Digest -- Task 4

_This is the digest comment that would be posted on the created Jira task issue immediately after creation, before creating issue links or other comments._

## Digest Comment Body

```
[sdlc-workflow] Description digest: sha256-adf:<computed-after-jira-creation>
```

## Protocol

1. After creating the task in Jira, re-fetch the issue to get the description as persisted by the API
2. Write the description to a temp file: `/tmp/desc-<task-key>.txt`
3. Compute the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the digest as a standalone ADF comment (no footnote appended)

## ADF Comment Format

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

_Note: The actual hex digest cannot be computed in this eval since no Jira API interaction occurs. In production, the digest would be computed from the Jira-persisted description content using scripts/sha256-digest.py._
