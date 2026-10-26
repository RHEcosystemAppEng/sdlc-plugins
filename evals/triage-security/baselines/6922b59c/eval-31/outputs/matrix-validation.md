# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file:** `security-matrix-wrong-columns-mock.md`
**Template:** `docs/templates/security-matrix.template.md`

### Section Headings

| Required Section | Present? | Status |
|---|---|---|
| `## Supportability Matrix` | Yes | Pass |
| `## Ecosystem Mappings` | Yes | Pass |
| `### Source Pinning Method` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 | Pass |
| Ecosystem Mappings | Yes | Yes | 1 | Pass |

### Ecosystem Mappings Column Validation

**Result: WARNING — column mismatch**

> **Warning:** Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
>
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

**Diff:**

```diff
- Ecosystem | Repository | Lock File | Check Command | Upstream Branch
+ Ecosystem | Repo | Lock File Path | Command | Branch
```

Column-by-column comparison:

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | **No** |
| 3 | Lock File | Lock File Path | **No** |
| 4 | Check Command | Command | **No** |
| 5 | Upstream Branch | Branch | **No** |

### Overall Validation Result

**Warnings (non-repairable issues found)**

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

The Ecosystem Mappings table column names do not match the canonical template defined in `docs/templates/security-matrix.template.md`. The column names must be corrected to match the template exactly for automated lock file inspection and upstream fix checks to function correctly.
