# Step 2.1.1 — Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

### Required section headings extracted from template

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

### Ecosystem Mappings columns extracted from template

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation: Stream 2.2.x matrix (security-matrix-wrong-columns-mock.md)

### 1. Required sections present

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: **Pass** -- all required sections are present.

### 2. Table column structure (Ecosystem Mappings)

**Expected columns** (from canonical template):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

**Actual columns** (from matrix file):

```
Ecosystem | Repo | Lock File Path | Command | Branch
```

**Column-by-column diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | **No** |
| 3 | Lock File | Lock File Path | **No** |
| 4 | Check Command | Command | **No** |
| 5 | Upstream Branch | Branch | **No** |

4 of 5 columns do not match the canonical template.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 rows | Yes |
| Ecosystem Mappings | Yes | Yes | 1 row | Yes |

Result: **Pass** -- both tables are syntactically valid Markdown tables.

---

## Validation Result: WARNING

The Ecosystem Mappings table has column names that do not match the canonical template. This is a non-auto-repairable issue that requires user decision.

> **Warning**: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

This column mismatch is **not** eligible for auto-repair. Only the following issues are auto-repairable:
- Missing `## Forward Pointer` section (appended with content `None`)
- Extra whitespace in column headers (trimmed)

Column name mismatches require user intervention because they may indicate a structurally different matrix format that cannot be safely reinterpreted.

---

## User Decision Required

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** -- skip the 2.2.x stream (Ecosystem Mappings columns cannot be reliably parsed against the expected schema)
2. **Abort triage** -- halt triage to fix the matrix file column names first

Choose (1/2):
