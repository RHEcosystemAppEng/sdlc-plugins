# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

### Section Headings

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `### Source Pinning Method` | YES |
| `## Ecosystem Mappings` | YES |
| `## Forward Pointer` | YES |

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 | YES |
| Ecosystem Mappings | YES | YES | 1 | YES |

### Ecosystem Mappings Column Validation

**Result: WARNING — column mismatch detected**

The Ecosystem Mappings table columns do not match the canonical template (`docs/templates/security-matrix.template.md`).

Expected (template):
```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (matrix file):
```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Column diff:

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

This column mismatch **cannot be auto-repaired** — the column names differ in ways that require a user decision to resolve. The data may still be usable if columns are positionally equivalent, but the skill cannot confirm this without user input.

### Validation Summary

| Check | Result |
|---|---|
| Required sections | PASS |
| Table parsability | PASS |
| Ecosystem Mappings columns | WARNING |

**Overall: WARNING** — non-repairable issues found.

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** — attempt to use the Ecosystem Mappings table by positional column mapping (skip streams with critical warnings)
2. **Abort triage** — fix the matrix file column headers to match the canonical template first

Choose (1/2):
