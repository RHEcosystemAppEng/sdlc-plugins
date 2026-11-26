# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` not set). Eval run, so Jira, git, and external lookups were not called.
**Issue stream scope**: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix validated**: `security-matrix-missing-section-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`)
**Matrix Last-Updated**: 2026-06-28T10:00:00Z

---

## Template extraction

**Required section headings** (the four that Step 2.1.1 enforces):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

(`## Version Stream` is informational only and is not enforced.)

**Expected Ecosystem Mappings columns**, in order:
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Check 1 — Required sections present

| Required Section | Present in Matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | **FAIL — CRITICAL** |
| `## Forward Pointer` | Yes | PASS |
| `## Version Stream` (informational) | Yes | not enforced |

## Check 2 — Ecosystem Mappings column structure

| Expected Columns | Actual Columns | Result |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | _(no table; section is absent)_ | **CANNOT VALIDATE** (section missing) |

## Check 3 — Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | PASS. Column names are product-specific, so only parsability is checked |
| Ecosystem Mappings | — | — | — | **CANNOT VALIDATE** (section missing) |

---

## Auto-repairs

None apply. The auto-repairable cases (a missing `## Forward Pointer` section, extra whitespace in column headers) do not occur in this file. A missing `## Ecosystem Mappings` section **cannot be auto-repaired**: the skill does not invent lock file paths, check commands, or upstream branches. No file was modified.

---

## Warnings (cannot be auto-repaired)

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`) is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Why this is critical**: Ecosystem Mappings is where each ecosystem gets its lock file path, check command, and upstream branch. Without it:
- Ecosystem detection cannot confirm that **Cargo** (the vulnerable library `quinn-proto` is a Rust crate) is a supported ecosystem for this stream.
- Step 2.3 cannot find which lock file (e.g. `Cargo.lock`) to inspect at the pinned commits (`v0.4.5`, `v0.4.8`) or how to inspect it.
- Step 2.5 cannot find which upstream branch to check for the fix (`quinn-proto` >= 0.11.14).

**Validation status for stream 2.2.x: WARNINGS (critical). Stream halted.**

---

## Validation summary

| Stream | Matrix File | Status | Issues |
|---|---|---|---|
| 2.2.x | `security-matrix-missing-section-mock.md` | **WARNING (critical), stream excluded** | Missing `## Ecosystem Mappings` section |
| 2.1.x | _(no matrix fixture provided for this eval)_ | Not validated | No matrix content available for `rhtpa-release.0.3.z` |

---

## User decision prompt

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Impact on TC-8001**: The issue is scoped to `[rhtpa-2.2]`, which is stream **2.2.x**, and that is the stream excluded above. Choosing option 1 would leave no valid matrix data for the issue's own stream, so its version impact (2.2.0, 2.2.1) could not be determined from lock file evidence. **Recommendation: option 2 (abort).** Add an `## Ecosystem Mappings` section to the 2.2.x matrix that follows the canonical template, for example a Cargo row for `rhtpa-backend` with lock file `Cargo.lock`, check command `git show <commit>:Cargo.lock`, and the correct upstream branch. Then re-run `/sdlc-workflow:triage-security TC-8001`.

Triage pauses at Step 2.1.1 until the user decides. Nothing has been written to Jira (no assignment, Affects Versions change, comment, or task).

---

## Additional observations (outside Step 2.1.1)

- **Container Images section missing**: the template has a `#### Container Images` table that this matrix does not have. Step 2.1.1 does not enforce it as a required heading. The On-demand matrix population step would flag it later as missing coverage for each (Product Version, Component) pair.
- **Supportability Matrix header**: the first column is named `Version`, not the template's `Product Version`. This is allowed because Supportability Matrix columns are product-specific.
- **Matrix staleness (Step 0.3)**: Last-Updated 2026-06-28 is about 151 days before today (2026-11-26), well past the 14-day threshold. The staleness check would offer Refresh now, Proceed anyway, or Stop.
- **PSIRT Affects Versions**: `RHTPA 2.0.0` does not belong to any configured stream (2.1.x, 2.2.x). It should be corrected in Step 3 once version impact can be determined.
