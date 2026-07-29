# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions correction includes all affected versions across all streams, scoped to only those versions that are actually affected based on lock file evidence.

### Comparison

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

### Changes

| Action | Version | Reason |
|--------|---------|--------|
| KEEP | RHTPA 2.1.0 | Affected -- ships h2 0.4.5 (< 0.4.8) at tag v0.3.8 |
| ADD | RHTPA 2.1.1 | Affected -- ships h2 0.4.5 (< 0.4.8) at tag v0.3.12; missing from PSIRT assignment |
| REMOVE | RHTPA 2.2.0 | Not affected -- ships h2 0.4.8 (>= 0.4.8, fixed) at tag v0.4.5 |

### Rationale

PSIRT assigned Affects Versions based on scan-time heuristics, claiming both RHTPA 2.1.0 and RHTPA 2.2.0. Lock file analysis at pinned source commits from security-matrix.md reveals:

1. **RHTPA 2.2.0 is NOT affected** -- the backend tag v0.4.5 ships h2 0.4.8, which is the exact fixed version. This version (and all later 2.2.x versions) already include the fix.

2. **RHTPA 2.1.1 IS affected but was missing** -- PSIRT listed only RHTPA 2.1.0 but not RHTPA 2.1.1. The backend tag v0.3.12 (used by 2.1.1) ships h2 0.4.5, which is within the vulnerable range.

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.1.0>"},
    {"id": "<jira-id-for-RHTPA-2.1.1>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The update removes RHTPA 2.2.0 and adds RHTPA 2.1.1.

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- not affected (>= 0.4.8)

RHTPA 2.2.0 removed (ships fixed h2 version). RHTPA 2.1.1 added (missing from PSIRT assignment).
Issue is unscoped -- correction covers all streams.
```
