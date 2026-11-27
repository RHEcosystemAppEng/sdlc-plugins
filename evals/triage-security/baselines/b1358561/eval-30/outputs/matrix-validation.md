# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (not Fullsend) — matrix format validation applies
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix validated**: 2.2.x stream — `rhtpa-release.0.4.z` security matrix
(fixture: `security-matrix-missing-section-mock.md`)

> Note: the 2.1.x stream (`rhtpa-release.0.3.z`) matrix was not supplied for this
> eval, so only the 2.2.x stream is validated here. The CLAUDE.md Version Streams
> table also lacks a **Security Matrix Path** column; the supplied fixture was used
> as the 2.2.x matrix.

## Template extraction

**Required section headings** (`##` / `###` from template; `## Version Stream` is
informational and not enforced; `#### Container Images` is level 4 and not in the
required set):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (exact names, in order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required sections present

| Required Section | Present in matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | **FAIL — critical (missing)** |
| `### Source Pinning Method` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |
| `## Version Stream` (informational) | Yes | not enforced |

## Check 2 — Ecosystem Mappings column structure

| Expected | Actual | Result |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | *(section absent — no table)* | **Cannot validate — section missing** |

## Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | ≥1 data row | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | Yes (2 rows: 2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | — | — | — | **N/A — section missing** |

Supportability Matrix column names are product-specific and not compared against the
template (only parsability is checked).

## Auto-repairs

None applicable. The only issue (missing `## Ecosystem Mappings`) is not in the
auto-repairable set (only a missing `## Forward Pointer` and column-header whitespace
are auto-repairable). No changes were proposed or written to the matrix file.

## Warnings

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` (2.2.x stream, `rhtpa-release.0.4.z`) is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

Impact: without Ecosystem Mappings there is no lock file path (e.g., `Cargo.lock`),
check command, or upstream branch for the `cargo` ecosystem / `backend` repository,
so the quinn-proto version cannot be looked up at the pinned commits (`v0.4.5`,
`v0.4.8`) for versions 2.2.0 and 2.2.1.

## Validation result: **WARNINGS** (non-repairable, critical)

| Stream | Matrix | Result | Action |
|---|---|---|---|
| 2.2.x | rhtpa-release.0.4.z security matrix | WARNING — critical (missing `## Ecosystem Mappings`) | Exclude from aggregation if user continues |

### User prompt

> "Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):"

Triage pauses here awaiting the user's choice:
- **1 (Continue)**: the 2.2.x stream is excluded from the aggregated working matrix;
  versions 2.2.0 and 2.2.1 will not be analyzed for quinn-proto impact.
- **2 (Abort)**: triage stops so the matrix can be fixed by adding an
  `## Ecosystem Mappings` section, for example:

  ```
  ## Ecosystem Mappings

  | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
  |---|---|---|---|---|
  | cargo | backend | `Cargo.lock` | `git show <commit>:Cargo.lock` | `main` |
  ```

  (Illustrative only — the actual values must come from the engineer; the skill
  does not write this section automatically.)

## Additional observation (Step 0.3 context)

The matrix's `Last-Updated` timestamp is `2026-06-28T10:00:00Z`, 152 days before
today (2026-11-27), exceeding the 14-day staleness threshold. In an interactive run,
the Step 0.3 staleness warning (Refresh now / Proceed anyway / Stop) would be shown
before reaching this validation step.
