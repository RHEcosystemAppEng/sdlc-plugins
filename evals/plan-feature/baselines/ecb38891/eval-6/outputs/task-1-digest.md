[sdlc-workflow] Description digest: sha256-md:<would-be-computed-after-jira-creation>

Note: In a live run, this digest would be computed by:
1. Creating the task in Jira
2. Re-fetching the task description from the Jira API
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the tagged digest as a standalone comment on the created issue

Since this is a file-based eval (no Jira interaction), the digest cannot be computed.
The digest comment format would be:

[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>
