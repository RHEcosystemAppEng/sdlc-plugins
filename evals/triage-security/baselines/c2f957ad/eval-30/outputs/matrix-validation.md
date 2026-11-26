# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (no Fullsend bundle; Step 0.6 not in sandbox mode)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix file validated**: `evals/triage-security/files/security-matrix-missing-section-mock.md`
**Stream**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)

## Template Extraction

**Required section headings** (from template `##` / `###` headings; `## Version Stream` is informational and not enforced):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required Sections Present

| Required Section | Present in Matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes (line 10) | PASS |
| `## Ecosystem Mappings` | **No** | **FAIL — critical (missing)** |
| `### Source Pinning Method` | Yes (line 17) | PASS |
| `## Forward Pointer` | Yes (line 21) | PASS |
| `## Version Stream` (informational) | Yes (line 6) | n/a (not enforced) |

## Check 2 — Ecosystem Mappings Column Structure

| Expected | Actual | Result |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | _(no table — section absent)_ | **Cannot validate — section missing** |

## Check 3 — Table Parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | PASS (column names are product-specific; only parsability is validated) |
| Ecosystem Mappings | — | — | — | **Cannot validate — section missing** |

## Auto-Repairs

None applicable. The only auto-repairable issues are a missing `## Forward Pointer`
section and extra whitespace in column headers; neither applies. A missing
`## Ecosystem Mappings` section is **not** auto-repairable (lock file paths, check
commands, and upstream branches cannot be inferred). No write to the matrix file
was proposed or performed.

## Warnings

> ⚠️ Matrix file `evals/triage-security/files/security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

Impact: without Ecosystem Mappings there is no lock file path (e.g., `Cargo.lock`
for the Cargo ecosystem / `quinn-proto`), no check command, and no upstream branch
for the 2.2.x stream. Version impact lookups (Step 2.2+) for released versions
2.2.0 and 2.2.1 cannot proceed for this stream.

## Validation Outcome

**Status: WARNINGS** (non-repairable, critical)

Stream 2.2.x is flagged as a critical-warning stream and would be excluded from
aggregation if the user chooses to continue.

### User Prompt

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

Triage halts here pending the user's choice. Note: the issue summary targets
`[rhtpa-2.2]`, which is exactly the stream being skipped, so choosing option 1
would leave no matrix data for the affected stream. Recommended action: choose
option 2, add the `## Ecosystem Mappings` section (per the canonical template,
e.g., a `cargo` row for `rhtpa-backend` with lock file `Cargo.lock`, check command
`git show <commit>:Cargo.lock`, and the upstream branch), then re-run triage.

## Additional Observations (outside Step 2.1.1 scope)

- **Step 0.3 staleness**: matrix `Last-Updated` is 2026-06-28T10:00:00Z, which is
  151 days before today (2026-11-26) — over the 14-day threshold. In an
  interactive run the staleness prompt (Refresh / Proceed / Stop) would appear before Step 2.1.1.
- **Version Streams config**: the mock CLAUDE.md Version Streams table has no
  `Security Matrix Path` column, so the matrix path for each stream is not
  configured. The provided fixture was used as the 2.2.x matrix.
- **Stream 2.1.x**: no matrix file was provided for the 2.1.x stream
  (`rhtpa-release.0.3.z`), so it was not validated. Normally Step 2.1 would fall back to `git show` against the Konflux repo, but that was out of scope for this eval (no external tools).
- **Container Images**: the template's `#### Container Images` subsection is absent
  from the matrix. It is not one of the four required headings for Step 2.1.1. It
  matters only for on-demand matrix population.
