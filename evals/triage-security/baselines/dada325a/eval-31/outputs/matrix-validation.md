# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream in scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
**Konflux Release Repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
**Matrix file validated**: `security-matrix-wrong-columns-mock.md` (stream 2.2.x, `Last-Updated: 2026-06-28T10:00:00Z`)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Template Extraction

- **Required section headings**: `## Supportability Matrix`, `## Ecosystem Mappings`, `### Source Pinning Method`, `## Forward Pointer` (`## Version Stream` is informational only and not enforced)
- **Ecosystem Mappings columns (expected)**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Checks

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required sections present | PASS | `## Supportability Matrix` (line 10), `### Source Pinning Method` (line 17), `## Ecosystem Mappings` (line 21), `## Forward Pointer` (line 27) all present. `## Version Stream` is also present but not enforced. |
| 2 | Ecosystem Mappings column structure | **FAIL — WARNING** | Column count is correct (5), but 4 of the 5 column names differ from the template. See the diff below. |
| 3a | Table parsability: Supportability Matrix | PASS | Header row, `---` separator row, and 2 data rows (2.2.0, 2.2.1). Column names are product-specific and are not checked against the template. |
| 3b | Table parsability: Ecosystem Mappings | PASS | Header row, `---` separator row, and 1 data row (Cargo). |

## Warning

> ⚠️ Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Column diff (expected vs actual)

```diff
- | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
+ | Ecosystem | Repo | Lock File Path | Command | Branch |
```

| Position | Expected (template) | Actual (matrix) | Status |
|----------|---------------------|-----------------|--------|
| 1 | `Ecosystem` | `Ecosystem` | match |
| 2 | `Repository` | `Repo` | **mismatch** |
| 3 | `Lock File` | `Lock File Path` | **mismatch** |
| 4 | `Check Command` | `Command` | **mismatch** |
| 5 | `Upstream Branch` | `Branch` | **mismatch** |

- Column count: expected 5, actual 5 (count matches)
- Column names: 1 of 5 match; positions 2–5 have the wrong names

## Auto-Repair Assessment

| Repair type | Applicable? | Notes |
|-------------|-------------|-------|
| Missing `## Forward Pointer` section | No | Section is present (line 27). |
| Extra whitespace in column headers | No | Headers have no extra whitespace. The problem is the column names themselves, and whitespace normalization cannot fix that. |

The Ecosystem Mappings column mismatch **cannot be auto-repaired**, so it needs a user decision. The skill does not rename columns automatically. No write to the matrix file was proposed or made.

## Validation Outcome: **Warnings**

This warning is not one of the critical halt conditions: both critical sections are present and both tables parse. The column names still differ from the template, and later steps use them by name. Step 2.4 uses `Check Command` and `Lock File` to inspect released versions. Step 2.5 uses `Upstream Branch` and `Repository` for the upstream fix check. The skill would therefore present this prompt to the user:

> "Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):"

**Recommended fix**: rename the Ecosystem Mappings header in the 2.2.x matrix to match the template:

```markdown
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
```

## Additional Observations (outside Step 2.1.1 enforcement)

- The template's `#### Container Images` subsection is missing from this matrix. Step 2.1.1 does not enforce it because it checks only `##`/`###` headings. The On-demand matrix population step would flag it as missing component evidence.
- The Supportability Matrix uses `Version` where the template uses `Product Version`. Supportability Matrix column names are product-specific, so this is not validated.
- The Supportability Matrix source column `backend` does not match the configured Source Repositories short name `rhtpa-backend`. This is informational only and not enforced by Step 2.1.1.
