# Step 2.1.1 — Matrix Format Validation

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (not Fullsend) — format validation applies
**Template**: `docs/templates/security-matrix.template.md`

## Template extraction

**Required section headings** (the `## Version Stream` heading is informational and not enforced):

- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

**Expected Ecosystem Mappings columns** (exact names, exact order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Streams validated

| Stream | Konflux Release Repo | Matrix file | Result |
|---|---|---|---|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md` (fixture: `security-matrix-wrong-columns-mock.md`) | **WARNING** |
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | not provided in eval inputs | Not evaluated |

## Stream 2.2.x — check results

### Check 1: Required sections present — PASS

| Required heading | Present? |
|---|---|
| `## Supportability Matrix` | Yes (line 10) |
| `### Source Pinning Method` | Yes (line 17) |
| `## Ecosystem Mappings` | Yes (line 21) |
| `## Forward Pointer` | Yes (line 27) |

`## Version Stream` is also present (informational, not enforced).

### Check 2: Ecosystem Mappings column structure — FAIL

Column count matches (5 expected, 5 actual), but four of the five column names differ from the template:

| # | Expected (template) | Actual (matrix) | Match |
|---|---|---|---|
| 1 | `Ecosystem` | `Ecosystem` | Yes |
| 2 | `Repository` | `Repo` | **No** |
| 3 | `Lock File` | `Lock File Path` | **No** |
| 4 | `Check Command` | `Command` | **No** |
| 5 | `Upstream Branch` | `Branch` | **No** |

Diff:

```diff
- | Ecosystem | Repository | Lock File      | Check Command | Upstream Branch |
+ | Ecosystem | Repo       | Lock File Path | Command       | Branch          |
```

This is not a whitespace-only difference, so the "normalize whitespace in column headers" auto-repair does not apply. Renamed columns cannot be auto-repaired and need a user decision.

> ⚠️ Matrix file `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Check 3: Table parsability — PASS

| Table | Header row | Separator row (`---`) | Data rows |
|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) |
| Ecosystem Mappings | Yes | Yes | 1 (Cargo) |

Note: the Supportability Matrix uses `Version` where the template uses `Product Version`, and `backend` as the source column. These columns are product-specific, so Step 2.1.1 checks only that the table parses, not the names. This is not flagged.

### Auto-repairs

None applicable. Forward Pointer is present, and the header mismatches are not whitespace-only. No write to the matrix file is proposed.

## Validation outcome

**Result: WARNINGS** (an issue that cannot be auto-repaired)

- No critical warnings: both critical sections (`## Supportability Matrix`, `## Ecosystem Mappings`) are present and both tables parse.
- One non-critical warning: the Ecosystem Mappings column names do not match the template (shown above).

Prompt shown to the user:

> "Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):"

If the user picks **1**, stream 2.2.x stays in the aggregation because its warning is not critical. Its Cargo mapping is read by column position: Repo = `backend`, Lock File = `Cargo.lock`, Check Command = `git show <tag>:Cargo.lock`, Upstream Branch = `release/0.4.z`. The engineer should still rename the columns to match the template.
If the user picks **2**, triage stops so the matrix can be fixed first.

The matrix file was not changed during validation.
