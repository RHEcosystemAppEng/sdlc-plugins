# Step 3 -- Affects Versions Correction

## Current State

- **Issue**: TC-8001
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0

## Version Impact (scoped to 2.2.x)

The version impact table from Step 2 shows the following affected versions in the 2.2.x stream:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0   | 0.11.9      | **YES**   |
| 2.2.1   | 0.11.12     | **YES**   |
| 2.2.2   | -- (retag)  | **YES**   |
| 2.2.3   | 0.11.14     | NO        |
| 2.2.4   | 0.11.14     | NO        |

Since the issue is scoped to stream 2.2.x, only 2.2.x versions are included in the Affects Versions correction. Versions 2.1.0 and 2.1.1 (stream 2.1.x) are affected but belong to a sibling issue (see Case A cross-stream analysis in Step 8).

## Proposed Correction

**PROPOSAL** (no Jira operations performed):

The PSIRT-assigned Affects Versions value "RHTPA 2.0.0" is incorrect. There is no 2.0.x stream in the configured Version Streams -- the product has streams 2.1.x and 2.2.x. Based on lock file analysis at pinned commits from the supportability matrix, the correct Affects Versions for this 2.2.x-scoped issue are:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions 0.11.9, 0.11.12, and 0.11.12 respectively, all of which are below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are excluded.

The correction would be applied via:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). No hardcoded version IDs are used.

A correction comment would be posted documenting the change:

> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
