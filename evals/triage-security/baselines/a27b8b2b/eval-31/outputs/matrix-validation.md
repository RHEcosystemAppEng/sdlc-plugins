# Step 2.1.1 -- Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Ecosystem Mappings columns extracted from template:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation Results: security-matrix-wrong-columns-mock.md (Stream 2.2.x)

### 1. Required Sections Check

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: **Pass** -- all required sections are present.

### 2. Table Column Structure (Ecosystem Mappings)

**Expected columns** (from canonical template):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

**Actual columns** (from loaded matrix file):

```
Ecosystem | Repo | Lock File Path | Command | Branch
```

**Column diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

Result: **FAIL** -- 4 of 5 columns do not match the canonical template.

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 rows | Yes |
| Ecosystem Mappings | Yes | Yes | 1 row | Yes |

Result: **Pass** -- both tables have valid Markdown table syntax.

### 4. Auto-Repair Assessment

The column name mismatch in Ecosystem Mappings is **NOT eligible for auto-repair**. Only the following issues qualify for auto-repair:

- Missing `## Forward Pointer` section (append with content `None`)
- Extra whitespace in column headers (normalize by trimming)

Column name mismatches require user decision because the skill uses column names to locate data (Repository, Lock File, Check Command, Upstream Branch) during version impact analysis. Using incorrect column names could cause silent data extraction failures.

---

## Validation Outcome: WARNING

Matrix validation found issues that cannot be auto-repaired.

> **Warning:** Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

The following columns do not match the canonical template:
- Column 2: expected `Repository`, found `Repo`
- Column 3: expected `Lock File`, found `Lock File Path`
- Column 4: expected `Check Command`, found `Command`
- Column 5: expected `Upstream Branch`, found `Branch`

**Options:**

1. **Continue with partial data** -- skip the 2.2.x stream (Ecosystem Mappings cannot be reliably parsed with non-standard column names) and proceed with any remaining valid streams
2. **Abort triage** -- halt triage to fix the matrix file first (rename columns to match the canonical template)

Choose (1/2):
