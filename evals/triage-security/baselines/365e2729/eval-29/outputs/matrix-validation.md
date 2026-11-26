# Step 2.1.1 — Matrix Format Validation (TC-8001)

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (FULLSEND_OUTPUT_DIR absent), eval simulation (no Jira / git calls)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `evals/triage-security/files/security-matrix-mock.md` (contains both stream matrices, one per Version Streams row)

## Template extraction

**Required section headings** (`##` / `###` headings from the template; `## Version Stream` is informational and not enforced; `#### Container Images` is level 4 and is not part of the heading check):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Ecosystem Mappings columns, in order, from the template header row**:

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Supportability Matrix**: columns are product-specific, so only parsability is checked (header row, separator row containing `---`, and at least one data row).

---

## Stream 2.1.x — `rhtpa-release.0.3.z`

Configured Konflux repo: `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path `/home/dev/repos/rhtpa-release.0.3.z`)

### Check 1 — Required sections present

| Required Heading | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | YES | |
| `## Ecosystem Mappings` | YES | |
| `### Source Pinning Method` | YES | |
| `## Forward Pointer` | YES | "Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`" |
| `## Version Stream` (informational) | YES | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repository | YES |
| 3 | Lock File | Lock File | YES |
| 4 | Check Command | Check Command | YES |
| 5 | Upstream Branch | Upstream Branch | YES |

Column count: 5 expected, 5 actual. No extra header whitespace found.

### Check 3 — Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | YES | 2 (2.1.0, 2.1.1) | YES |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | YES | 2 (Cargo, RPM) | YES |

### Auto-repairs

None needed (Forward Pointer present, headers have no extra whitespace).

### Result: **PASS**

---

## Stream 2.2.x — `rhtpa-release.0.4.z`

Configured Konflux repo: `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path `/home/dev/repos/rhtpa-release.0.4.z`)

### Check 1 — Required sections present

| Required Heading | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | YES | |
| `## Ecosystem Mappings` | YES | |
| `### Source Pinning Method` | YES | |
| `## Forward Pointer` | YES | "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | YES | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repository | YES |
| 3 | Lock File | Lock File | YES |
| 4 | Check Command | Check Command | YES |
| 5 | Upstream Branch | Upstream Branch | YES |

Column count: 5 expected, 5 actual. No extra header whitespace found.

### Check 3 — Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | YES | 5 (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | YES |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | YES | 2 (Cargo, RPM) | YES |

### Auto-repairs

None needed.

### Result: **PASS**

---

## Validation Summary

| Stream | Matrix | Sections | Ecosystem Mappings Columns | Tables Parsable | Auto-repairs | Warnings | Result |
|---|---|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 4/4 | Exact match (5/5, in order) | YES | None | None | **PASS** |
| 2.2.x | rhtpa-release.0.4.z | 4/4 | Exact match (5/5, in order) | YES | None | None | **PASS** |

**Outcome**: Both matrices pass, so per Step 2.1.1 the skill continues without asking the user anything. No files were written: no repair was needed, so the local matrix write-safety procedure did not run. Both streams go into the aggregated working matrix: 7 released versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 [backend retag of 2.2.1], 2.2.3, 2.2.4).

## Observations outside the Step 2.1.1 checks (informational, do not change the result)

- **Supportability Matrix first column** is `Version`, while the template uses `Product Version`. Step 2.1.1 does not check Supportability Matrix column names because they are product-specific, so this is not a failure.
- **`#### Container Images` section is absent** from both matrices. It is a level-4 heading, so the Step 2.1.1 heading check skips it. Step 2.1 "On-demand matrix population" does flag it as missing, which would trigger a population proposal in a live interactive run. That step requires release/image evidence and a confirmed write, and this eval did neither.
- **Staleness (Step 0.3)**: `Last-Updated: 2026-06-28T10:00:00Z` is 151 days before today (2026-11-26), well past the 14-day threshold. A live run would show the Refresh / Proceed / Stop prompt for each stream before reaching this step. The timestamp sits once at the top of the combined mock file, so it applies to both streams.
- **Version Streams table** in the mock CLAUDE.md has no `Security Matrix Path` column. For this eval, the per-stream matrices were taken from the combined mock file instead of per-stream paths.
