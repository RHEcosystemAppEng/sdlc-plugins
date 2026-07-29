# Description Digest -- Task 6

This digest comment would be posted on the created Jira task immediately after creation per the description-digest-protocol.

## Digest Comment

[sdlc-workflow] Description digest: sha256-md:<hash-computed-after-jira-roundtrip>

### Digest Computation Process

1. After creating the task in Jira, re-fetch it using jira.get_issue(<created-task-key>)
2. Extract the description field from the response (as persisted by Jira, not the submitted markdown)
3. Write the description to /tmp/desc-<task-key>.txt
4. Run: python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt
5. Post the format-tagged digest as a standalone ADF comment (no footer appended)

Note: The actual hash value cannot be computed without a Jira roundtrip. In production, the digest would be computed from the Jira-persisted description after API normalization.
