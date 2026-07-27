[sdlc-workflow] Description digest: sha256-md:<placeholder-digest-for-task-3>

Note: In a live execution, this digest would be computed by:
1. Creating the task in Jira
2. Re-fetching the task description from Jira API
3. Writing the description to a temp file
4. Running: python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
5. Posting the resulting tagged digest as a standalone comment

Since we are writing to files instead of Jira, the actual SHA-256 digest cannot be computed.
The digest comment would be posted as a standalone ADF comment on each created task issue
immediately after creation, before creating issue links or other comments.
