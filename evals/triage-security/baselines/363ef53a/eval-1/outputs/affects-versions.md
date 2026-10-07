# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8001 is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`).
Only versions belonging to the 2.2.x stream are included in the correction.
The 2.1.x versions (2.1.0, 2.1.1) are tracked by companion/sibling issues
for the 2.1.x stream.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect -- there is no 2.0.x stream in the Version Streams
  configuration, and no version `RHTPA 2.0.0` corresponds to an actual supported
  release. PSIRT likely assigned this based on the component label rather than
  lock file analysis.
- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9, which is within the affected range
  (< 0.11.14). Source tag: `v0.4.5`.
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12, which is within the affected range
  (< 0.11.14). Source tag: `v0.4.8`.
- **RHTPA 2.2.2** -- retag of 2.2.1 (same source commit `v0.4.8`), so same
  quinn-proto version 0.11.12. Within the affected range.
- **RHTPA 2.2.3** -- ships quinn-proto 0.11.14, which is the fixed version. NOT
  affected.
- **RHTPA 2.2.4** -- ships quinn-proto 0.11.14. NOT affected.

## Proposed Jira mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(Step 3.1).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
- RHTPA 2.2.2 (v0.4.8 retag): quinn-proto 0.11.12 (affected)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (NOT affected -- fixed version)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (NOT affected -- fixed version)
```
