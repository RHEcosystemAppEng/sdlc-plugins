# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (`security-matrix-wrong-columns-mock.md`)

### Section Headings

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `### Source Pinning Method` | YES |
| `## Ecosystem Mappings` | YES |
| `## Forward Pointer` | YES |

All required section headings are present.

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Valid? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 | YES |
| Ecosystem Mappings | YES | YES | 1 | YES |

Both tables have valid Markdown table syntax.

### Ecosystem Mappings Column Validation

> **WARNING** Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
>
> **Expected** (from `docs/templates/security-matrix.template.md`):
> ```
> | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
> ```
>
> **Actual**:
> ```
> | Ecosystem | Repo | Lock File Path | Command | Branch |
> ```
>
> **Diff**:
> ```diff
> - Ecosystem | Repository | Lock File | Check Command | Upstream Branch
> + Ecosystem | Repo       | Lock File Path | Command    | Branch
>              ^^^^^^^^^^   ^^^^^^^^^^^^^^   ^^^^^^^^^^^^  ^^^^^^
>              Column 2:    Column 3:        Column 4:     Column 5:
>              expected     expected         expected      expected
>              "Repository" "Lock File"      "Check        "Upstream
>              got "Repo"   got "Lock File   Command"      Branch"
>                           Path"            got "Command" got "Branch"
> ```

### Summary

- **Auto-repairs performed**: none
- **Warnings**: 1 (column mismatch in Ecosystem Mappings)

Matrix validation found issues that cannot be auto-repaired.

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. **Continue with partial data** — skip streams with critical warnings
> 2. **Abort triage** to fix the matrix files first
>
> Choose (1/2):

**Status**: BLOCKED — awaiting user decision before proceeding with version impact analysis.
