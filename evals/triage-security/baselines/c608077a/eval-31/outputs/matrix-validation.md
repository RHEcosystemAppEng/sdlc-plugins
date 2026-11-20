# Matrix Format Validation — TC-8001 (Step 2.1.1)

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream under validation**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path `/home/dev/repos/rhtpa-release.0.4.z`)
**Matrix file**: `security-matrix-wrong-columns-mock.md` (fixture standing in for `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (not Fullsend), so Step 2.1.1 validation runs.

> Scope note: the issue title suffix `[rhtpa-2.2]` targets the 2.2.x stream. No matrix
> fixture was supplied for the 2.1.x stream (`rhtpa-release.0.3.z`), so only 2.2.x was validated.

## Template extraction

- **Required section headings**: `## Supportability Matrix`, `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer`
  (`## Version Stream` is informational and not enforced)
- **Ecosystem Mappings columns (expected, in order)**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check results

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required section: `## Supportability Matrix` | PASS | Present |
| 1 | Required section: `### Source Pinning Method` | PASS | Present |
| 1 | Required section: `## Ecosystem Mappings` | PASS | Present |
| 1 | Required section: `## Forward Pointer` | PASS | Present (no auto-repair needed) |
| 2 | Ecosystem Mappings column names/order | **WARNING** | Column count matches (5), but 4 of 5 names differ from the template (see diff below) |
| 3 | Supportability Matrix table parsable | PASS | Header row, separator row (`---`), and 2 data rows (2.2.0, 2.2.1). Column names are product-specific and not enforced. |
| 3 | Ecosystem Mappings table parsable | PASS | Header row, separator row (`---`), and 1 data row (Cargo) |
| — | Whitespace in column headers | PASS | No leading/trailing whitespace to normalize |

## Warning

> ⚠️ Matrix file `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md` (fixture `security-matrix-wrong-columns-mock.md`) has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Column diff (expected vs actual)

| Position | Expected (template) | Actual (matrix) | Status |
|----------|---------------------|-----------------|--------|
| 1 | `Ecosystem` | `Ecosystem` | match |
| 2 | `Repository` | `Repo` | **MISMATCH** |
| 3 | `Lock File` | `Lock File Path` | **MISMATCH** |
| 4 | `Check Command` | `Command` | **MISMATCH** |
| 5 | `Upstream Branch` | `Branch` | **MISMATCH** |

```diff
- | Ecosystem | Repository | Lock File      | Check Command | Upstream Branch |
+ | Ecosystem | Repo       | Lock File Path | Command       | Branch          |
```

This is a non-repairable issue: column renames are not in the auto-repair set (only a
missing Forward Pointer section and header whitespace are auto-repaired). The matrix file
was **not modified**.

## Auto-repairs

None performed. No write was attempted, so Local matrix write safety was not invoked and
the file's `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) is unchanged.

## Validation outcome: **Warnings**

Prompt shown to the user before proceeding:

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

Notes for the decision:
- The column-mismatch warning is **not** one of the critical (halting) warnings — those are a
  missing `## Supportability Matrix` / `## Ecosystem Mappings` section or an unparsable table.
  If the user chooses 1, the 2.2.x stream is not excluded from aggregation; its Supportability
  Matrix rows (2.2.0 → backend `v0.4.5`, 2.2.1 → backend `v0.4.8`) remain usable.
- The Ecosystem Mappings row (Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` /
  `release/0.4.z`) can be read positionally, since the columns line up one-to-one with the template.
  The engineer should still rename the headers to the canonical names so later runs pass.
- If the user chooses 2, triage stops here. Suggested fix: change the Ecosystem Mappings header to
  `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |`.

Triage pauses here until the user chooses. No later steps (aggregation, version checks
against `Cargo.lock` for quinn-proto < 0.11.14, Jira updates) were run.
