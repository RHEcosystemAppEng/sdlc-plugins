# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions should include all actually affected versions across all streams.

| Source | Affects Versions |
|--------|-----------------|
| Current (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Proposed (lock-file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **RHTPA 2.1.0**: KEEP -- h2 0.4.5 is vulnerable (below fix threshold 0.4.8)
- **RHTPA 2.1.1**: ADD -- h2 0.4.5 is vulnerable (below fix threshold 0.4.8); missing from PSIRT assignment
- **RHTPA 2.2.0**: REMOVE -- h2 0.4.8 is at or above fix threshold; NOT affected

## Rationale

PSIRT assigned Affects Versions based on scan-time coverage, not actual dependency analysis. Lock file inspection at pinned source commits shows:

- 2.1.0 (tag v0.3.8): `Cargo.lock` contains h2 0.4.5 -- AFFECTED
- 2.1.1 (tag v0.3.12): `Cargo.lock` contains h2 0.4.5 -- AFFECTED (was missing from PSIRT assignment)
- 2.2.0 (tag v0.4.5): `Cargo.lock` contains h2 0.4.8 -- NOT AFFECTED (ships fixed version)

All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are not affected.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Correction scoped to affected versions only: RHTPA 2.1.0 and RHTPA 2.1.1.

## Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 — affected (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 — affected (< 0.4.8, was missing)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 — not affected (ships fixed version, removed)
Unscoped issue — correction covers all streams.
```
