# Description Digest -- Task 1 (Add database indexes for search performance optimization)

Per the description digest protocol (shared/description-digest-protocol.md), after creating this task in Jira, the skill would:

1. Re-fetch the created issue from Jira to get the description as persisted by the API:
   ```
   jira.get_issue(<created-task-key>)
   ```

2. Write the description field to a temp file and compute the tagged digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
   ```
   Output format: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the API access method.

3. Post a standalone ADF comment on the created issue:
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
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

This digest comment is posted immediately after task creation, before creating issue links or other comments. It is a standalone comment, not appended to the plan summary.
