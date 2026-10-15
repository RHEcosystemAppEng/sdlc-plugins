[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In production, this digest would be computed by:
1. Creating the task in Jira via jira.create_issue
2. Re-fetching the created issue via jira.get_issue(<created-task-key>)
3. Writing the description to /tmp/desc-<task-key>.txt
4. Running: python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
5. Posting the tagged digest as a standalone ADF comment on the created issue

The digest is computed from the Jira-persisted description (not the submitted markdown),
since Jira normalizes content during storage.
