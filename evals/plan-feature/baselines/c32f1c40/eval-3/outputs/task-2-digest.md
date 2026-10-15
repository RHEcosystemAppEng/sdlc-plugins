[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In the live workflow, this digest is computed by:
1. Creating the task in Jira via jira.create_issue
2. Re-fetching the created issue via jira.get_issue to get the description as persisted by the API
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt` to compute the format-tagged digest
5. Posting the digest as a standalone ADF comment on the created issue

The digest comment is posted immediately after task creation, before creating issue links or other comments.
