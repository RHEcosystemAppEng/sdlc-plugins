[sdlc-workflow] Description digest: sha256-md:<computed-from-jira-persisted-description>

Note: In production, this digest would be computed by:
1. Creating the task in Jira
2. Re-fetching the created issue to get the Jira-persisted description
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-TC-XXXX.txt`
5. Posting the full tagged digest (e.g., `sha256-md:a1b2c3...64chars...`) as a standalone comment
