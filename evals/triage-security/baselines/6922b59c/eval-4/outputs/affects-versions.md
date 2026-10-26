# Affects Versions Correction -- TC-8004

## Step 3: Affects Versions Analysis

### Current PSIRT-Assigned Affects Versions

- RHTPA 2.1.0
- RHTPA 2.2.0

### Lock File Evidence

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | YES (< 0.4.8) |
| RHTPA 2.1.1 | 0.4.5 | YES (< 0.4.8) |
| RHTPA 2.2.0 | 0.4.8 | NO (>= 0.4.8) |
| RHTPA 2.2.1 | 0.4.8 | NO (>= 0.4.8) |
| RHTPA 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO (>= 0.4.8) |
| RHTPA 2.2.4 | 0.4.9 | NO (>= 0.4.8) |

### Correction Required

The issue is **unscoped** (no stream suffix), so all affected versions across all streams are included.

**PSIRT Affects Versions are incorrect:**
- **RHTPA 2.2.0 is NOT affected** -- it ships h2 0.4.8 which is the fixed version. Remove.
- **RHTPA 2.1.1 IS affected** -- it ships h2 0.4.5 which is within the vulnerable range. Add.

### Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

Changes:
- **Remove**: RHTPA 2.2.0 (ships h2 0.4.8 -- not affected)
- **Add**: RHTPA 2.1.1 (ships h2 0.4.5 -- affected)
- **Keep**: RHTPA 2.1.0 (ships h2 0.4.5 -- affected)

### Rationale

Based on lock file analysis at pinned commits from security-matrix.md:
- All 2.1.x versions (2.1.0 via v0.3.8, 2.1.1 via v0.3.12) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- All 2.2.x versions (2.2.0 via v0.4.5 onward) ship h2 >= 0.4.8, which is at or above the fix threshold.

The Affects Versions field should contain only versions that actually ship the vulnerable dependency. Scoped to affected versions only per lock file evidence.

### Jira Mutation (not executed)

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

Evidence:
- 2.1.0 (v0.3.8): h2 = 0.4.5 (vulnerable, < 0.4.8)
- 2.1.1 (v0.3.12): h2 = 0.4.5 (vulnerable, < 0.4.8)
- 2.2.0 (v0.4.5): h2 = 0.4.8 (not affected, >= 0.4.8)

RHTPA 2.2.0 removed -- ships h2 0.4.8 (fixed version).
RHTPA 2.1.1 added -- ships h2 0.4.5 (vulnerable).
```
