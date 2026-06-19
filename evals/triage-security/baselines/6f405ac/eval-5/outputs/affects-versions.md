# Step 3 - Affects Versions Correction: TC-8005

## Current vs Proposed Affects Versions

| | Value |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect. There is no 2.0.x version stream configured in the project, and the issue is scoped to stream 2.2.x via the summary suffix `[rhtpa-2.2]`.

Based on rpms.lock.yaml analysis at pinned commits from the supportability matrix:

- **RHTPA 2.2.0** (build v0.4.5): ships openssl-libs 3.0.7-25.el9_3, which is within the affected range (before 3.0.7-28.el9_4). **AFFECTED.**
- **RHTPA 2.2.1** (build v0.4.8): ships openssl-libs 3.0.7-27.el9_4, which is within the affected range. **AFFECTED.**
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1, same openssl-libs 3.0.7-27.el9_4. **AFFECTED.**
- **RHTPA 2.2.3** (build v0.4.11): ships openssl-libs 3.0.7-28.el9_4, which is the fixed version. **NOT AFFECTED.**
- **RHTPA 2.2.4** (build v0.4.12): ships openssl-libs 3.0.7-28.el9_4, which is the fixed version. **NOT AFFECTED.**

Only versions within the 2.2.x stream scope are included. Versions 2.1.0 and 2.1.1 (also affected) belong to the 2.1.x stream and would be tracked by a separate companion Vulnerability issue.

## Proposed Jira Update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The exact IDs are not hardcoded.

## Comment to Post

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not affected.
```
