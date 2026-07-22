# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x versions are tracked by companion/sibling issues per the stream-scoped model.

**Current Affects Versions (PSIRT-assigned):** RHTPA 2.0.0

**Proposed Affects Versions (from lock file analysis):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

PSIRT assigned `RHTPA 2.0.0` which does not correspond to any version in the 2.2.x stream's supportability matrix. The version impact analysis (Step 2) using `rpms.lock.yaml` data at pinned commits shows:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| RHTPA 2.2.0 | 3.0.7-25.el9_3 | YES -- below fix threshold 3.0.7-28.el9_4 |
| RHTPA 2.2.1 | 3.0.7-27.el9_4 | YES -- below fix threshold 3.0.7-28.el9_4 |
| RHTPA 2.2.2 | 3.0.7-27.el9_4 | YES -- retag of 2.2.1, same openssl-libs version |
| RHTPA 2.2.3 | 3.0.7-28.el9_4 | NO -- at fixed version |
| RHTPA 2.2.4 | 3.0.7-28.el9_4 | NO -- at fixed version |

## Correction

```
Current: [RHTPA 2.0.0] --> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream in the configured Version Streams. The corrected Affects Versions reflect the actual affected versions within the 2.2.x stream based on rpms.lock.yaml evidence at each pinned build tag.

Jira mutation (requires engineer confirmation):
```
jira.edit_issue(TC-8005, fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).
