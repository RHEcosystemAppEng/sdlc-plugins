# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8005 is scoped to the **2.2.x stream** (suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the correction.

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (from lock file analysis) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0 is incorrect**: there is no 2.0.x version stream configured. PSIRT assigned this version based on scan time, not actual dependency analysis.
- **RHTPA 2.2.0**: ships openssl-libs 3.0.7-25.el9_3 (vulnerable; before fixed version 3.0.7-28.el9_4).
- **RHTPA 2.2.1**: ships openssl-libs 3.0.7-27.el9_4 (vulnerable; before fixed version 3.0.7-28.el9_4).
- **RHTPA 2.2.2**: retag of 2.2.1, same openssl-libs version (vulnerable).
- **RHTPA 2.2.3**: ships openssl-libs 3.0.7-28.el9_4 (fixed version) -- excluded.
- **RHTPA 2.2.4**: ships openssl-libs 3.0.7-28.el9_4 (fixed version) -- excluded.

## Jira Update

After engineer confirmation, the Affects Versions field would be updated:

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-version-id>"},
    {"id": "<RHTPA-2.2.1-version-id>"},
    {"id": "<RHTPA-2.2.2-version-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not correspond to any configured version stream and was removed.
RHTPA 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (fixed) and are excluded.
```

## Cross-Stream Note

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship openssl-libs 3.0.7-24.el9). However, since this issue is scoped to 2.2.x, those versions are not included in this issue's Affects Versions. Cross-stream impact is handled in Step 8 (Case A).
