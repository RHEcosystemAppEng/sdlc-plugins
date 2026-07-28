# Description Digest — Task 7

This digest comment would be posted on the created Jira task immediately after creation, per `shared/description-digest-protocol.md`.

## Protocol Steps

1. After creating the task in Jira, re-fetch the issue to get the persisted description.
2. Write the description to `/tmp/desc-<task-key>.txt`.
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post the digest as a standalone ADF comment.

## Comment Body

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest-computed-from-persisted-description>
```

Note: The actual hex digest would be computed from the Jira-persisted description content using `scripts/sha256-digest.py`. The format tag (`sha256-md` or `sha256-adf`) depends on the Jira access method used.
