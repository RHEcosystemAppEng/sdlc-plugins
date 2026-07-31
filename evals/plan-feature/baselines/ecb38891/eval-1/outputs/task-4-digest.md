# Description Digest Comment (Jira comment on Task 4)

[sdlc-workflow] Description digest: sha256-md:<digest-would-be-computed-after-refetching-from-jira>

Note: In a live run, this digest is computed by:
1. Creating the task in Jira
2. Re-fetching the task to get the persisted description
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the tagged digest as a standalone comment (no footer)
