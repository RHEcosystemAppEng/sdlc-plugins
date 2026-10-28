# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-wrong-columns-mock.md`
**Template**: `docs/templates/security-matrix.template.md`

### Section Headings

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 | Parsable |
| Ecosystem Mappings | Yes | Yes | 1 | Parsable |

### Ecosystem Mappings Column Validation

**Result: WARNING -- Column mismatch detected**

Expected columns (from template):

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual columns (from matrix file):

```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Diff:

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | No |
| 3 | Lock File | Lock File Path | No |
| 4 | Check Command | Command | No |
| 5 | Upstream Branch | Branch | No |

> **Warning**: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

This column mismatch cannot be auto-repaired. The Ecosystem Mappings column names must match the canonical template exactly for triage-security to reliably parse lock file paths, check commands, and upstream branch references.

### Overall Validation Result

**Warnings** (non-repairable issues found)

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

The 2.2.x stream's Ecosystem Mappings table uses non-standard column names. While the column count matches (5 columns), the column headers differ from the canonical template. This may cause incorrect field lookups during lock file inspection (Step 2.3) if the skill relies on column names for parsing.
