# Step 3 -- Affects Versions Correction

## Current vs Proposed

This issue is **scoped** to stream **2.2.x** (suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but are tracked by companion/sibling issues or preemptive tasks (see Step 4 / Case A).

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect -- there is no 2.0.x version stream in the configured Version Streams table. PSIRT assigned this based on scan-time metadata, not actual dependency analysis.
- **RHTPA 2.2.0** (build v0.4.5): ships quinn-proto 0.11.9, which is within the affected range (< 0.11.14).
- **RHTPA 2.2.1** (build v0.4.8): ships quinn-proto 0.11.12, which is within the affected range (< 0.11.14).
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1, same quinn-proto version (0.11.12), within affected range.
- **RHTPA 2.2.3** (build v0.4.11): ships quinn-proto 0.11.14, which is the fixed version -- NOT affected.
- **RHTPA 2.2.4** (build v0.4.12): ships quinn-proto 0.11.14 -- NOT affected.

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

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

## Correction Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed version) and are not affected.
```
