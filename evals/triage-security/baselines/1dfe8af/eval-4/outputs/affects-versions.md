# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions correction includes all actually affected versions across all streams.

| | Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Proposed (lock file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **RHTPA 2.1.0**: KEEP -- h2 version 0.4.5 is vulnerable (< 0.4.8)
- **RHTPA 2.1.1**: ADD -- h2 version 0.4.5 is vulnerable (< 0.4.8), missing from PSIRT assignment
- **RHTPA 2.2.0**: REMOVE -- h2 version 0.4.8 is the fixed version (>= 0.4.8), not affected

## Rationale

The PSIRT-assigned Affects Versions are incorrect:
1. RHTPA 2.2.0 is listed but ships h2 0.4.8, which is the exact fixed version -- it is NOT affected.
2. RHTPA 2.1.1 is missing but ships h2 0.4.5, which IS affected.

The correction is based on lock file analysis at pinned commits from security-matrix.md. Since the issue is unscoped, all affected versions across all streams are included (only 2.1.x versions are actually affected).

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.1.0>"},
    {"id": "<jira-id-for-RHTPA-2.1.1>"}
  ]
})
```

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Changes:
- Removed RHTPA 2.2.0: ships h2 0.4.8 (fixed version, not affected)
- Added RHTPA 2.1.1: ships h2 0.4.5 (vulnerable, < 0.4.8)

Based on lock file analysis at pinned commits from security-matrix.md.
Issue is unscoped -- correction covers all affected versions across all streams.
Only 2.1.x stream versions are affected; 2.2.x stream ships the patched dependency.
```
