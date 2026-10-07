# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Template**: `docs/templates/security-matrix.template.md`

---

## Stream: 2.2.x

**Matrix file**: `security-matrix-wrong-columns-mock.md`

### 1. Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS |
| `## Ecosystem Mappings` | PASS |
| `### Source Pinning Method` | PASS |
| `## Forward Pointer` | PASS |

All required sections are present.

### 2. Table Column Structure (Ecosystem Mappings)

**Result**: WARNING — column mismatch detected

Expected (from template):
```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix file):
```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Column diff:

| Position | Expected | Actual | Match? |
|----------|----------|--------|--------|
| 1 | Ecosystem | Ecosystem | MATCH |
| 2 | Repository | Repo | MISMATCH |
| 3 | Lock File | Lock File Path | MISMATCH |
| 4 | Check Command | Command | MISMATCH |
| 5 | Upstream Branch | Branch | MISMATCH |

> WARNING: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | PASS | PASS | 2 rows | PASS |
| Ecosystem Mappings | PASS | PASS | 1 row | PASS |

Both tables have valid Markdown table syntax with header, separator, and data rows.

### Auto-Repairs Applied

None — no auto-repairable issues found.

### Validation Summary

- **Status**: WARNING (non-repairable issues found)
- **Issues**: 4 column name mismatches in Ecosystem Mappings table
- **Impact**: The Ecosystem Mappings columns do not match the canonical template. Column name mismatches may cause the triage skill to fail when looking up lock file paths and check commands by column name.

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):
