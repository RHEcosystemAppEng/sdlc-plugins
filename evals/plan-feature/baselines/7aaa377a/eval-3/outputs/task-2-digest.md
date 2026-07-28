[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In production, this digest is computed by:
1. Creating the task in Jira via jira.create_issue
2. Re-fetching the created issue via jira.get_issue to get the persisted description
3. Writing the description to a temp file
4. Running: python3 scripts/sha256-digest.py /tmp/desc-TC-XXXX.txt
5. Posting the tagged digest (e.g., sha256-md:a1b2c3... or sha256-adf:a1b2c3...) as a standalone comment
