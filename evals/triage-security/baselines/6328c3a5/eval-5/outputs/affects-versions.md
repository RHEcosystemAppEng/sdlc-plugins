# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction.

### Version Impact (2.2.x stream only)

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned `RHTPA 2.0.0` which does not correspond to any configured version stream (no 2.0.x stream exists). Based on rpms.lock.yaml analysis at pinned commits from the supportability matrix, the affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (all shipping openssl-libs < 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 ship the fixed version and are excluded.

The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a different stream and are tracked by companion issue(s) per Step 4 cross-stream coordination.

### Jira Update

After engineer confirmation, update:

```
jira.edit_issue(TC-8005, fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). Correction comment with rpms.lock.yaml evidence and scoping rationale would be posted to the issue.
