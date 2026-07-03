# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8001 is scoped to stream **2.2.x** (from the summary suffix `[rhtpa-2.2]`). The Affects Versions correction is scoped to this stream only. Cross-stream impact on 2.1.x is handled separately via Case B in Step 8.

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect -- there is no 2.0.x version stream in the supportability matrix. PSIRT likely assigned this based on scan time or a placeholder value.
- **RHTPA 2.2.0** (quinn-proto 0.11.9) -- affected; version is below the fix threshold of 0.11.14.
- **RHTPA 2.2.1** (quinn-proto 0.11.12) -- affected; version is below the fix threshold of 0.11.14.
- **RHTPA 2.2.2** (retag of 2.2.1, quinn-proto 0.11.12) -- affected; same source as 2.2.1.
- **RHTPA 2.2.3** (quinn-proto 0.11.14) -- NOT affected; version meets the fix threshold.
- **RHTPA 2.2.4** (quinn-proto 0.11.14) -- NOT affected; version meets the fix threshold.

## Proposed Jira Mutation

After engineer confirmation:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-version-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-version-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-version-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The correction removes RHTPA 2.0.0 and adds the three actually affected versions in the 2.2.x stream.

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
