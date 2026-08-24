# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-wrong-columns-mock.md`
**Template**: `docs/templates/security-matrix.template.md`

### Section Headings

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `### Source Pinning Method` | YES |
| `## Ecosystem Mappings` | YES |
| `## Forward Pointer` | YES |

All required sections are present.

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 | YES |
| Ecosystem Mappings | YES | YES | 1 | YES |

### Ecosystem Mappings Column Validation

**Result: MISMATCH**

Expected (from template):
```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix file):
```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

**Diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

### Warnings

> Warning: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

This is a non-repairable issue. The column names do not match the canonical template, which may cause automated lock file inspection commands to fail due to column name misresolution.

### Auto-Repairs Applied

None required. No missing Forward Pointer section or whitespace issues detected.

### Overall Validation Status: WARNING

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
