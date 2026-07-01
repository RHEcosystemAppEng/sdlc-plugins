# Affects Versions Correction — TC-8004

## Current vs Proposed

The issue is **unscoped** (no stream suffix), so Affects Versions should include all affected versions across all streams.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **RHTPA 2.1.0**: KEEP — h2 0.4.5 is within the affected range (< 0.4.8). Correctly included by PSIRT.
- **RHTPA 2.1.1**: ADD — h2 0.4.5 is within the affected range (< 0.4.8). Missing from PSIRT assignment.
- **RHTPA 2.2.0**: REMOVE — h2 0.4.8 is at or above the fix threshold. Not affected. Incorrectly included by PSIRT.
- **RHTPA 2.2.1**: no change — not affected (h2 0.4.8), correctly excluded.
- **RHTPA 2.2.2**: no change — not affected (retag of 2.2.1), correctly excluded.
- **RHTPA 2.2.3**: no change — not affected (h2 0.4.9), correctly excluded.
- **RHTPA 2.2.4**: no change — not affected (h2 0.4.9), correctly excluded.

## Rationale

PSIRT assigned Affects Versions based on scan-time data and included RHTPA 2.2.0, which ships h2 0.4.8 (the fix version). Lock file analysis at pinned source commits confirms that only 2.1.x versions (2.1.0 and 2.1.1) ship the vulnerable h2 < 0.4.8. The 2.2.x stream ships h2 >= 0.4.8 starting from its earliest release.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Correction scoped to affected versions only, across all streams (issue is unscoped).

## Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
Removed RHTPA 2.2.0 (ships h2 0.4.8, at or above fix threshold).
Added RHTPA 2.1.1 (ships h2 0.4.5, within affected range).
Issue is unscoped — correction includes all affected versions across all streams.
```
