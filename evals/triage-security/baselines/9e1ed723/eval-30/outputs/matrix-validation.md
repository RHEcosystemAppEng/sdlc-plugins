# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Execution mode**: Interactive (`FULLSEND_OUTPUT_DIR` is not set — Step 0.6)
**Issue stream scope**: `[rhtpa-2.2]` → **2.2.x** (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix file validated**: `evals/triage-security/files/security-matrix-missing-section-mock.md` (2.2.x stream matrix, `rhtpa-release.0.4.z`)
**Canonical template**: `docs/templates/security-matrix.template.md`

---

## Template extraction

**Required section headings** (from the template's `##` / `###` headings; `## Version Stream` is informational only and not enforced):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (template header row, in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Check 1 — Required sections present

| Required Section | Present in matrix? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | **FAIL — critical (non-repairable)** |
| `## Forward Pointer` | Yes | PASS |
| `## Version Stream` (informational, not enforced) | Yes | n/a |

The matrix file has no `## Ecosystem Mappings` heading at all. The sections it does contain are `## Version Stream`, `## Supportability Matrix`, `### Source Pinning Method`, and `## Forward Pointer`.

## Check 2 — Ecosystem Mappings column structure

| Expected | Actual | Result |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | *(no table — section missing)* | **Cannot validate** |

Column validation can't run because the Ecosystem Mappings section and its table are absent. This is already covered by the critical missing-section warning in Check 1.

## Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | — | — | — | **Cannot validate (section missing)** |

Supportability Matrix column names are product-specific, so only parsability is checked. The table parses correctly.

---

## Auto-repair evaluation

| Auto-repairable condition | Detected? | Action |
|---|---|---|
| Missing `## Forward Pointer` section | No | None |
| Extra whitespace in column headers | No | None |

**No auto-repairs apply.** A missing `## Ecosystem Mappings` section can't be auto-repaired. Its contents (ecosystem, repository, lock file, check command, upstream branch) are deployment-specific data that the skill must not invent. The matrix file was **not modified**, and no `security-matrix.md` write was made.

---

## Warnings (non-repairable — require user decision)

> ⚠️ Matrix file `evals/triage-security/files/security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Impact on the 2.2.x stream:**

- The Ecosystem Mappings table is where the skill finds the lock file path (e.g., `Cargo.lock`), the check command, and the upstream branch for each ecosystem. Without it:
  - Ecosystem detection for `quinn-proto` (Cargo) can't be confirmed against the stream's supported ecosystems. The skill reads the supported ecosystems from this table instead of assuming a fixed set.
  - Step 2.3 (lock file extraction at pinned commits `v0.4.5` / `v0.4.8`) can't determine which lock file to inspect or which command to run.
  - Step 2.5 (upstream fix status) can't determine which upstream branch to check.
- Under Step 2.1.1, the 2.2.x stream is a **critical-warning stream**. It is excluded from aggregation unless the matrix is fixed.
- 2.2.x is the stream TC-8001 is scoped to (`[rhtpa-2.2]`). If this stream is excluded, the version impact for the issue's own stream can't be determined, so Steps 3 (Affects Versions correction, currently `RHTPA 2.0.0`) and 8 (remediation) can't be completed for this issue.

---

## Overall validation result

**Status: WARNINGS** (non-repairable issues found — 1 critical warning)

| Stream | Matrix | Result |
|---|---|---|
| 2.2.x | `security-matrix-missing-section-mock.md` | **WARNING — critical: missing `## Ecosystem Mappings`. Stream cannot be processed.** |

### User decision required

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Triage is paused at this gate** until the engineer chooses. Choosing **1** removes 2.2.x from the aggregated working matrix. Because 2.2.x is the issue's scoped stream, the analysis could not produce a version impact result for TC-8001's own stream. **Recommended: option 2.** Add an `## Ecosystem Mappings` section to the 2.2.x matrix in the canonical format, then re-run triage. For example:

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |
```

(The real values must come from the rhtpa-backend repository and the Konflux release repo. They are left as template placeholders here so that no data is made up.)

---

## Other observations from earlier steps (for context)

- **Step 0.3 staleness:** the matrix has `Last-Updated: 2026-06-28T10:00:00Z`, which is 148 days old as of 2026-11-23 and well past the 14-day threshold. In a live run the engineer would first be offered Refresh / Proceed / Stop. A refresh (setup Step 10.6) could also add the missing Ecosystem Mappings section.
- **Security Configuration:** the Version Streams table has no `Security Matrix Path` column. The validated matrix was taken from the eval-supplied fixture for the 2.2.x stream. No matrix file was supplied for the 2.1.x stream (`rhtpa-release.0.3.z`), so that stream was not validated here.
- **Source Repositories:** there is no Deployment Context column, so `rhtpa-backend` defaults to `upstream`.
- No Jira, git, or external calls were made. All results above come only from the supplied input files.
