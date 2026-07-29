# Jira Comment: Description Digest for Task 1

**Posted to:** (created task key for Task 1)

**Comment type:** Standalone digest comment (no footer)

## Content

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
          "text": "[sdlc-workflow] Description digest: sha256-adf:<digest-computed-after-refetch>"
        }
      ]
    }
  ]
}
```

**Note:** The actual digest value would be computed by:
1. Re-fetching the created issue from Jira to get the persisted description
2. Writing the description to `/tmp/desc-<task-key>.txt`
3. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Using the format-tagged output (e.g., `sha256-adf:a1b2c3...`) in the comment
