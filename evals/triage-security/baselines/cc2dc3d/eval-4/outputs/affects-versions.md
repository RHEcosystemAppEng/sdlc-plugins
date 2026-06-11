# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so Affects Versions should include all affected versions across all streams.

### Current (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Version Impact Evidence

| Version | Affected? | Evidence |
|---------|-----------|----------|
| RHTPA 2.1.0 | YES | h2 0.4.5 at v0.3.8 -- vulnerable (< 0.4.8) |
| RHTPA 2.1.1 | YES | h2 0.4.5 at v0.3.12 -- vulnerable (< 0.4.8) |
| RHTPA 2.2.0 | NO | h2 0.4.8 at v0.4.5 -- fixed version |
| RHTPA 2.2.1 | NO | h2 0.4.8 at v0.4.8 -- fixed version |
| RHTPA 2.2.2 | NO | retag of 2.2.1 -- same as 2.2.1 |
| RHTPA 2.2.3 | NO | h2 0.4.9 at v0.4.11 -- above fixed version |
| RHTPA 2.2.4 | NO | h2 0.4.9 at v0.4.12 -- above fixed version |

### Proposed Correction

```
Current: [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Add** RHTPA 2.1.1 -- lock file confirms h2 0.4.5 (vulnerable)
- **Remove** RHTPA 2.2.0 -- lock file confirms h2 0.4.8 (fixed version, not affected)

### Rationale

PSIRT assigned Affects Versions based on scan time, not dependency analysis. Lock file inspection at the pinned source commits from the supportability matrix shows:

1. RHTPA 2.1.0 and RHTPA 2.1.1 both ship h2 0.4.5 (vulnerable -- before the 0.4.8 fix)
2. RHTPA 2.2.0 ships h2 0.4.8 (the exact fixed version -- NOT affected)
3. All subsequent 2.2.x versions ship h2 >= 0.4.8 (NOT affected)

The correction scopes Affects Versions to only the actually-affected versions.

### Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.1.0>"},
    {"id": "<jira-id-for-RHTPA-2.1.1>"}
  ]
})
```

Note: Jira version IDs should be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs above are placeholders.

### Proposed Comment (requires engineer confirmation)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

Evidence:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- AFFECTED (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- AFFECTED (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT AFFECTED (>= 0.4.8)

Removed RHTPA 2.2.0 (ships patched h2 0.4.8). Added RHTPA 2.1.1 (ships vulnerable h2 0.4.5).
This issue is unscoped -- analysis covers all streams.
```
