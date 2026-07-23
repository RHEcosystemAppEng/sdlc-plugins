# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Template**: `docs/templates/security-matrix.template.md`

## Stream: 2.2.x

**Matrix file**: `security-matrix-wrong-columns-mock.md`
**Last-Updated**: 2026-06-28T10:00:00Z

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | Present |
| `## Ecosystem Mappings` | Present |
| `### Source Pinning Method` | Present |
| `## Forward Pointer` | Present |

All required sections are present.

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | Parsable |
| Ecosystem Mappings | Yes | Yes | 1 | Parsable |

### Ecosystem Mappings Column Validation

**WARNING: Column mismatch detected.**

The Ecosystem Mappings table has unexpected column names that do not match the canonical template.

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

Column diff:

| Position | Expected | Actual | Match? |
|----------|----------|--------|--------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

### Summary

- **Auto-repairs applied**: None
- **Warnings**: 1

> Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
