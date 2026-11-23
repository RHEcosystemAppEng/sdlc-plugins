# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812, quinn-proto)
**Template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `security-matrix-mock.md` (contains two stream matrices, validated independently)

## Template Extraction

**Required section headings** (per Step 2.1.1; `## Version Stream` is informational and not enforced):

| # | Heading | Level |
|---|---------|-------|
| 1 | `## Supportability Matrix` | `##` |
| 2 | `### Source Pinning Method` | `###` |
| 3 | `## Ecosystem Mappings` | `##` |
| 4 | `## Forward Pointer` | `##` |

**Expected Ecosystem Mappings columns** (exact names, in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 2.1.x — `rhtpa-release.0.3.z`

### Check 1: Required sections present

| Required Section | Present | Notes |
|------------------|---------|-------|
| `## Supportability Matrix` | Yes | |
| `### Source Pinning Method` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `## Forward Pointer` | Yes | Points to `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| `## Version Stream` (informational) | Yes | Not enforced |

### Check 2: Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: expected 5, actual 5. No whitespace anomalies in headers.

### Check 3: Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Parsable |
|-------|------------|-----------------------|-----------|----------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.1.0, 2.1.1) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

Supportability Matrix column names (`Version` instead of the template's `Product Version`) are product-specific and are not validated against the template, per Step 2.1.1.

### Result: **PASS**

No issues found. No auto-repairs needed. No warnings. Proceed silently.

---

## Stream 2.2.x — `rhtpa-release.0.4.z`

### Check 1: Required sections present

| Required Section | Present | Notes |
|------------------|---------|-------|
| `## Supportability Matrix` | Yes | |
| `### Source Pinning Method` | Yes | |
| `## Ecosystem Mappings` | Yes | |
| `## Forward Pointer` | Yes | "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | Yes | Not enforced |

### Check 2: Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: expected 5, actual 5. No whitespace anomalies in headers.

### Check 3: Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Parsable |
|-------|------------|-----------------------|-----------|----------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 5 (2.2.0 – 2.2.4) | Yes |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | Yes |

### Result: **PASS**

No issues found. No auto-repairs needed. No warnings. Proceed silently.

---

## Summary

| Stream | Matrix | Sections | Ecosystem Columns | Tables Parsable | Auto-Repairs | Warnings | Result |
|--------|--------|----------|-------------------|-----------------|--------------|----------|--------|
| 2.1.x | rhtpa-release.0.3.z | 4/4 | Match | Yes | None | None | **PASS** |
| 2.2.x | rhtpa-release.0.4.z | 4/4 | Match | Yes | None | None | **PASS** |

**Overall outcome**: Pass. Both streams proceed without user interruption to
aggregation. No auto-repair writes were proposed, so Local matrix write safety was
not triggered and no matrix file was modified.

**Aggregated working matrix** (7 versions across 2 streams):
2.1.0, 2.1.1 (2.1.x) and 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1 backend `v0.4.8`), 2.2.3, 2.2.4 (2.2.x).

## Observations Outside the Step 2.1.1 Checks (informational, do not change the result)

- **Container Images subsection absent**: the template has a `#### Container Images`
  subsection (level 4). It is not among the `##`/`###` headings that Step 2.1.1
  enforces, so its absence does not fail format validation. It is relevant to
  "On-demand matrix population" (missing `(Product Version, Component)` image rows),
  which is a separate step from format validation.
- **Staleness (Step 0.3)**: `Last-Updated: 2026-06-28T10:00:00Z` is 148 days old as of
  2026-11-23, exceeding the 14-day threshold. In an interactive run the engineer would
  be asked to refresh, proceed, or stop before reaching Step 2.1.1.
- **Security Matrix Path column**: the Version Streams table in the mock CLAUDE.md has
  no `Security Matrix Path` column. For this eval the matrix content was taken from the
  provided mock file instead of a configured path or a Konflux `git show` fallback.
