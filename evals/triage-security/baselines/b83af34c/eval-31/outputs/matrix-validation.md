# Step 2.1.1 -- Matrix Format Validation Results

## Triage Context

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Stream**: 2.2.x (from issue suffix `[rhtpa-2.2]`)

## Template Reference

Canonical template: `docs/templates/security-matrix.template.md`

## Validation: Stream 2.2.x

**Matrix file**: `security-matrix-wrong-columns-mock.md`

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS -- present |
| `## Ecosystem Mappings` | PASS -- present |
| `### Source Pinning Method` | PASS -- present |
| `## Forward Pointer` | PASS -- present |

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | yes | yes | 2 | PASS |
| Ecosystem Mappings | yes | yes | 1 | PASS |

### Ecosystem Mappings Column Validation

**Result: COLUMN MISMATCH**

Expected columns (from canonical template `docs/templates/security-matrix.template.md`):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

Actual columns (from matrix file):

```
Ecosystem | Repo | Lock File Path | Command | Branch
```

**Diff of column names:**

```diff
  Column 1: Ecosystem        -- match
- Column 2: Repository       (expected)
+ Column 2: Repo             (actual)
- Column 3: Lock File        (expected)
+ Column 3: Lock File Path   (actual)
- Column 4: Check Command    (expected)
+ Column 4: Command          (actual)
- Column 5: Upstream Branch  (expected)
+ Column 5: Branch           (actual)
```

4 of 5 columns have mismatched names. Only column 1 (`Ecosystem`) matches the template.

### Auto-Repair Assessment

This issue **cannot be auto-repaired**. Column name mismatches in Ecosystem Mappings are classified as warnings per Step 2.1.1 -- they require user decision because:

1. Renaming columns may change the semantic meaning of the data
2. The skill references columns by name (e.g., "Repository column", "Check Command column", "Upstream Branch column") in Steps 2.3 and 2.5
3. Automatic renaming could silently mask a deeper structural problem (e.g., the data may have been intentionally structured differently)

### Warning

> **Warning**: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

## Validation Summary

| Check | Result |
|-------|--------|
| Required sections | PASS |
| Table parsability | PASS |
| Ecosystem Mappings columns | **WARNING -- column mismatch** |

**Overall: Warnings detected (non-repairable issues)**

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** -- skip streams with critical warnings (the 2.2.x stream Ecosystem Mappings columns do not match the template; column-based lookups may return incorrect data)
2. **Abort triage** -- fix the matrix files first to align column names with the canonical template

Choose (1/2):
