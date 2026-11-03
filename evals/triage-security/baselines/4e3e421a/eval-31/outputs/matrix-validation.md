# Step 2.1.1 — Matrix Format Validation

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent)
**Issue stream scope**: `[rhtpa-2.2]` → stream **2.2.x** (`rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix file validated**: `security-matrix-wrong-columns-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`)
**Matrix Last-Updated**: 2026-06-28T10:00:00Z

## Template Extraction

**Required section headings** (from template):
- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

(`## Version Stream` is informational and not enforced.)

**Expected Ecosystem Mappings columns** (from template header row, exact names and order):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

## Check Results

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Required sections present | PASS | All four required headings found: `## Supportability Matrix`, `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer` (plus informational `## Version Stream`) |
| 2 | Ecosystem Mappings column structure | **FAIL (WARNING)** | Column count matches (5), but 4 of 5 column names differ from the template |
| 3a | Supportability Matrix parsability | PASS | Header row, `---` separator row, and 2 data rows (2.2.0, 2.2.1). Column names are product-specific and not compared against the template |
| 3b | Ecosystem Mappings parsability | PASS | Header row, `---` separator row, and 1 data row (Cargo) |

## Auto-Repairs

None applicable.
- `## Forward Pointer` is present — no append needed.
- Column headers contain no extra leading/trailing whitespace — the mismatch is in column **names**, which is not auto-repairable.

No changes were proposed or written to the matrix file.

## Warnings (cannot auto-fix — require user decision)

> ⚠️ Matrix file `security-matrix-wrong-columns-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`) has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Column diff (expected vs actual)

```diff
- | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
+ | Ecosystem | Repo | Lock File Path | Command | Branch |
```

| Position | Expected (template) | Actual (matrix) | Status |
|----------|---------------------|-----------------|--------|
| 1 | `Ecosystem` | `Ecosystem` | Match |
| 2 | `Repository` | `Repo` | **Mismatch** |
| 3 | `Lock File` | `Lock File Path` | **Mismatch** |
| 4 | `Check Command` | `Command` | **Mismatch** |
| 5 | `Upstream Branch` | `Branch` | **Mismatch** |

- Expected column count: 5 — Actual column count: 5 (count matches; names do not)
- Missing expected columns: `Repository`, `Lock File`, `Check Command`, `Upstream Branch`
- Unexpected actual columns: `Repo`, `Lock File Path`, `Command`, `Branch`

**Impact**: Steps 2.3 (lock file extraction at pinned refs) and 2.5 (upstream fix check)
look up the lock file path, check command, and upstream branch by their canonical
column names. With these headers, the Cargo mapping for `backend` (`Cargo.lock`,
`git show <tag>:Cargo.lock`, `release/0.4.z`) cannot be reliably resolved through
the template contract. The skill does not guess which non-standard column maps to
which canonical column.

**Suggested fix** (manual, engineer action): rename the Ecosystem Mappings header to

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
```

## Validation Outcome

**Result: WARNINGS** — non-repairable issue found. Triage is paused for a user decision:

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

Notes for the decision:
- Stream 2.2.x is the **only stream in scope** for TC-8001 (`[rhtpa-2.2]`). Option 1
  would exclude the 2.2.x stream from aggregation, leaving no in-scope matrix data,
  so version impact analysis for this issue could not proceed.
- **Recommended**: Option 2 — fix the Ecosystem Mappings header, then re-run
  `/sdlc-workflow:triage-security TC-8001`.
- Not performed (out of scope for this eval / pending decision): Jira assignment and
  transition (Step 0.8), lock file inspection, Affects Versions correction
  (PSIRT value `RHTPA 2.0.0` still unverified), and remediation.
