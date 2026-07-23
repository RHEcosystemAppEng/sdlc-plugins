[sdlc-workflow] Description digest: sha256-md:<computed-after-jira-creation>

---

Note: In a live execution, this digest would be computed by:
1. Creating the task in Jira via jira.create_issue()
2. Re-fetching the created issue via jira.get_issue(<created-task-key>)
3. Writing the returned description to /tmp/desc-<task-key>.txt
4. Running: python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
5. Posting the resulting tagged digest (e.g., sha256-md:a1b2c3...64chars or sha256-adf:a1b2c3...64chars) as a standalone ADF comment on the created issue

The digest comment is posted immediately after task creation, before creating issue links or other comments.
