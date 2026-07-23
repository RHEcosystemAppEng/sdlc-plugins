# Description Digest -- Task 3

Per the description digest protocol (`shared/description-digest-protocol.md`), this comment would be posted on the created Task 3 issue immediately after creation, before creating issue links or other comments.

The digest is computed by:
1. Re-fetching the task description from Jira after creation (`jira.get_issue(<task-3-key>)`)
2. Writing the description to a temp file (`/tmp/desc-<task-3-key>.txt`)
3. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-3-key>.txt`
4. Posting the tagged digest as a standalone comment

Comment body (single line):
```
[sdlc-workflow] Description digest: sha256-adf:<64-char-hex-digest-computed-at-creation-time>
```

Note: The actual hex digest cannot be computed in this eval because the description is not posted to Jira (Jira normalizes content during storage, producing a different hash than the submitted markdown). In a live run, the digest would be computed from the Jira-persisted ADF representation.
