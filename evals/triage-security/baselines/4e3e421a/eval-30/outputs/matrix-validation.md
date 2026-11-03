# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Issue stream scope**: `[rhtpa-2.2]` → **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Execution mode**: interactive (`FULLSEND_OUTPUT_DIR` not set). Step 2.1.1 applies.
**Matrix validated**: `security-matrix-missing-section-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Template extraction

Required section headings (from the template, per Step 2.1.1):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

(`## Version Stream` is informational and not enforced.)

Expected Ecosystem Mappings columns, in order:
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1: Required sections present

| Required Section | Present? | Notes |
|---|---|---|
| `## Supportability Matrix` | YES | |
| `## Ecosystem Mappings` | **NO** | **Section is missing from the file. Critical.** |
| `### Source Pinning Method` | YES | One entry: `backend` → `artifacts.lock.yaml` |
| `## Forward Pointer` | YES | "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | YES | Not enforced |

## Check 2: Ecosystem Mappings column structure

| Expected | Actual |
|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | *(no table — section absent)* |

**Result**: cannot be validated because the section does not exist. This is reported under the missing-section warning, not as a separate column warning.

## Check 3: Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | YES (`Version \| Build \| Build Date \| backend \| Notes`) | YES | 2 (2.2.0, 2.2.1) | PARSABLE |
| Ecosystem Mappings | — | — | — | NOT PRESENT |

Supportability Matrix column names are product-specific (e.g. `Version` rather than the template's `Product Version`). Step 2.1.1 checks only that this table parses, not its column names, so this is not flagged.

## Auto-repair proposals

**None.** Only two issues can be auto-repaired: a missing `## Forward Pointer` section and extra whitespace in column headers. Neither occurs here. A missing `## Ecosystem Mappings` section **cannot be auto-repaired**. Its rows (ecosystem, repository, lock file, check command, upstream branch) are product-specific data, and the skill must not make them up. No write to `security-matrix.md` is proposed.

## Validation result: **WARNINGS** (non-repairable)

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`) is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Why this blocks the stream:** the Ecosystem Mappings table is where triage finds:
- which ecosystems are supported, which drives ecosystem detection. quinn-proto is a Cargo crate, but Cargo cannot be confirmed as a supported ecosystem for this stream.
- the lock file path (e.g. `Cargo.lock`) and the check command for `git show <commit>:<lock-file>` in Step 2.3.
- the upstream branch for the upstream fix status check in Step 2.5.

Without it, no version lookups can run for 2.2.x (2.2.0 `v0.4.5`, 2.2.1 `v0.4.8`). The skill must not guess a lock file path or ecosystem.

**Stream status**: 2.2.x → **HALTED (critical warning)**, excluded from aggregation unless the matrix is fixed.

## User decision required

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Recommendation: option 2 (Abort).** 2.2.x is the **only** stream in this issue's scope (`[rhtpa-2.2]`). If 2.2.x is skipped, the in-scope versions have no version impact data. Steps 3 (Affects Versions correction) and 8 (Remediation) would then rest on no evidence. Fix the matrix first by adding an `## Ecosystem Mappings` section that matches the template, for example a Cargo row for `backend` with its lock file, check command and upstream branch. Then re-run `/sdlc-workflow:triage-security TC-8001`.

Triage stops here until the engineer chooses. No Jira mutations have been made and no matrix files have been written.

## Other observations (not Step 2.1.1 failures)

- **Staleness (Step 0.3)**: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` is 128 days old as of 2026-11-03, well past the 14-day threshold. The staleness prompt (Refresh now / Proceed anyway / Stop) would come before this step. Refreshing via setup Step 10.6 would also be a good moment to fill in the missing Ecosystem Mappings.
- **Missing Container Images subsection**: the template's `#### Container Images` table is absent. Step 2.1.1 does not enforce it, but on-demand matrix population would flag it.
- **2.1.x stream**: the config lists a 2.1.x stream (`rhtpa-release.0.3.z`), but no matrix fixture was provided for it, so it was not validated here. It is also outside this issue's scope.
- **Configuration note**: the Version Streams table in the mock CLAUDE.md has no `Security Matrix Path` column. Matrix location was taken from the provided fixture.
