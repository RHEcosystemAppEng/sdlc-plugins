# Step 3 -- Affects Versions Correction

## Stream Scope

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). Only 2.2.x versions are included in the Affects Versions correction. The 2.1.x stream impact is handled via cross-stream notification (Step 7, Case B).

## Current vs Proposed

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (from lock file analysis) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned version **RHTPA 2.0.0** is incorrect -- there is no 2.0.x version stream in the supportability matrix, and no Jira version matching "RHTPA 2.0.0" exists in the configured version streams. Lock file analysis at pinned commits from the supportability matrix shows:

- **RHTPA 2.2.0** (tag `v0.4.5`): ships quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.1** (tag `v0.4.8`): ships quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.2** (tag `v0.4.8`, retag of 2.2.1): same as 2.2.1 -- AFFECTED
- **RHTPA 2.2.3** (tag `v0.4.11`): ships quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)
- **RHTPA 2.2.4** (tag `v0.4.12`): ships quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime (Step 3.1). Version names from the supportability matrix are used here, prefixed with the Jira version prefix "RHTPA" from Security Configuration.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
- RHTPA 2.2.2 (v0.4.8): retag of 2.2.1 (affected)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected -- fixed version)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected -- fixed version)
```
