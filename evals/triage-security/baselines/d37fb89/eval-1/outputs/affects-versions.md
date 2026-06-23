# Step 3 -- Affects Versions Correction

## Current vs Corrected Affects Versions

**Issue scope**: TC-8001 is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`).

### PSIRT-assigned Affects Versions (current)

| Version | Valid? |
|---------|--------|
| RHTPA 2.0.0 | NO -- version 2.0.0 does not exist in the supportability matrix or in any configured version stream |

### Version impact analysis (2.2.x stream only)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO -- ships fixed version |
| 2.2.4 | 0.11.14 | NO -- ships fixed version |

### Proposed correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any real product version. Lock file analysis at pinned commits from security-matrix.md confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (the vulnerable range). Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are not affected.

This correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a companion Vulnerability issue for that stream.

### Jira mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

### Comment (would post after correction)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any version in the supportability matrix.
Versions 2.2.3+ ship quinn-proto 0.11.14 (fixed) and are not affected.
```

### Cross-stream note

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected -- both ship quinn-proto 0.11.9. This is outside the scope of TC-8001 and would be tracked by a companion PSIRT issue for the 2.1.x stream.
