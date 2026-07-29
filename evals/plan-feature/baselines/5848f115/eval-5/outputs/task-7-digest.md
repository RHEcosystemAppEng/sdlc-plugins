[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-persistence>

Note: In a live execution, the digest would be computed by:
1. Re-fetching the created task from Jira after creation
2. Writing the description to a temp file
3. Running `python3 scripts/sha256-digest.py /tmp/desc-TC-9012.txt`
4. Posting the format-tagged digest (e.g., sha256-md:a1b2c3... or sha256-adf:a1b2c3...) as a standalone comment

This step cannot be performed in eval mode because no Jira issue is actually created.
