[sdlc-workflow] Description digest: sha256-md:<would-be-computed-after-jira-creation>

Note: In a live run, this digest is computed by:
1. Creating the task in Jira
2. Re-fetching the created issue to get the persisted description
3. Writing the description to a temp file
4. Running `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
5. Posting the tagged digest as a standalone comment

The digest cannot be pre-computed because Jira normalizes content during storage.
The format tag (sha256-md or sha256-adf) depends on the Jira access method used.

additional_fields applied to this task:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
