[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In production, this digest is computed by:
1. Creating the task in Jira via `jira.create_issue`
2. Re-fetching the created issue via `jira.get_issue(<created-task-key>)`
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the format-tagged digest as a standalone comment

This is an eval — no Jira interaction occurs, so the digest cannot be computed from the Jira-persisted description.
