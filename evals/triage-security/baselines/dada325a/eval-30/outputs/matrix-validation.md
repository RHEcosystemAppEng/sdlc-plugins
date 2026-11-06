# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (not Fullsend) — format validation applies
**Canonical template**: `docs/templates/security-matrix.template.md`
**Stream under validation**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix file**: `security-matrix-missing-section-mock.md` (stands in for the 2.2.x stream's `security-matrix.md`)

> Note: The 2.1.x stream (`rhtpa-release.0.3.z`) is also configured in Security
> Configuration, but no matrix fixture was supplied for it. Only the 2.2.x matrix is
> validated here.

## Template extraction

**Required section headings** (from the template's `##` / `###` headings; `## Version Stream` is informational and not enforced):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required sections present

| Required Section | Present in matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes (line 10) | PASS |
| `## Ecosystem Mappings` | **No** — heading not found anywhere in file | **FAIL (critical)** |
| `### Source Pinning Method` | Yes (line 17) | PASS |
| `## Forward Pointer` | Yes (line 21) | PASS |
| `## Version Stream` (informational) | Yes (line 6) | not enforced |

## Check 2 — Ecosystem Mappings table column structure

**Not evaluable.** The `## Ecosystem Mappings` section does not exist, so there is no
table header to compare against the expected
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch` columns.
This is reported as the missing-section warning below, not as a column mismatch.

## Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | ≥1 data row | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | Yes (2 rows: 2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | — | — | — | N/A (section missing) |

Supportability Matrix column names are product-specific and are only validated for
parsability, not against template names (so `Version` vs. the template's `Product
Version` is not flagged).

## Auto-repair proposals

None applicable. The only auto-repairable issues defined by Step 2.1.1 are a missing
`## Forward Pointer` section and extra whitespace in column headers; neither occurs here.
A missing `## Ecosystem Mappings` section **cannot be auto-repaired** — the skill must not
invent lock file paths, check commands, or upstream branches. No write to the matrix file
was proposed or performed.

## Warnings (non-repairable)

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Why this is critical:** Ecosystem Mappings supply the Lock File, Check Command, and
Upstream Branch that Step 2 uses to determine which `quinn-proto` version (Cargo
ecosystem, `Cargo.lock` in `rhtpa-backend`) shipped in 2.2.0 / 2.2.1 and whether the
upstream fix (0.11.14) is already present. Without them, released-version and fix-availability
checks for the 2.2.x stream cannot run.

## Overall validation result: **WARNINGS** (critical)

Presented to the user:

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Effect of each choice:**

- **1 — Continue**: the 2.2.x stream is excluded from the aggregated working matrix.
  Versions 2.2.0 and 2.2.1 would not be assessed for CVE-2026-31812, even though the
  issue is scoped to `[rhtpa-2.2]`. Only remaining valid streams (2.1.x, if its matrix
  validates) would proceed. No Jira changes would be made for 2.2.x on the basis of
  matrix data.
- **2 — Abort (recommended)**: stop triage. Add a `## Ecosystem Mappings` section to the
  2.2.x matrix following the template, e.g.:

  ```markdown
  ## Ecosystem Mappings

  | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
  |---|---|---|---|---|
  | cargo | rhtpa-backend | `Cargo.lock` | `git show <commit>:Cargo.lock` | `main` |
  ```

  (values shown are illustrative; confirm the actual lock file and upstream branch), then
  re-run `/sdlc-workflow:triage-security TC-8001`.

Triage is paused at this gate awaiting the user's decision; no further steps (version
impact analysis, Affects Versions correction, Jira operations) were executed.

## Other observations (outside Step 2.1.1)

- **Staleness (Step 0.3)**: `Last-Updated: 2026-06-28T10:00:00Z` is ~131 days old
  (threshold 14 days) — would trigger the refresh/proceed/stop prompt.
- **Missing `#### Container Images` table**: not a Step 2.1.1 required heading (it is a
  `####` heading), but its absence would trigger on-demand matrix population later in Step 2.1.
- **Version Streams config**: the Security Configuration's Version Streams table has no
  `Security Matrix Path` column; the matrix path was taken from the supplied fixture.
