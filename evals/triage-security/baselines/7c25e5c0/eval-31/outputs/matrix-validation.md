# Step 2.1.1 — Matrix Format Validation

## Template Reference

Canonical template loaded from: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

### Expected Ecosystem Mappings Columns (extracted from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation Results for `security-matrix-wrong-columns-mock.md`

### 1. Required Sections — **Pass**

All four required sections are present in the matrix file:

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

### 2. Table Column Structure (Ecosystem Mappings) — **Warning: Column Mismatch**

⚠️ Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.

**Expected (from template):**

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

**Actual (from matrix file):**

```
Ecosystem | Repo | Lock File Path | Command | Branch
```

**Column-by-column diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | ✓ |
| 2 | Repository | Repo | ✗ |
| 3 | Lock File | Lock File Path | ✗ |
| 4 | Check Command | Command | ✗ |
| 5 | Upstream Branch | Branch | ✗ |

4 of 5 columns do not match the template. This is NOT auto-repairable — column name mismatches may indicate structural divergence that requires human review. Renaming columns without verifying that the data matches the expected semantics could silently corrupt the matrix.

### 3. Table Parsability — **Pass**

Both tables have valid Markdown table syntax:

- **Supportability Matrix**: header row present, separator row present, 2 data rows — parsable.
- **Ecosystem Mappings**: header row present, separator row present, 1 data row — parsable.

---

## Overall Validation Result: **Warning**

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** — skip this stream (2.2.x) due to the column mismatch warning; proceed with any remaining valid streams
2. **Abort triage** — halt triage to fix the matrix file's Ecosystem Mappings columns first

Choose (1/2):
