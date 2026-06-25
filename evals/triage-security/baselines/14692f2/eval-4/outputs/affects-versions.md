# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so all affected versions across all streams should be included in Affects Versions.

Based on the version impact table, only 2.1.x versions are actually affected. The 2.2.x versions all ship h2 >= 0.4.8 and are NOT affected.

### Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Remove** RHTPA 2.2.0 -- lock file analysis shows h2 0.4.8 at tag v0.4.5, which equals the fix threshold. Version 2.2.0 is NOT affected.
- **Add** RHTPA 2.1.1 -- lock file analysis shows h2 0.4.5 at tag v0.3.12, which is below the fix threshold of 0.4.8. Version 2.1.1 IS affected but was missing from PSIRT's assignment.

### Rationale

PSIRT assigned Affects Versions based on scan-time data, not dependency analysis. Lock file inspection at pinned commits from the supportability matrix shows:

| Jira Version | h2 version | Below fix threshold (0.4.8)? | Include? |
|-------------|------------|-------------------------------|----------|
| RHTPA 2.1.0 | 0.4.5 | YES | YES (keep) |
| RHTPA 2.1.1 | 0.4.5 | YES | YES (add -- was missing) |
| RHTPA 2.2.0 | 0.4.8 | NO | NO (remove) |
| RHTPA 2.2.1 | 0.4.8 | NO | NO |
| RHTPA 2.2.2 | -- | NO (retag of 2.2.1) | NO |
| RHTPA 2.2.3 | 0.4.9 | NO | NO |
| RHTPA 2.2.4 | 0.4.9 | NO | NO |

### Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). Only versions confirmed as affected by lock file evidence are included.

### Comment (proposed)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
RHTPA 2.2.0 removed: ships h2 0.4.8 (at fix threshold).
RHTPA 2.1.1 added: ships h2 0.4.5 (below fix threshold 0.4.8).
Issue is unscoped -- correction covers all streams.
```
