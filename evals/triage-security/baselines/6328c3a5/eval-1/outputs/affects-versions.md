# Step 3 -- Affects Versions Correction

## Stream Scope

TC-8001 is scoped to the **2.2.x** stream (summary suffix `[rhtpa-2.2]`). Per Step 3.2, only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x versions are tracked by a separate sibling issue (or will require one).

## Current vs. Proposed Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

### Correction rationale

The PSIRT-assigned version **RHTPA 2.0.0** does not correspond to any version in the supportability matrix or any configured version stream. There is no 2.0.x stream in the Version Streams table.

Based on lock file analysis at pinned source commits from the supportability matrix:

- **RHTPA 2.2.0** (build v0.4.5): quinn-proto 0.11.9 -- **affected** (< 0.11.14)
- **RHTPA 2.2.1** (build v0.4.8): quinn-proto 0.11.12 -- **affected** (< 0.11.14)
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1 -- **affected** (same as 2.2.1)
- **RHTPA 2.2.3** (build v0.4.11): quinn-proto 0.11.14 -- **not affected** (>= 0.11.14)
- **RHTPA 2.2.4** (build v0.4.12): quinn-proto 0.11.14 -- **not affected** (>= 0.11.14)

Only affected versions within the issue's scoped stream (2.2.x) are included.

## Proposed Jira Update

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1), not hardcoded.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not match any configured version stream. The actual affected
versions in the 2.2.x stream are 2.2.0 through 2.2.2, which ship quinn-proto
0.11.9 or 0.11.12 (both below the fix threshold of 0.11.14).

Versions 2.2.3+ ship quinn-proto 0.11.14 and are NOT affected.
```

No Jira operations were performed (eval-only mode).
