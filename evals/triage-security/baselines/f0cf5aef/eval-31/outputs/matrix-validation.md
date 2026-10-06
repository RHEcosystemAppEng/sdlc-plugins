# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Template**: `docs/templates/security-matrix.template.md`
**Matrix file**: `security-matrix.md` (stream 2.2.x)

### Section Validation

| Required Section | Status |
|---|---|
| `## Supportability Matrix` | PASS |
| `### Source Pinning Method` | PASS |
| `## Ecosystem Mappings` | PASS |
| `## Forward Pointer` | PASS |

All required sections are present.

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | PASS | PASS | 2 rows | PASS |
| Ecosystem Mappings | PASS | PASS | 1 row | PASS |

Both tables have valid Markdown table syntax.

### Ecosystem Mappings Column Validation

**WARNING: Column mismatch detected. This cannot be auto-repaired.**

Expected columns (from canonical template):

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual columns (from matrix file):

```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Diff:

```diff
- Ecosystem | Repository | Lock File | Check Command | Upstream Branch
+ Ecosystem | Repo       | Lock File Path | Command  | Branch
            ^^^^^^^^^^    ^^^^^^^^^^^^^^    ^^^^^^^^^   ^^^^^^
            Column 2:     Column 3:        Column 4:   Column 5:
            expected      expected         expected    expected
            "Repository"  "Lock File"      "Check      "Upstream
            got "Repo"    got "Lock File   Command"    Branch"
                          Path"            got         got "Branch"
                                           "Command"
```

### Summary

| Check | Result |
|---|---|
| Required sections | PASS |
| Table parsability | PASS |
| Ecosystem Mappings columns | WARNING |

**Validation outcome: WARNING (non-repairable issues found)**

Matrix validation found issues that cannot be auto-repaired.

> Matrix file `security-matrix.md` (stream 2.2.x) has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

Options:
1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

This stream cannot be reliably processed until the Ecosystem Mappings column names are corrected to match the canonical template.
