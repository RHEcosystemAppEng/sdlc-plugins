# Description Digest -- Task 6

*Posted as a standalone Jira comment on the created task issue immediately after creation (Step 6a)*

## Digest Comment Format

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>
```

## Computation Steps

1. After creating the task in Jira, re-fetch the issue to get the description as persisted by the API:
   `jira.get_issue(<created-task-key>)`

2. Write the description to a temp file:
   `/tmp/desc-<task-key>.txt`

3. Compute the tagged digest using the script:
   `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`

4. Post the digest as a standalone ADF comment (no footnote appended):
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest-from-step-3>"
           }
         ]
       }
     ]
   }
   ```

## Notes

- In eval mode, no Jira interaction occurs. This file documents the digest comment that would be posted.
- The digest is computed from the Jira-persisted description (re-fetched after creation), not from the markdown submitted to create_issue.
- The format tag (sha256-md or sha256-adf) depends on which Jira access method returns the description.
- This comment is posted before creating issue links or other comments on the task.
