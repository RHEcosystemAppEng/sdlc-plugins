# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Template**: `docs/templates/security-matrix.template.md`
**Matrix file**: `security-matrix-wrong-columns-mock.md`

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS |
| `### Source Pinning Method` | PASS |
| `## Ecosystem Mappings` | PASS |
| `## Forward Pointer` | PASS |

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | PASS | PASS | 2 rows | PASS |
| Ecosystem Mappings | PASS | PASS | 1 row | PASS |

### Ecosystem Mappings Column Validation

**WARNING**: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

Column diff:

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

### Summary

- Sections: all 4 required sections present (PASS)
- Tables: both tables parsable (PASS)
- Ecosystem Mappings columns: 4 of 5 columns do not match the template (WARNING)

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
