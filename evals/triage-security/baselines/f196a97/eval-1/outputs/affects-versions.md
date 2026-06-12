# Step 3 - Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Issue Stream Scope

This issue is scoped to the **2.2.x** stream (per summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream should be included in the Affects Versions for this issue.

## Version Impact (scoped to 2.2.x stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

## Analysis

The PSIRT-assigned value "RHTPA 2.0.0" is **incorrect**:
- There is no 2.0.x version stream configured in the project's Security Configuration.
- "RHTPA 2.0.0" does not correspond to any version in the supportability matrix.
- The issue summary suffix `[rhtpa-2.2]` indicates this should track the 2.2.x stream.

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (vulnerable, < 0.11.14)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (vulnerable, < 0.11.14)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships quinn-proto 0.11.12 (vulnerable, < 0.11.14)
- **RHTPA 2.2.3** -- ships quinn-proto 0.11.14 (fixed version, NOT affected)
- **RHTPA 2.2.4** -- ships quinn-proto 0.11.14 (fixed version, NOT affected)

Only affected versions within the 2.2.x stream scope are included. The 2.1.x versions (also affected) belong to a separate stream and would be tracked by a companion PSIRT issue.

## Jira Mutation (proposed)

After engineer confirmation, execute:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Comment to add:

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Version evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (vulnerable)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (vulnerable)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1, quinn-proto 0.11.12 (vulnerable)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (fixed, not affected)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (fixed, not affected)
```

## Cross-Stream Impact Note

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x only. A cross-stream impact comment should be posted (Case B) to note that 2.1.x is also affected and may require a separate PSIRT issue or companion tracker.
