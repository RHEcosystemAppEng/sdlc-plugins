# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8001 is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).
Only versions belonging to the 2.2.x stream are included in the Affects Versions
correction. The 2.1.x stream versions (2.1.0, 2.1.1) are affected but belong to
a sibling issue's scope.

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0 is incorrect**: There is no 2.0.x version stream configured. PSIRT
  likely assigned this version based on scan time or a default value, not actual
  dependency analysis.
- **RHTPA 2.2.0**: quinn-proto 0.11.9 at tag v0.4.5 -- vulnerable (< 0.11.14)
- **RHTPA 2.2.1**: quinn-proto 0.11.12 at tag v0.4.8 -- vulnerable (< 0.11.14)
- **RHTPA 2.2.2**: retag of 2.2.1 (v0.4.9 = v0.4.8) -- vulnerable (same as 2.2.1)
- **RHTPA 2.2.3**: quinn-proto 0.11.14 at tag v0.4.11 -- NOT affected (fixed version)
- **RHTPA 2.2.4**: quinn-proto 0.11.14 at tag v0.4.12 -- NOT affected (fixed version)

## Proposed Jira Update

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

(Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
at runtime -- not hardcoded.)

## Correction Comment

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  - RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected
  - RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected
  - RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 -- affected
  - RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- not affected (fixed)
  - RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- not affected (fixed)")
```

## Cross-Stream Impact Note

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9),
but those versions are outside this issue's scope. Cross-stream impact is handled
in Step 8 (Case A).
