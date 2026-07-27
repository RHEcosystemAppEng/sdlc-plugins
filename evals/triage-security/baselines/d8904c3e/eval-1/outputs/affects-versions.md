# Step 3 -- Affects Versions Correction

## Stream Scope

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).
Only versions belonging to the 2.2.x stream are included in the Affects Versions correction.
The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a sibling issue's scope.

## Current vs Proposed Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (from lock file analysis)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x version stream configured in the project's Security Configuration. The Version Streams table only defines 2.1.x and 2.2.x streams.

Based on lock file analysis at pinned commits from security-matrix.md, the affected 2.2.x versions are:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES -- below fix threshold 0.11.14 |
| RHTPA 2.2.1 | 0.11.12 | YES -- below fix threshold 0.11.14 |
| RHTPA 2.2.2 | 0.11.12 | YES -- retag of 2.2.1, same quinn-proto version |
| RHTPA 2.2.3 | 0.11.14 | NO -- at fixed version |
| RHTPA 2.2.4 | 0.11.14 | NO -- at fixed version |

## Jira Update

After engineer confirmation, the Affects Versions field would be updated:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs are discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1), not hardcoded.

## Comment

A correction comment would be posted to TC-8001:

> Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
