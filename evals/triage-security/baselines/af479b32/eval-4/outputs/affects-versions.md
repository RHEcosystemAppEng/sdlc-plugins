# Affects Versions Correction — TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so Affects Versions should include all affected versions across all streams.

| Source | Versions |
|--------|----------|
| PSIRT-assigned (current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Lock file evidence (proposed) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

### Changes

| Action | Version | Reason |
|--------|---------|--------|
| KEEP   | RHTPA 2.1.0 | Correctly identified as affected -- ships h2 0.4.5 (< 0.4.8) |
| ADD    | RHTPA 2.1.1 | Missing from PSIRT assignment -- ships h2 0.4.5 (< 0.4.8) |
| REMOVE | RHTPA 2.2.0 | Incorrectly included -- ships h2 0.4.8 (>= fix threshold 0.4.8, NOT affected) |

### Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits from security-matrix.md reveals:

- **RHTPA 2.1.0** (build v0.3.8): `Cargo.lock` shows h2 0.4.5 -- AFFECTED
- **RHTPA 2.1.1** (build v0.3.12): `Cargo.lock` shows h2 0.4.5 -- AFFECTED (missing from PSIRT assignment)
- **RHTPA 2.2.0** (build v0.4.5): `Cargo.lock` shows h2 0.4.8 -- NOT AFFECTED (ships the fixed version)

All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are therefore not affected.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

## Proposed Jira Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

Removed RHTPA 2.2.0: ships h2 0.4.8 (at or above fix threshold).
Added RHTPA 2.1.1: ships h2 0.4.5 (below fix threshold 0.4.8).

Issue is unscoped -- correction includes all affected versions across all streams.
Only stream 2.1.x is affected; stream 2.2.x ships the patched version.
```
