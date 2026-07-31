# Step 2.1.1 — Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

### Required Section Headings (extracted from template)

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

### Expected Ecosystem Mappings Columns (extracted from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation: Stream 2.2.x — `security-matrix-wrong-columns-mock.md`

### 1. Required Sections Present

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: **Pass** — all required sections are present.

### 2. Ecosystem Mappings Column Structure

Expected columns (from template):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

Actual columns (from matrix file):

```
Ecosystem | Repo | Lock File Path | Command | Branch
```

Column-by-column diff:

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | **No** |
| 3 | Lock File | Lock File Path | **No** |
| 4 | Check Command | Command | **No** |
| 5 | Upstream Branch | Branch | **No** |

Result: **Warning** — 4 of 5 columns do not match the template.

> ⚠️ Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

This column mismatch is **NOT auto-repairable** — only the following issues are eligible for auto-repair:
- Missing `## Forward Pointer` section (append with content `None`)
- Extra whitespace in column headers (normalize by trimming)

Column name mismatches require user decision because renaming columns could break downstream parsing logic that depends on exact column names.

### 3. Table Parsability

| Table | Header Row? | Separator Row? | Data Rows? | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | Yes (2 rows) | Yes |
| Ecosystem Mappings | Yes | Yes | Yes (1 row) | Yes |

Result: **Pass** — both tables are syntactically valid Markdown tables.

---

## Overall Validation Result: Warning

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** — skip this stream (2.2.x) due to column mismatch; proceed with any remaining valid streams
2. **Abort triage** — halt triage to fix the matrix file column names first

Choose (1/2):

**Note**: The Ecosystem Mappings columns in `security-matrix-wrong-columns-mock.md` must be renamed to match the canonical template before automated triage can process this stream. The expected column names are: `Ecosystem`, `Repository`, `Lock File`, `Check Command`, `Upstream Branch`.
