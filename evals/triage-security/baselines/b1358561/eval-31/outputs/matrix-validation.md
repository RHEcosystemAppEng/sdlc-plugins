# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream scope**: 2.2.x (summary suffix `[rhtpa-2.2]`)
**Matrix file**: `security-matrix-wrong-columns-mock.md` (stream 2.2.x, Konflux release repo `rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Mode**: interactive (not Fullsend) — format validation applies

## Template extraction

**Required section headings** (enforced):
- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

(`## Version Stream` is informational, not enforced.)

**Expected Ecosystem Mappings columns** (exact names, exact order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check results

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required sections present | PASS | All four required headings found: `## Supportability Matrix`, `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer` (plus informational `## Version Stream`) |
| 2 | Ecosystem Mappings column structure | **WARNING** | Column count matches (5) but 4 of 5 column names differ from the template (see diff below) |
| 3 | Table parsability — Supportability Matrix | PASS | Header row, separator row (`---`), 2 data rows. Column names are product-specific and are not validated against the template |
| 3 | Table parsability — Ecosystem Mappings | PASS | Header row, separator row (`---`), 1 data row |

## Auto-repairs

None applicable. No missing `## Forward Pointer` section, and no leading/trailing whitespace in column headers. Wrong column names are not auto-repairable; no write to the matrix file was proposed or made.

## Warnings

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
| 2 | `Repository` | `Repo` | **MISMATCH** |
| 3 | `Lock File` | `Lock File Path` | **MISMATCH** |
| 4 | `Check Command` | `Command` | **MISMATCH** |
| 5 | `Upstream Branch` | `Branch` | **MISMATCH** |

**Impact**: downstream steps look up Ecosystem Mappings by template column names. Step 2.2 (lock file and check command for the Cargo ecosystem, used to check `quinn-proto` at each pinned tag) and the remediation templates (`Repository` and `Upstream Branch` columns) cannot reliably resolve these fields from this table as it stands.

**Suggested manual fix** (left to the engineer; not auto-applied):

```markdown
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
```

## Validation outcome

**Overall result: WARNINGS** (a non-repairable issue was found). Triage does not continue silently. This prompt goes to the user:

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

Notes for the decision:
- The column-name warning is not one of the critical "halt this stream" conditions. Those are a missing `## Supportability Matrix` or `## Ecosystem Mappings` section, or an unparsable table. If the user picks option 1, stream 2.2.x is not excluded automatically. Its Ecosystem Mappings values would be read by column position (Ecosystem, Repository, Lock File, Check Command, Upstream Branch), and that has to be flagged.
- Recommended choice: **2 (abort)**. Rename the four headers to match the template, then re-run triage for TC-8001.
- Triage stops here until the user answers. No aggregation, version impact analysis, or Jira changes were made.

## Other observations (outside Step 2.1.1 scope)

- The matrix `Last-Updated` is `2026-06-28T10:00:00Z`, which is about 5 months before today (2026-11-27). Step 0.3 would raise a staleness check before this step.
- The matrix has no `#### Container Images` section. That is not a format-validation failure (only the four headings above are enforced), but on-demand population would flag the missing `(Product Version, Component)` rows later.
- The Supportability Matrix uses `Version` where the template uses `Product Version`. Allowed: those columns are product-specific and only checked for parsability.
