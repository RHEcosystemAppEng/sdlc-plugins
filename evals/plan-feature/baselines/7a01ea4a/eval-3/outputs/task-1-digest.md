# Description Digest Comment (posted on Task 1 after creation)

[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In a real execution, this digest would be computed by:
1. Creating the task in Jira via jira.create_issue
2. Re-fetching the created task via jira.get_issue to get the persisted description
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the resulting tagged digest as a standalone comment

The digest is computed from the Jira-persisted description, not the submitted markdown,
because Jira normalizes content during storage.
