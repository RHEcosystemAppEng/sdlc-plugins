# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so Affects Versions should include
all affected versions across all streams -- scoped to affected versions only.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **Remove**: RHTPA 2.2.0 -- version 2.2.0 ships h2 0.4.8 which is the fixed version; NOT affected
- **Add**: RHTPA 2.1.1 -- version 2.1.1 ships h2 0.4.5 which is within the vulnerable range (< 0.4.8); AFFECTED
- **Keep**: RHTPA 2.1.0 -- version 2.1.0 ships h2 0.4.5 which is within the vulnerable range (< 0.4.8); AFFECTED

## Rationale

PSIRT assigned Affects Versions based on scan time, listing RHTPA 2.1.0 and RHTPA 2.2.0.
Lock file analysis at the pinned commits from the supportability matrix shows:

- Stream 2.1.x: ALL versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable (< 0.4.8)
- Stream 2.2.x: ALL versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is the fixed version

PSIRT missed 2.1.1 (affected but not listed) and incorrectly included 2.2.0 (not affected).

## Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Comment to post:
```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

- Removed RHTPA 2.2.0: ships h2 0.4.8 (fixed version, not affected)
- Added RHTPA 2.1.1: ships h2 0.4.5 (vulnerable, < 0.4.8)

This issue is unscoped -- correction covers all affected versions across all streams.
```
