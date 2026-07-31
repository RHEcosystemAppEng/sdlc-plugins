# Description Digest — Task 2 (would be posted as Jira comment on created task)

Per the description digest protocol, after creating the task in Jira:

1. Re-fetch the created task from Jira to get the description as persisted by the API
2. Write the description to `/tmp/desc-<task-key>.txt`
3. Compute the tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the following comment on the created task issue:

```
[sdlc-workflow] Description digest: sha256-adf:<64-char-hex-digest>
```

(The actual hex digest would be computed from the Jira-persisted description content using the sha256-digest.py script. The format tag depends on the Jira access method used: `sha256-adf` for REST API, `sha256-md` for MCP.)

This is a standalone comment — no footnote appended.
