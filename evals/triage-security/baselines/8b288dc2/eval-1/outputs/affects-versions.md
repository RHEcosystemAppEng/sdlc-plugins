# Step 3 -- Affects Versions Correction for TC-8001

## Current vs Proposed Affects Versions

The issue TC-8001 is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the correction. The 2.1.x stream versions are tracked by companion issues (see Step 4 cross-stream coordination).

### PSIRT-Assigned (Current)

- RHTPA 2.0.0

### Version Impact Evidence (Stream 2.2.x Only)

| Version | quinn-proto | Affected? | In Jira? |
|---------|-------------|-----------|----------|
| RHTPA 2.2.0 | 0.11.9 | YES | To be verified via Jira API |
| RHTPA 2.2.1 | 0.11.12 | YES | To be verified via Jira API |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES | To be verified via Jira API |
| RHTPA 2.2.3 | 0.11.14 | NO | -- |
| RHTPA 2.2.4 | 0.11.14 | NO | -- |

### Proposed Correction

**PROPOSAL** (requires engineer confirmation before execution):

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any configured version stream (no 2.0.x stream exists in Security Configuration). Lock file analysis at pinned source commits from security-matrix.md shows that quinn-proto < 0.11.14 is present in versions 2.2.0 (v0.4.5: 0.11.9), 2.2.1 (v0.4.8: 0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fix) and are NOT affected.

### Proposed Jira Mutation

```
PROPOSAL: jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are placeholders -- actual IDs must be resolved at runtime.

### Proposed Comment

```
PROPOSAL: jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  Evidence:
  - RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14)
  - RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14)
  - RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 -- affected (same source)
  - RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT affected (>= fix threshold)
  - RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT affected (>= fix threshold)

  RHTPA 2.0.0 was removed -- no 2.0.x stream exists in the configured Version Streams.")
```

### Notes

- No ProdSec Jira account ID is configured, so no @mention is included in the comment.
- The Jira version IDs must be discovered dynamically (Step 3.1) before executing the mutation.
- RHTPA 2.0.0 is not a valid version in any configured stream -- it appears PSIRT assigned an incorrect version.
