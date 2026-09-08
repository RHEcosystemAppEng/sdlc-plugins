# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since this issue is **unscoped** (no stream suffix), the Affects Versions field should include all affected versions across all streams -- but only those actually affected per lock file evidence.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

### Versions to ADD

| Version | Reason |
|---------|--------|
| RHTPA 2.1.1 | Ships h2 0.4.5 (vulnerable, < 0.4.8) -- missing from PSIRT assignment |

### Versions to REMOVE

| Version | Reason |
|---------|--------|
| RHTPA 2.2.0 | Ships h2 0.4.8 (fixed version) -- NOT affected |

### Versions to KEEP

| Version | Reason |
|---------|--------|
| RHTPA 2.1.0 | Ships h2 0.4.5 (vulnerable, < 0.4.8) -- correctly assigned by PSIRT |

## Rationale

PSIRT assigned Affects Versions based on scan time and component presence, not actual dependency version analysis. Lock file inspection at pinned source commits reveals:

- **RHTPA 2.1.0** (tag v0.3.8): `Cargo.lock` contains h2 0.4.5 -- VULNERABLE (correct)
- **RHTPA 2.1.1** (tag v0.3.12): `Cargo.lock` contains h2 0.4.5 -- VULNERABLE (missing from PSIRT assignment)
- **RHTPA 2.2.0** (tag v0.4.5): `Cargo.lock` contains h2 0.4.8 -- NOT AFFECTED (incorrectly assigned by PSIRT)

All 2.2.x versions ship h2 >= 0.4.8 and are not affected. The corrected Affects Versions should be scoped to the actually affected versions only: RHTPA 2.1.0 and RHTPA 2.1.1.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Comment to post after correction:

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

- RHTPA 2.2.0 removed: ships h2 0.4.8 (fixed version, not affected)
- RHTPA 2.1.1 added: ships h2 0.4.5 (vulnerable, < 0.4.8)

This issue is unscoped (no stream suffix) -- Affects Versions covers all affected versions across all streams.
```
