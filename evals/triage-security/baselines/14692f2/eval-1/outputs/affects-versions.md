# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in this issue's Affects Versions.

### PSIRT-Assigned (Current)

- RHTPA 2.0.0

### Lock-File-Verified (Proposed)

Based on version impact analysis from Step 2, the affected versions within the 2.2.x stream are:

- RHTPA 2.2.0 (quinn-proto 0.11.9 -- affected)
- RHTPA 2.2.1 (quinn-proto 0.11.12 -- affected)
- RHTPA 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12 -- affected)

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not exist in the Version Streams configuration (there is no 2.0.x stream). Lock file analysis at pinned commits from security-matrix.md confirms:

- RHTPA 2.2.0 (tag v0.4.5) ships quinn-proto 0.11.9 -- within affected range < 0.11.14
- RHTPA 2.2.1 (tag v0.4.8) ships quinn-proto 0.11.12 -- within affected range < 0.11.14
- RHTPA 2.2.2 (tag v0.4.9) is a retag of 2.2.1, same backend commit -- within affected range
- RHTPA 2.2.3 (tag v0.4.11) ships quinn-proto 0.11.14 -- NOT affected (fixed version)
- RHTPA 2.2.4 (tag v0.4.12) ships quinn-proto 0.11.14 -- NOT affected (fixed version)

Note: Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected but are outside this issue's stream scope. They would be tracked by a companion CVE Jira for the 2.1.x stream (see Step 4 cross-stream coordination).

### PROPOSAL: Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). These are placeholder references -- the actual IDs are resolved at execution time.

### PROPOSAL: Correction Comment

```
jira.add_comment("TC-8001", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].")
```
