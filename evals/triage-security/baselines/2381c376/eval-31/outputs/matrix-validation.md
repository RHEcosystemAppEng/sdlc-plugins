# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | Present |
| `### Source Pinning Method` | Present |
| `## Ecosystem Mappings` | Present |
| `## Forward Pointer` | Present |

All required sections are present.

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | Parsable |
| Ecosystem Mappings | Yes | Yes | 1 | Parsable |

### Ecosystem Mappings Column Validation

**Result: MISMATCH**

Expected (from `docs/templates/security-matrix.template.md`):

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from stream 2.2.x matrix):

```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Column diff:

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | No |
| 3 | Lock File | Lock File Path | No |
| 4 | Check Command | Command | No |
| 5 | Upstream Branch | Branch | No |

### Validation Summary

**Status: WARNING (cannot auto-repair)**

> Matrix file for stream **2.2.x** has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
