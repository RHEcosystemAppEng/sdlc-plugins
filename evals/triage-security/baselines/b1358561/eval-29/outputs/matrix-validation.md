# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812, quinn-proto)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `security-matrix-mock.md` (contains two stream matrices, validated independently)

## Template-derived validation criteria

**Required section headings** (extracted from template; `## Version Stream` is informational and not enforced):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (exact names, exact order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Table parsability**: Supportability Matrix and Ecosystem Mappings tables must each have a header row, a separator row (containing `---`), and at least one data row. Supportability Matrix column names are product-specific and are NOT compared against the template.

---

## Stream 1: 2.1.x — `rhtpa-release.0.3.z`

Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`

### Check 1 — Required sections present

| Required Section | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `### Source Pinning Method` | Yes | Entry for `backend` (artifacts.lock.yaml) |
| `## Forward Pointer` | Yes | Points to 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| `## Version Stream` (informational) | Yes | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 actual. No whitespace anomalies in headers.

### Check 3 — Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.1.0, 2.1.1) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

Note: Supportability Matrix uses `Version` instead of the template's `Product Version` as its first column. Per Step 2.1.1, Supportability Matrix columns are product-specific and are not validated against the template — this is not a finding.

### Auto-repairs

None required (Forward Pointer present; no column-header whitespace issues).

### Warnings

None.

### Result: **PASS** — stream 2.1.x proceeds to aggregation silently.

---

## Stream 2: 2.2.x — `rhtpa-release.0.4.z`

Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`

### Check 1 — Required sections present

| Required Section | Present | Notes |
|---|---|---|
| `## Supportability Matrix` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `### Source Pinning Method` | Yes | Entry for `backend` (artifacts.lock.yaml) |
| `## Forward Pointer` | Yes | "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | Yes | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 actual. No whitespace anomalies in headers.

### Check 3 — Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 5 (2.2.0 – 2.2.4) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

Note: as with 2.1.x, the `Version` vs `Product Version` header difference in the Supportability Matrix is product-specific and not a finding. Row 2.2.2 is a backend retag of 2.2.1 (`v0.4.8`), recorded in Notes — structurally valid.

### Auto-repairs

None required.

### Warnings

None.

### Result: **PASS** — stream 2.2.x proceeds to aggregation silently.

---

## Summary

| Stream | Konflux Release Repo | Required Sections | Ecosystem Columns | Tables Parsable | Auto-Repairs | Warnings | Result |
|---|---|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 4/4 | Match | Yes | 0 | 0 | **PASS** |
| 2.2.x | rhtpa-release.0.4.z | 4/4 | Match | Yes | 0 | 0 | **PASS** |

**Overall: PASS.** Both matrices conform to the canonical template structure. No user prompt is required (per Step 2.1.1, Pass results proceed silently). Both streams are included in the aggregated working matrix: 7 product versions total (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4).

### Informational observations (outside the Step 2.1.1 pass/fail checks)

- **No `#### Container Images` section** in either matrix. The template includes it at heading level 4, so it is not one of the four headings Step 2.1.1 requires and does not affect the validation result. The On-demand matrix population step would flag the missing Container Images coverage separately. That step was not run in this eval because it needs Konflux/registry access and matrix writes.
- **No `<!-- Last-Updated: ... -->` timestamp** in either matrix file. Under Step 0.3 this produces a non-blocking advisory to run `/setup` to add a timestamp. It is not a format-validation failure.
- The Version Streams table in the project CLAUDE.md has no `Security Matrix Path` column. For this eval, both matrices were loaded from the provided mock file rather than from per-stream configured paths. No Konflux fallback (`git show`) was run.
- No matrix files were modified. No writes were needed because no auto-repairs applied.
