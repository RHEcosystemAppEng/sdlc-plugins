# Affects Versions Correction -- TC-8004

## Step 3: Affects Versions Analysis

### Current PSIRT-Assigned Affects Versions

| Jira Version | In Current Affects Versions? |
|---|---|
| RHTPA 2.1.0 | YES |
| RHTPA 2.2.0 | YES |

### Evidence-Based Correction

The issue is **unscoped** (no stream suffix), so the Affects Versions field should
include all actually affected versions across all streams.

Based on the version impact analysis (lock file evidence at pinned commits from the
supportability matrix):

| Version | h2 shipped | Affected? | Should be in Affects Versions? |
|---------|------------|-----------|-------------------------------|
| RHTPA 2.1.0 | 0.4.5 | YES | **YES** |
| RHTPA 2.1.1 | 0.4.5 | YES | **YES** (currently missing) |
| RHTPA 2.2.0 | 0.4.8 | NO | **NO** (currently included incorrectly) |
| RHTPA 2.2.1 | 0.4.8 | NO | NO |
| RHTPA 2.2.2 | -- | NO | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO | NO |
| RHTPA 2.2.4 | 0.4.9 | NO | NO |

### PROPOSAL: Affects Versions Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Add** RHTPA 2.1.1 -- version 2.1.1 ships h2 0.4.5, which is within the affected
  range (< 0.4.8). PSIRT missed this version.
- **Remove** RHTPA 2.2.0 -- version 2.2.0 ships h2 0.4.8, which is the exact fixed
  version and therefore NOT affected. PSIRT incorrectly included this version.

**Rationale:** PSIRT assigned Affects Versions based on scan-time heuristics, not actual
dependency analysis. Lock file inspection at the pinned source commits confirms that
only the 2.1.x stream versions ship a vulnerable h2 version (0.4.5 < 0.4.8). All 2.2.x
versions ship h2 0.4.8 or later and are not affected.

### PROPOSAL: Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
in a live triage. The version names above are illustrative; actual mutations would use
the discovered Jira version ID values.

### PROPOSAL: Correction Comment

Post comment to TC-8004 documenting the correction:

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT affected (>= 0.4.8, ships fix version)

Scoped to affected versions only (unscoped issue -- all streams analyzed).
```
