[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-persistence>

Note: In a live execution, this digest would be computed by:
1. Creating the task in Jira via jira.create_issue
2. Re-fetching the task via jira.get_issue(<created-key>) to get the persisted description
3. Writing the description to /tmp/desc-<task-key>.txt
4. Running: python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
5. Posting the tagged digest (e.g., sha256-md:a1b2c3... or sha256-adf:a1b2c3...) as a standalone comment

The digest comment is posted as a standalone ADF comment immediately after task creation, before creating issue links or other comments.
