# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped** to the 2.2.x stream (from the summary suffix
`[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the
Affects Versions correction. The 2.1.x stream versions (also affected) are outside
this issue's scope and are handled via cross-stream impact in Step 8 (Case B).

### PSIRT-assigned Affects Versions (incorrect)

| Version | Assessment |
|---------|------------|
| RHTPA 2.0.0 | WRONG -- no 2.0.x stream exists in the configured Version Streams |

### Version Impact (2.2.x stream only -- issue scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO -- at fix version |
| RHTPA 2.2.4 | 0.11.14 | NO -- at fix version |

### Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream.
The issue's `[rhtpa-2.2]` suffix indicates it tracks the 2.2.x stream. Lock file
analysis at pinned commits confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship
quinn-proto < 0.11.14 (the vulnerable range). Versions 2.2.3 and 2.2.4 ship
quinn-proto 0.11.14 (the fix version) and are NOT affected.

### Jira Update (after engineer confirmation)

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
(Step 3.1) -- not hardcoded.

### Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed) and are excluded.
```
