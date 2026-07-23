# Description Digest Comment — Task 5

This comment would be posted on the created Jira task issue immediately after creation, via `jira.add_comment`.

The digest is computed by:
1. Re-fetching the task description from Jira after creation via `jira.get_issue(<task-5-key>)`
2. Writing the description to a temp file
3. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-5-key>.txt`
4. Posting the tagged digest as a standalone comment

Comment body (ADF format):
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
          "text": "[sdlc-workflow] Description digest: sha256-adf:<computed-64-char-hex-digest>"
        }
      ]
    }
  ]
}
```

Note: The actual hex digest would be computed at runtime from the Jira-persisted description content. It is not pre-computed here because Jira normalizes content during storage, so the submitted markdown and the stored ADF representation produce different hashes.
