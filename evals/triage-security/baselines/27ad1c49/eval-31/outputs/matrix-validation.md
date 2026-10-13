# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x

**Matrix file**: `security-matrix-wrong-columns-mock.md`
**Template**: `docs/templates/security-matrix.template.md`

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
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | Parsable |
| Ecosystem Mappings | Yes | Yes | 1 | Parsable |

### Ecosystem Mappings Column Validation

**Result: WARNING -- column mismatch detected**

The Ecosystem Mappings table has column names that do not match the canonical template.

Expected (from template):

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix file):

```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

**Diff (expected vs actual):**

| Position | Expected | Actual | Match? |
|----------|----------|--------|--------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | No |
| 3 | Lock File | Lock File Path | No |
| 4 | Check Command | Command | No |
| 5 | Upstream Branch | Branch | No |

4 of 5 columns have mismatched names (columns 2-5). The column count is correct (5), but the column names differ from the canonical template.

### Validation Summary

- **Sections**: Pass (all required sections present)
- **Table parsability**: Pass (both tables are well-formed Markdown)
- **Ecosystem Mappings columns**: WARNING -- wrong column names

This is a non-auto-repairable warning. The matrix file uses abbreviated or alternative column names that do not match the canonical template. The triage-security skill may fail to locate expected columns by name.

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):
