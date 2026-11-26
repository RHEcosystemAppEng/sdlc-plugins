# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Issue stream scope**: `[rhtpa-2.2]` → stream **2.2.x** (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Ecosystem detected**: Cargo (quinn-proto is a Rust crate)
**Matrix file validated**: `evals/triage-security/files/security-matrix-wrong-columns-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent)

## Template extraction

**Required section headings** (per Step 2.1.1; `## Version Stream` is informational and not enforced):

- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

**Ecosystem Mappings columns (template header row, in order)**:

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Validation checks

### Check 1: Required sections present — PASS

| Required heading | Present in matrix | Result |
|---|---|---|
| `## Supportability Matrix` | Yes (line 10) | PASS |
| `### Source Pinning Method` | Yes (line 17) | PASS |
| `## Ecosystem Mappings` | Yes (line 21) | PASS |
| `## Forward Pointer` | Yes (line 27) | PASS |
| `## Version Stream` (informational, not enforced) | Yes (line 6) | n/a |

### Check 2: Ecosystem Mappings column structure — FAIL (warning)

The column count matches (5 vs 5), but 4 of the 5 column names do not match the template:

| Position | Expected (template) | Actual (matrix) | Match |
|---|---|---|---|
| 1 | `Ecosystem` | `Ecosystem` | Yes |
| 2 | `Repository` | `Repo` | **No** |
| 3 | `Lock File` | `Lock File Path` | **No** |
| 4 | `Check Command` | `Command` | **No** |
| 5 | `Upstream Branch` | `Branch` | **No** |

Diff (expected vs actual):

```diff
- | Ecosystem | Repository | Lock File      | Check Command | Upstream Branch |
+ | Ecosystem | Repo       | Lock File Path | Command       | Branch          |
```

This is not a whitespace-only difference, so the header-whitespace auto-repair does not
apply. It has to be fixed by hand.

### Check 3: Table parsability — PASS

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 1 (Cargo) | PASS |

The Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) are
product-specific. Per Step 2.1.1 only parsability is checked for this table, not the
column names.

## Auto-repairs

None. No missing `## Forward Pointer` section and no whitespace-only header issues.
The matrix file was not changed.

## Warnings

> ⚠️ Matrix file `evals/triage-security/files/security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

No critical warnings: both critical sections are present and both tables parse.

## Validation result: WARNINGS

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

Triage pauses here until the engineer chooses. No Jira mutations have been made.

**Impact of each choice:**

- **Option 1 (continue)**: the column-name mismatch is a non-critical warning, so stream
  2.2.x is not excluded from aggregation. The Ecosystem Mappings data maps cleanly by
  position (Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` /
  `release/0.4.z`), so the Step 2.3 lock file inspection of quinn-proto for 2.2.0
  (`v0.4.5`) and 2.2.1 (`v0.4.8`) could still run. The engineer should still be told that
  the columns were mapped by position and not by name.
- **Option 2 (abort)**: rename the Ecosystem Mappings header to the template's column
  names (`Repo` → `Repository`, `Lock File Path` → `Lock File`, `Command` →
  `Check Command`, `Branch` → `Upstream Branch`) and re-run triage.

Suggested corrected header for the matrix file (to apply by hand, or through a confirmed
write that follows Local matrix write safety):

```markdown
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
```

## Related observations (outside Step 2.1.1)

- **Step 0.3 staleness**: the matrix has `Last-Updated: 2026-06-28T10:00:00Z`, which is
  151 days before today (2026-11-26). That is past the 14-day threshold, so the
  interactive flow would also offer Refresh now / Proceed anyway / Stop for stream 2.2.x.
- **Repository name mismatch**: the matrix uses the short name `backend`, but Security
  Configuration > Source Repositories lists `rhtpa-backend`. The template says the
  Repository column should hold the configured short name. Step 2.1.1 does not check
  this, but the engineer should be aware of it.
- **Stream 2.1.x**: Version Streams also lists 2.1.x (`rhtpa-release.0.3.z`). No matrix
  for that stream was provided, so it was not validated. Because the issue is scoped to
  2.2.x, 2.1.x would only matter for the Case A cross-stream check.
- The mock Security Configuration has no Security Matrix Path column in the Version
  Streams table, so the provided fixture file was used as the 2.2.x matrix.
