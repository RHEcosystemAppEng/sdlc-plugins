# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812, quinn-proto) `[rhtpa-2.2]`
**Template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent), simulated. No git, Jira, or external calls were made.

## Template Extraction

**Required section headings.** These are taken from the template's `##` and `###` headings, as Step 2.1.1 defines them:

| # | Heading | Level | Criticality if missing |
|---|---------|-------|------------------------|
| 1 | `Supportability Matrix` | `##` | Critical warning: stream cannot be processed |
| 2 | `Ecosystem Mappings` | `##` | Critical warning: stream cannot be processed |
| 3 | `Source Pinning Method` | `###` | Required |
| 4 | `Forward Pointer` | `##` | Auto-repairable: append with content `None` |

- `## Version Stream` is informational only. Step 2.1.1 does not enforce it.
- `#### Container Images` is a level-4 heading, so it is not one of the required headings. If it is missing, that is handled by on-demand matrix population, not by format validation.

**Expected Ecosystem Mappings columns, in order:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Supportability Matrix columns:** these are product-specific. Only parsability is checked: a header row, a separator row with `---`, and at least one data row. Column names are not compared against the template.

## Matrix Files Loaded

The Version Streams table in Security Configuration lists two streams. Both matrices come from the supplied `security-matrix-mock.md`, which holds one section per stream. Each section is validated separately below as that stream's matrix file.

| Stream | Konflux Release Repo | Source |
|--------|----------------------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | `security-matrix-mock.md`, section "Stream 1: rhtpa-release.0.3.z" |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | `security-matrix-mock.md`, section "Stream 2: rhtpa-release.0.4.z" |

Configuration note: the Version Streams table in `claude-md-security-config.md` has no `Security Matrix Path` column. Its columns are only Stream, Konflux Release Repo, and Local Path. The matrices were therefore taken from the supplied mock file. In a real run this gap would need resolving, either by adding the column with `/setup` or by using the Konflux fallback read.

---

## Stream 2.1.x — rhtpa-release.0.3.z

### Check 1: Required sections present

| Required heading | Found | Result |
|------------------|-------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |
| `## Version Stream` (informational) | Yes | n/a (not enforced) |

### Check 2: Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 actual. No extra whitespace in headers. **PASS**

### Check 3: Table parsability

| Table | Header row | Separator row | Data rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | Yes | 2 (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | PASS |

The first Supportability Matrix column is named `Version`, while the template uses `Product Version`. Supportability column names are product-specific and not validated, so this is not a finding.

### Auto-repairs

None needed.

### Warnings

None.

### Stream result: **PASS**

---

## Stream 2.2.x — rhtpa-release.0.4.z

### Check 1: Required sections present

| Required heading | Found | Result |
|------------------|-------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |
| `## Version Stream` (informational) | Yes | n/a (not enforced) |

### Check 2: Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | Yes |
| 2 | Repository | Repository | Yes |
| 3 | Lock File | Lock File | Yes |
| 4 | Check Command | Check Command | Yes |
| 5 | Upstream Branch | Upstream Branch | Yes |

Column count: 5 expected, 5 actual. No extra whitespace in headers. **PASS**

### Check 3: Table parsability

| Table | Header row | Separator row | Data rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | Yes | 5 (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 (Cargo, RPM) | PASS |

### Auto-repairs

None needed.

### Warnings

None.

### Stream result: **PASS**

---

## Summary

| Stream | Required sections | Ecosystem Mappings columns | Table parsability | Auto-repairs | Warnings | Result |
|--------|-------------------|----------------------------|-------------------|--------------|----------|--------|
| 2.1.x | 4/4 present | Exact match | Both tables valid | None | None | **PASS** |
| 2.2.x | 4/4 present | Exact match | Both tables valid | None | None | **PASS** |

**Overall outcome: PASS.** Step 2.1.1 says to proceed silently in this case, with no prompt to the user. No matrix file was modified, and no Local matrix write safety procedure was triggered. Both streams go into the aggregated working matrix:

- 2.1.x: 2.1.0, 2.1.1
- 2.2.x: 2.2.0, 2.2.1, 2.2.2 (backend retag of 2.2.1), 2.2.3, 2.2.4

Total: 7 product versions across 2 streams.

## Related Observations (outside Step 2.1.1 scope)

These do not affect the format-validation result. They are recorded here so they get dealt with in their own steps:

1. **Staleness (Step 0.3).** The matrix header shows `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so the matrix is 129 days old, well past the 14-day threshold. Step 0.3 requires a staleness warning with three options: Refresh now, Proceed anyway, or Stop.
2. **Container Images section absent (on-demand population).** Neither stream has the `#### Container Images` table. Format validation does not require it, but the on-demand matrix population procedure would flag the missing `(Product Version, Component)` image rows. Any proposed population must stay **NOT WRITTEN** until verified image evidence is available.
3. **Missing `Security Matrix Path` column** in the Version Streams configuration, as noted above.
