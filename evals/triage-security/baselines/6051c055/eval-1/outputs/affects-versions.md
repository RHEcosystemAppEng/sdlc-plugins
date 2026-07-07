# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8001 is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x versions are outside this issue's scope and belong to a companion/sibling issue.

**Current Affects Versions (PSIRT-assigned):** RHTPA 2.0.0

**Proposed Affects Versions (from lock file evidence):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Correction Details

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale:** PSIRT assigned "RHTPA 2.0.0" which does not correspond to any version in the configured Version Streams (only 2.1.x and 2.2.x are configured). Lock file analysis at pinned source commits from security-matrix.md confirms:

- **RHTPA 2.2.0** (tag v0.4.5): ships quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.1** (tag v0.4.8): ships quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- AFFECTED (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): ships quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)
- **RHTPA 2.2.4** (tag v0.4.12): ships quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)

Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version (0.11.14).

### Proposed Jira Mutation

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

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3+ already ship quinn-proto 0.11.14 (fixed) and are excluded.
```
