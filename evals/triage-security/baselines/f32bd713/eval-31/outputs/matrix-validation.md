# Step 2.1.1 — Matrix Format Validation Results

## Issue: TC-8001 (CVE-2026-31812 quinn-proto)

## Stream: 2.2.x (rhtpa-release.0.4.z)

### Section Presence Check

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

All required sections are present.

### Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 | YES |
| Ecosystem Mappings | YES | YES | 1 | YES |

Both tables have valid Markdown table syntax.

### Ecosystem Mappings Column Validation

**Result: WARNING -- column mismatch detected**

The Ecosystem Mappings table columns do not match the canonical template (`docs/templates/security-matrix.template.md`).

> **Warning:** Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

#### Column Diff

| Position | Expected (Template) | Actual (Matrix) | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

4 of 5 columns have mismatched names. Only the first column (`Ecosystem`) matches the canonical template.

### Auto-Repairs Applied

None. Column name mismatches cannot be auto-repaired -- they require user decision.

### Summary

- **Sections**: PASS (all required sections present)
- **Table parsability**: PASS (both tables parsable)
- **Ecosystem Mappings columns**: WARNING (4 column name mismatches)

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
