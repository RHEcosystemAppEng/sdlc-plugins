# Description Digest Comment (posted on Task 5 after creation)

This comment would be posted immediately after creating Task 5 in Jira.

## Process

1. After creating the task, re-fetch the issue from Jira to get the description as persisted by the API.
2. Write the fetched description to a temp file (e.g., `/tmp/desc-TASK-KEY.txt`).
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/desc-TASK-KEY.txt`
4. Post the digest comment as a standalone ADF comment.

## Comment Body

```
[sdlc-workflow] Description digest: sha256-adf:<64-char-hex-digest-computed-from-persisted-description>
```

Note: The actual hex digest cannot be computed in this eval because the description is not persisted to Jira. In a live run, the script auto-detects the format (ADF JSON from REST API or markdown from MCP) and outputs the appropriate tagged digest (sha256-adf:... or sha256-md:...).
