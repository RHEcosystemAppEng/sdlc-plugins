# Step 2.1.1 — Matrix Format Validation (TC-8001)

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `security-matrix-mock.md` (holds the matrix files for both configured streams)

## Template extraction

**Required section headings** (the `##`/`###` headings Step 2.1.1 enforces):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

`## Version Stream` is informational and not enforced. The template's `#### Container Images` heading is level 4, so this format check does not require it. Missing Container Images coverage is handled separately by on-demand matrix population.

**Expected Ecosystem Mappings columns, in order**:
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

The Supportability Matrix columns differ between products, so only its parsability is checked.

---

## Stream 1: 2.1.x — rhtpa-release.0.3.z

Matrix file: Stream 1 section of `security-matrix-mock.md` (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)

### Check 1 — Required sections present

| Required Section | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | Yes | |
| `### Source Pinning Method` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `## Forward Pointer` | Yes | "Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`" |
| `## Version Stream` (informational) | Yes | Covers **2.1.x** |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 found. Names and order match. No header has extra whitespace.

### Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.1.0, 2.1.1) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

### Result: **PASS**

- Auto-repairs: none needed
- Warnings: none
- Stream 1 is included in aggregation.

---

## Stream 2: 2.2.x — rhtpa-release.0.4.z

Matrix file: Stream 2 section of `security-matrix-mock.md` (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)

### Check 1 — Required sections present

| Required Section | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | Yes | |
| `### Source Pinning Method` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `## Forward Pointer` | Yes | "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | Yes | Covers **2.2.x** |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 found. Names and order match. No header has extra whitespace.

### Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 5 (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

### Result: **PASS**

- Auto-repairs: none needed
- Warnings: none
- Stream 2 is included in aggregation.

---

## Summary

| Stream | Konflux Release Repo | Sections | EM Columns | Tables Parsable | Result |
|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 4/4 | Match | Yes | **PASS** |
| 2.2.x | rhtpa-release.0.4.z | 4/4 | Match | Yes | **PASS** |

**Overall result: PASS.** No auto-repairs were proposed and no warnings were raised. Per Step 2.1.1, a Pass means the triage continues without asking the user. Nothing was written to either matrix file. Both streams go into the aggregated working matrix, which has 7 versions: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3 and 2.2.4.

### Observations (do not affect validation)

- The Supportability Matrix first column is `Version`, while the template uses `Product Version`. Step 2.1.1 deliberately does not check these columns, so this is not a finding.
- Neither matrix has a `#### Container Images` section. Step 2.1.1 does not enforce this. On-demand matrix population (after Step 2.1.1) would flag the missing image coverage separately. It was not run in this eval.
- The Version Streams table in the project CLAUDE.md has no `Security Matrix Path` column. The matrix contents come from the provided mock file, which stands in for the local file or the `git show main:<path>` fallback from each Konflux release repo.
