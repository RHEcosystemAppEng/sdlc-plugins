[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

Note: In production, this digest is computed by:
1. Creating the task in Jira
2. Re-fetching the created issue to get the description as persisted by Jira
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the tagged digest (e.g., `sha256-md:a1b2c3...64chars...`) as a standalone comment

This file represents the digest comment that would be posted on the created Jira task for Task 8 (Merge feature branch TC-9005 to main).
