# Affects Versions Correction -- TC-8004

## Current vs Corrected Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Corrected (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

**Changes required:**

| Action | Version | Reason |
|--------|---------|--------|
| KEEP | RHTPA 2.1.0 | Affected -- ships h2 0.4.5 (< 0.4.8) |
| ADD | RHTPA 2.1.1 | Affected -- ships h2 0.4.5 (< 0.4.8); missing from PSIRT assignment |
| REMOVE | RHTPA 2.2.0 | Not affected -- ships h2 0.4.8 (>= 0.4.8, the fixed version) |

## Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits reveals:

- **RHTPA 2.1.0** (tag v0.3.8): `Cargo.lock` contains h2 0.4.5 -- within the vulnerable range (< 0.4.8). Correctly assigned by PSIRT.
- **RHTPA 2.1.1** (tag v0.3.12): `Cargo.lock` contains h2 0.4.5 -- within the vulnerable range. **Missing from PSIRT assignment** -- must be added.
- **RHTPA 2.2.0** (tag v0.4.5): `Cargo.lock` contains h2 0.4.8 -- at the fixed version (>= 0.4.8). **Incorrectly assigned by PSIRT** -- must be removed.

## Scope

This issue is **unscoped** (no stream suffix). The Affects Versions correction includes all affected versions across all streams, scoped to only those versions where the vulnerable dependency is actually present:

- 2.1.x stream: RHTPA 2.1.0, RHTPA 2.1.1 (both affected)
- 2.2.x stream: no versions affected (all ship h2 >= 0.4.8)

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

## Correction Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- AFFECTED
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- AFFECTED (added)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT AFFECTED (removed, ships fixed version)

Issue is unscoped -- correction covers all streams.
```
