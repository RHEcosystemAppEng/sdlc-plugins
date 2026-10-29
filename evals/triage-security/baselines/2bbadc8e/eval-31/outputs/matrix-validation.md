# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Template**: `docs/templates/security-matrix.template.md`
**Matrix file**: `security-matrix.md` (Stream 1: rhtpa-release.0.4.z)

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | Present |
| `## Ecosystem Mappings` | Present |
| `### Source Pinning Method` | Present |
| `## Forward Pointer` | Present |

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | Parsable |
| Ecosystem Mappings | Yes | Yes | 1 | Parsable |

### Ecosystem Mappings Column Validation

**Result: WARNING -- column mismatch**

Expected (from template):
```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix):
```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Diff:

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

> **Warning:** Matrix file has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`
>
> 4 of 5 columns have non-matching names. Column count is correct (5), but the
> column names do not match the canonical template. This cannot be auto-repaired.
> The engineer must rename the columns to match the template or confirm the
> current names are intentional.

### Overall Validation Summary

| Check | Result |
|-------|--------|
| Required sections | Pass |
| Table parsability | Pass |
| Ecosystem Mappings columns | **Warning** -- wrong column names (4 of 5 mismatch) |

**Validation outcome: Warnings**

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
