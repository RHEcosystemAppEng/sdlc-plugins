# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` not set). Step 0.7 skipped.
**Stream scope**: `[rhtpa-2.2]` maps to Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix validated**: `evals/triage-security/files/security-matrix-wrong-columns-mock.md` (stream 2.2.x)
**Canonical template**: `docs/templates/security-matrix.template.md`

> Note: the Version Streams table in the project CLAUDE.md has no `Security Matrix Path`
> column, so the eval-provided fixture is used as the 2.2.x matrix. No matrix was supplied
> for stream 2.1.x, so it is not validated here.

## Template Extraction

**Required section headings** (from template):

- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

(`## Version Stream` is informational and not enforced. `#### Container Images` is level 4, so it is not on the required list.)

**Expected Ecosystem Mappings columns** (template header row, in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Validation Checks

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required section `## Supportability Matrix` | PASS | Present |
| 1 | Required section `### Source Pinning Method` | PASS | Present |
| 1 | Required section `## Ecosystem Mappings` | PASS | Present |
| 1 | Required section `## Forward Pointer` | PASS | Present |
| 2 | Ecosystem Mappings column names and order | **FAIL (WARNING)** | Same column count (5), but 4 of 5 names differ from the template |
| 3 | Supportability Matrix table is parsable | PASS | Header, `---` separator, 2 data rows (2.2.0, 2.2.1). Column names are product-specific, so they are not compared to the template |
| 3 | Ecosystem Mappings table is parsable | PASS | Header, `---` separator, 1 data row (Cargo) |

## Warning

> ⚠️ Matrix file `evals/triage-security/files/security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Column Diff (expected vs actual)

| Position | Expected (template) | Actual (matrix) | Status |
|----------|---------------------|-----------------|--------|
| 1 | `Ecosystem` | `Ecosystem` | Match |
| 2 | `Repository` | `Repo` | **Mismatch** |
| 3 | `Lock File` | `Lock File Path` | **Mismatch** |
| 4 | `Check Command` | `Command` | **Mismatch** |
| 5 | `Upstream Branch` | `Branch` | **Mismatch** |

```diff
- | Ecosystem | Repository | Lock File      | Check Command | Upstream Branch |
+ | Ecosystem | Repo       | Lock File Path | Command       | Branch          |
```

## Auto-Repair Assessment

- Missing `## Forward Pointer`: not applicable, the section is present.
- Extra whitespace in column headers: not applicable. The mismatch comes from different column names, not padding.
- **Column renames cannot be auto-repaired.** Step 2.1.1 only allows the two repairs above. Renaming columns needs an engineer decision, so the matrix file was **not modified** and `Last-Updated` stays as it is.

## Validation Outcome: **WARNINGS** (cannot be auto-repaired)

| Stream | Matrix | Status | Critical? |
|--------|--------|--------|-----------|
| 2.2.x | `security-matrix-wrong-columns-mock.md` | Warning: Ecosystem Mappings column mismatch | No. All required sections are present and the tables parse. Only the column names differ from the template |

User prompt (triage is paused here until the engineer answers):

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Recommendation**: Option 2. Fix the 2.2.x Ecosystem Mappings header to match the template
(`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`), then re-run triage.
The Cargo row (`backend`, `Cargo.lock`, `git show <tag>:Cargo.lock`, `release/0.4.z`) can be
kept unchanged under the renamed headers. If the engineer picks option 1 instead, this
warning is not in the critical class (missing section or unparsable table), so stream 2.2.x
would stay in the aggregation. Its mappings would then be read by matching each column to
its expected meaning by position.

## Related Observation (Step 0.3 Staleness)

The matrix header has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-26, so the
matrix is **151 days old**, which is past the 14-day threshold. Step 0.3 would give the engineer
three choices: Refresh now, Proceed anyway, or Stop.

No Jira, git, or external calls were made. This analysis comes only from the provided fixture files.
