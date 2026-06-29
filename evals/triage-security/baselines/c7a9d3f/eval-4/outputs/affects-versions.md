# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), all affected versions across all streams are included in the correction.

### Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Version Impact Evidence

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** |
| RHTPA 2.1.1 | 0.4.5 | **YES** |
| RHTPA 2.2.0 | 0.4.8 | NO |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | _(retag)_ | NO |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

### Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Add**: RHTPA 2.1.1 -- lock file analysis confirms h2 0.4.5 (vulnerable, < 0.4.8)
- **Remove**: RHTPA 2.2.0 -- lock file analysis confirms h2 0.4.8 (fixed version, not vulnerable)

**Rationale**: PSIRT assigned RHTPA 2.2.0 as affected, but lock file analysis at the pinned source commit `v0.4.5` shows h2 version 0.4.8, which is the fixed version and therefore not vulnerable. PSIRT also missed RHTPA 2.1.1, which ships h2 0.4.5 (vulnerable). The correction scopes Affects Versions to only those versions that actually ship the vulnerable dependency.

### Proposed Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.1.0>"},
    {"id": "<jira-id-for-RHTPA-2.1.1>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown here are placeholders.

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- AFFECTED (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- AFFECTED (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT affected (>= 0.4.8, fixed version)

RHTPA 2.2.0 removed (not affected). RHTPA 2.1.1 added (affected but missing).
This is an unscoped issue -- all streams checked.
```
