# Step 3 -- Affects Versions Correction: TC-8001

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Issue Stream Scope

This issue is scoped to **stream 2.2.x** (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction.

## Version Impact (scoped to 2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | -- (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

## Proposed Correction

**PSIRT version is wrong**: RHTPA 2.0.0 does not correspond to any configured version stream (no 2.0.x stream exists). The issue's stream suffix `[rhtpa-2.2]` maps to stream 2.2.x.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: Lock file analysis at pinned source commits from security-matrix.md shows:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- vulnerable (< 0.11.14)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- vulnerable (< 0.11.14)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1, same as 2.2.1 -- vulnerable
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT vulnerable (>= 0.11.14)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT vulnerable (>= 0.11.14)

RHTPA 2.0.0 is removed because no 2.0.x stream exists in the Version Streams configuration. The version impact analysis shows it was incorrectly assigned by PSIRT.

## Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are placeholders.

## Proposed Jira Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 was removed -- no 2.0.x stream exists in the supportability matrix.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.
```

## Cross-Stream Note

Stream 2.1.x versions (2.1.0, 2.1.1) are also affected (quinn-proto 0.11.9) but belong to a different stream. They are NOT included in this issue's Affects Versions because the issue is scoped to 2.2.x. Cross-stream impact is handled in Step 7 (Case B).
