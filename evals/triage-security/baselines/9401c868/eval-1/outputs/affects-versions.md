# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the correction. The 2.1.x versions (also affected) belong to a companion/sibling issue scope.

| Field | Value |
|-------|-------|
| Current Affects Versions | RHTPA 2.0.0 |
| Proposed Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

**PSIRT version is wrong**: `RHTPA 2.0.0` does not correspond to any version in the supportability matrix. No 2.0.x stream exists in the configured Version Streams.

Based on lock file analysis at pinned commits from security-matrix.md, the affected versions within the 2.2.x stream are:

| Version | quinn-proto | Affected? | Included in Affects Versions? |
|---------|-------------|-----------|-------------------------------|
| RHTPA 2.2.0 | 0.11.9 | YES | YES (add) |
| RHTPA 2.2.1 | 0.11.12 | YES | YES (add) |
| RHTPA 2.2.2 | retag of 2.2.1 | YES | YES (add) |
| RHTPA 2.2.3 | 0.11.14 | NO | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO | NO (fixed) |

**Correction diff**: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

## Proposed Jira Mutation

After engineer confirmation:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be resolved dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any version in the supportability matrix.
Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, at or above
the fix threshold).
```
