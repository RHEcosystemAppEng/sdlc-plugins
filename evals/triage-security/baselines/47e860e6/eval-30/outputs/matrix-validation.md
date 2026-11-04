# Matrix Format Validation — TC-8001 (Step 2.1.1)

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Execution mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent), simulated with files. No Jira, git, or network calls were made.
**Issue stream scope**: `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix file validated**: `security-matrix-missing-section-mock.md` (stream **2.2.x**, `rhtpa-release.0.4.z`)

---

## Context from earlier steps

- **Step 0 (Configuration)**: PASS. The project CLAUDE.md has Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-...`), Code Intelligence, and Security Configuration (Product Lifecycle, 2 Version Streams, 1 Source Repository). Note: the Version Streams table has no `Security Matrix Path` column, so the matrix fixture that was provided is used as the 2.2.x matrix.
- **Step 0.3 (Staleness)**: the matrix header has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-04, so the matrix is **129 days old**, more than the 14-day threshold. In a live run, the engineer would be offered Refresh now / Proceed anyway / Stop. This eval assumes **Proceed anyway** so that Step 2.1.1 runs.
- **Step 1 (Extraction)**: CVE-2026-31812, library `quinn-proto` (Cargo ecosystem), affected range `< 0.11.14`, fixed in `0.11.14`, component `pscomponent:org/rhtpa-server`, PSIRT Affects Versions `RHTPA 2.0.0`.

---

## Template requirements extracted

**Required section headings** (`##` / `###` levels; `## Version Stream` is informational only and not enforced):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (exact names, in this order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Check 1: Required sections present

| Required section | Present in matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | **No, the section is missing entirely** | **CRITICAL WARNING** |
| `## Forward Pointer` | Yes ("This is the latest stream — no forward pointer.") | PASS |
| `## Version Stream` (informational) | Yes | Not enforced |

## Check 2: Ecosystem Mappings column structure

| Expected | Actual | Result |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | *(no table, because the section is absent)* | **Cannot validate.** Covered by the missing-section warning |

## Check 3: Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | PASS. Column names are product-specific and are not compared to the template |
| Ecosystem Mappings | none | none | none | **Not applicable.** The section is missing, which is covered by the critical warning |

---

## Auto-repairs

**None.** The only auto-repairable problems are a missing `## Forward Pointer` section and extra whitespace in column headers, and neither occurs here. A missing `## Ecosystem Mappings` section **cannot be auto-repaired**: the skill cannot invent the ecosystem, lock file, check command, or upstream branch values, and the guardrails forbid fabricating data. No proposed write was prepared, and the matrix file was not modified.

---

## Warnings (non-repairable)

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` (stream 2.2.x, `rhtpa-release.0.4.z`) is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Why this is critical**: Ecosystem Mappings is the source of the lock file path (for example `Cargo.lock`), the check command (`git show <commit>:<lock-file>`), and the upstream branch for each ecosystem. Without it:
- Ecosystem detection in Step 1 cannot confirm that **Cargo** is a supported ecosystem for this stream.
- Step 2.3 cannot work out which lock file to read at the pinned commits `v0.4.5` and `v0.4.8`.
- Step 2.5 cannot work out which upstream branch to check for the fix.

---

## Validation result: **WARNINGS**. The stream is halted.

| Stream | Matrix | Result | Included in aggregation? |
|---|---|---|---|
| 2.2.x | `security-matrix-missing-section-mock.md` | WARNING: missing `## Ecosystem Mappings` (critical) | **No, excluded** |
| 2.1.x | (no matrix supplied for this eval) | Not evaluated | n/a |

### Prompt presented to the engineer

> "Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):"

### Impact on TC-8001

TC-8001 is **scoped to stream 2.2.x** (`[rhtpa-2.2]`), and that is the stream with the critical warning. If the engineer picks option 1, 2.2.x is excluded from aggregation. That leaves no in-scope version impact data for 2.2.0 or 2.2.1, so the Affects Versions correction (Step 3) and remediation (Step 8) cannot be decided for this issue on lock-file evidence.

**Recommendation**: choose **2 (Abort)**. Add the `## Ecosystem Mappings` section to the 2.2.x matrix using the canonical template. For example, add a Cargo row for `backend` with its lock file, check command, and upstream branch, filled with real values from the repository rather than guessed ones. Alternatively, re-run `/setup` matrix population (Step 10.6), which also fixes the 129-day staleness. Then re-run `/sdlc-workflow:triage-security TC-8001`.

No Jira mutations were proposed or made. Triage stopped at Step 2.1.1 pending the engineer's decision.
