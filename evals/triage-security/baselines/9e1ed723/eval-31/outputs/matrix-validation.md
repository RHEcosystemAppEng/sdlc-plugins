# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Template**: `docs/templates/security-matrix.template.md`
**Matrix validated**: `security-matrix-wrong-columns-mock.md` (stream 2.2.x, Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix Last-Updated**: 2026-06-28T10:00:00Z

> Note: the Security Configuration Version Streams table in the project CLAUDE.md has no
> `Security Matrix Path` column, so this eval used the provided fixture file as the 2.2.x
> stream matrix. Only the 2.2.x stream matrix was supplied, so the 2.1.x stream was not validated.

## Template extraction

- **Required section headings** (`##` / `###`, excluding informational `## Version Stream`):
  `## Supportability Matrix`, `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer`
- **Expected Ecosystem Mappings columns** (exact names, exact order):
  `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check results

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required section `## Supportability Matrix` | PASS | Present |
| 1 | Required section `### Source Pinning Method` | PASS | Present |
| 1 | Required section `## Ecosystem Mappings` | PASS | Present |
| 1 | Required section `## Forward Pointer` | PASS | Present ("This is the latest stream — no forward pointer.") |
| 2 | Ecosystem Mappings column names/order | **FAIL (WARNING)** | 4 of 5 column names differ from the template. Column count matches (5). |
| 3 | Supportability Matrix table parsable | PASS | Header row, `---` separator row, and 2 data rows. Column names are product-specific and not checked against the template. |
| 3 | Ecosystem Mappings table parsable | PASS | Header row, `---` separator row, and 1 data row |

## Column diff — Ecosystem Mappings

```diff
- | Ecosystem | Repository | Lock File      | Check Command | Upstream Branch |
+ | Ecosystem | Repo       | Lock File Path | Command       | Branch          |
```

| Position | Expected (template) | Actual (matrix) | Match |
|----------|---------------------|-----------------|-------|
| 1 | `Ecosystem` | `Ecosystem` | yes |
| 2 | `Repository` | `Repo` | **NO** |
| 3 | `Lock File` | `Lock File Path` | **NO** |
| 4 | `Check Command` | `Command` | **NO** |
| 5 | `Upstream Branch` | `Branch` | **NO** |

## Auto-repairs

None. Neither auto-repairable condition applies: the `## Forward Pointer` section exists, and the
column headers have no extra leading/trailing whitespace. Renamed columns cannot be auto-repaired,
so the matrix was **not modified**. No write was made and `Last-Updated` is unchanged.

## Warnings (non-repairable)

> ⚠️ Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

This is not a critical (halting) warning: both critical sections exist and both tables parse.
However, Step 2.3 looks up the `Lock File`, `Check Command`, and `Upstream Branch` columns by name,
so this stream's mappings cannot be read reliably until the headers match the template.

## Overall validation status: **WARNINGS**

User prompt (shown before aggregation):

> "Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):"

Triage is paused at this prompt and waits for the engineer's choice. To fix the matrix, rename the
Ecosystem Mappings header to:

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
```
