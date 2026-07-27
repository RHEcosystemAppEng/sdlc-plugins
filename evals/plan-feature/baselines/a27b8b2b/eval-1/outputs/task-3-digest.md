# Description Digest — Task 3

Per the description digest protocol, after creating the task in Jira, the skill would:

1. Re-fetch the task from Jira to get the persisted description
2. Write the description to `/tmp/desc-TC-XXXX.txt`
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-XXXX.txt`
4. Post a standalone comment:

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>
```

The digest would be computed from the Jira-persisted description (not the submitted markdown), using the `scripts/sha256-digest.py` script which auto-detects the format and produces a tagged digest (e.g., `sha256-md:...` for markdown or `sha256-adf:...` for ADF JSON).

This comment is posted as a standalone ADF comment, separate from any other comments, immediately after task creation and before creating issue links.
