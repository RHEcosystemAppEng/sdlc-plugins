# Step 2.1.1 — Matrix Format Validation

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

## Validation Results: Stream 2.2.x

**Matrix file:** `security-matrix-wrong-columns-mock.md` (rhtpa-release.0.4.z)

### 1. Required Sections Check

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

**Result:** PASS — all required sections are present.

### 2. Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 rows | Yes |
| Ecosystem Mappings | Yes | Yes | 1 row | Yes |

**Result:** PASS — both tables have valid Markdown table syntax.

### 3. Ecosystem Mappings Column Structure Check

**Expected columns (from template):**
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Actual columns (from matrix file):**
`Ecosystem | Repo | Lock File Path | Command | Branch`

**Column-by-column diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | MATCH |
| 2 | Repository | Repo | MISMATCH |
| 3 | Lock File | Lock File Path | MISMATCH |
| 4 | Check Command | Command | MISMATCH |
| 5 | Upstream Branch | Branch | MISMATCH |

**Result:** WARNING — 4 of 5 Ecosystem Mappings column names do not match the template.

> WARNING: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

---

## Overall Validation Result: WARNING

Matrix validation found issues that cannot be auto-repaired.

The Ecosystem Mappings column mismatch is NOT eligible for auto-repair. Auto-repair is limited to:
- Missing `## Forward Pointer` section (appended with content `None`)
- Extra whitespace in column headers (trimmed)

Column name mismatches require user decision because the skill references columns by name (e.g., "Repository", "Lock File", "Check Command", "Upstream Branch") when extracting ecosystem data in Step 2.3. Using incorrect column names would cause data extraction failures.

**Options:**

1. **Continue with partial data** — skip the 2.2.x stream (which has the column mismatch warning) and proceed with any remaining valid streams
2. **Abort triage** — halt triage to fix the matrix file column names first

Choose (1/2):

---

*Note: Triage is paused at Step 2.1.1. No version impact analysis (Step 2.3), Affects Versions correction (Step 3), or remediation task creation (Step 8) has been performed. The column mismatch must be resolved — either by fixing the matrix file or by choosing to skip this stream — before triage can proceed.*
