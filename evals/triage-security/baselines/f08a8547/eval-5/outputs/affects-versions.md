# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8005 is scoped to the **2.2.x** stream (from suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x stream versions are affected but belong to a companion issue (see Case A cross-stream impact).

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect -- there is no 2.0.x version stream in the configured Version Streams table. Based on `rpms.lock.yaml` inspection at each pinned build tag in the 2.2.x stream's supportability matrix:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- vulnerable (before 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- vulnerable (before 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of v0.4.8 -- same as 2.2.1, vulnerable
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT vulnerable (equals fixed version)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT vulnerable (equals fixed version)

Only versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 already include the fix and should not be listed in Affects Versions.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: In production, version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The names above correspond to the Jira version prefix `RHTPA` from Security Configuration.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream -- removed.
Versions 2.2.3 and 2.2.4 already ship openssl-libs 3.0.7-28.el9_4 (fixed) -- excluded.
```
