# Step 3 -- Affects Versions Correction

## Current State

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Evidence (scoped to 2.2.x stream)

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES |
| RHTPA 2.2.1 | YES |
| RHTPA 2.2.2 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | NO (ships fixed 3.0.7-28.el9_4) |
| RHTPA 2.2.4 | NO (ships fixed 3.0.7-28.el9_4) |

## Proposed Correction

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream in the configured Version Streams, and the issue is scoped to the 2.2.x stream.

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Lock file analysis at pinned commits from the 2.2.x supportability matrix shows that versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs versions older than the fixed version 3.0.7-28.el9_4:
- 2.2.0 ships 3.0.7-25.el9_3
- 2.2.1 ships 3.0.7-27.el9_4
- 2.2.2 is a retag of 2.2.1 (same openssl-libs version)

Versions 2.2.3 and 2.2.4 are not affected -- they already ship the fixed version 3.0.7-28.el9_4.

## Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are placeholders -- actual IDs must be resolved at runtime.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
