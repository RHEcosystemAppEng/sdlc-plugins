# Step 2.1.1 -- Matrix Format Validation Results

**Vulnerability**: TC-8001 (CVE-2026-31812)
**Validation date**: 2026-07-27

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Template**: `docs/templates/security-matrix.template.md`
**Matrix file**: `security-matrix.md` (rhtpa-release.0.4.z)

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS |
| `### Source Pinning Method` | PASS |
| `## Ecosystem Mappings` | PASS |
| `## Forward Pointer` | PASS |

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | PASS | PASS | 2 rows | PASS |
| Ecosystem Mappings | PASS | PASS | 1 row | PASS |

### Ecosystem Mappings Column Validation

**Result: WARNING -- column mismatch detected**

Expected (from template):
```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix file):
```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

**Diff:**

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | MATCH |
| 2 | Repository | Repo | MISMATCH |
| 3 | Lock File | Lock File Path | MISMATCH |
| 4 | Check Command | Command | MISMATCH |
| 5 | Upstream Branch | Branch | MISMATCH |

4 of 5 columns do not match the canonical template.

### Auto-Repairs Applied

None -- no auto-repairable issues detected.

### Warnings

> Warning: Matrix file `security-matrix.md` (stream 2.2.x) has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

This is a non-repairable issue that requires user decision. The column names do not match the canonical template, which may cause ecosystem mapping lookups to fail during version impact analysis.

### Overall Validation Summary

| Check | Result |
|-------|--------|
| Required sections | PASS |
| Table parsability | PASS |
| Ecosystem Mappings columns | WARNING |

**Recommendation**: Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
