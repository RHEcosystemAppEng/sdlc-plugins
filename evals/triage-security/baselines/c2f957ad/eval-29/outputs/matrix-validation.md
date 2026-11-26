# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812, quinn-proto, `[rhtpa-2.2]`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent). Eval simulation: matrices come from `security-matrix-mock.md`, no `git show` or Jira calls made.

## Template extraction

**Required section headings** (the `##`/`###` headings enforced by Step 2.1.1):

| # | Heading | Level |
|---|---------|-------|
| 1 | `## Supportability Matrix` | 2 |
| 2 | `### Source Pinning Method` | 3 |
| 3 | `## Ecosystem Mappings` | 2 |
| 4 | `## Forward Pointer` | 2 |

Not enforced:
- `## Version Stream`: informational only, per Step 2.1.1.
- `#### Container Images`: level 4, so it is outside the `##`/`###` heading set.

**Expected Ecosystem Mappings columns, in order:**
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Supportability Matrix columns**: product-specific. Only parsability is checked, not the column names.

## Matrix files loaded

Both streams in the Security Configuration Version Streams table were enumerated directly. Forward pointers were not followed.

| Stream | Konflux Release Repo | Matrix source |
|--------|----------------------|---------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | security-matrix-mock.md, "Stream 1: rhtpa-release.0.3.z" |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | security-matrix-mock.md, "Stream 2: rhtpa-release.0.4.z" |

---

## Stream 2.1.x — `rhtpa-release.0.3.z`

### Check 1 — Required sections present

| Required heading | Present | Notes |
|------------------|---------|-------|
| `## Supportability Matrix` | YES | |
| `### Source Pinning Method` | YES | Has an entry for `backend` (`artifacts.lock.yaml`) |
| `## Ecosystem Mappings` | YES | |
| `## Forward Pointer` | YES | "Next stream: `2.2.x` at git.example.com/rhtpa/rhtpa-release.0.4.z" |

`## Version Stream` is present (informational): "covers the **2.1.x** product version stream".

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repository | YES |
| 3 | Lock File | Lock File | YES |
| 4 | Check Command | Check Command | YES |
| 5 | Upstream Branch | Upstream Branch | YES |

The column count (5) and order match exactly. Headers have no extra whitespace.

### Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Parsable |
|-------|-----------|-----------------------|-----------|----------|
| Supportability Matrix | YES (`Version \| Build \| Build Date \| backend \| Notes`) | YES | 2 (2.1.0, 2.1.1) | YES |
| Ecosystem Mappings | YES | YES | 2 (Cargo, RPM) | YES |

### Auto-repairs

None needed. The Forward Pointer section exists and the column headers have no extra whitespace.

### Warnings

None.

### Result: **PASS**: proceed silently

---

## Stream 2.2.x — `rhtpa-release.0.4.z`

### Check 1 — Required sections present

| Required heading | Present | Notes |
|------------------|---------|-------|
| `## Supportability Matrix` | YES | |
| `### Source Pinning Method` | YES | Has an entry for `backend` (`artifacts.lock.yaml`) |
| `## Ecosystem Mappings` | YES | |
| `## Forward Pointer` | YES | "This is the latest stream — no forward pointer." |

`## Version Stream` is present (informational): "covers the **2.2.x** product version stream".

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|----------|----------|--------|-------|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repository | YES |
| 3 | Lock File | Lock File | YES |
| 4 | Check Command | Check Command | YES |
| 5 | Upstream Branch | Upstream Branch | YES |

The column count (5) and order match exactly. Headers have no extra whitespace.

### Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Parsable |
|-------|-----------|-----------------------|-----------|----------|
| Supportability Matrix | YES (`Version \| Build \| Build Date \| backend \| Notes`) | YES | 5 (2.2.0 – 2.2.4; 2.2.2 is a backend retag of 2.2.1) | YES |
| Ecosystem Mappings | YES | YES | 2 (Cargo, RPM) | YES |

### Auto-repairs

None needed.

### Warnings

None.

### Result: **PASS**: proceed silently

---

## Summary

| Stream | Required sections | Ecosystem Mappings columns | Table parsability | Auto-repairs | Warnings | Result |
|--------|-------------------|----------------------------|-------------------|--------------|----------|--------|
| 2.1.x | 4/4 present | Exact match | Both parsable | None | None | **PASS** |
| 2.2.x | 4/4 present | Exact match | Both parsable | None | None | **PASS** |

**Overall outcome: PASS.** Both matrices conform to the canonical template, so the user is not prompted. Both streams go into the aggregated working matrix: 7 released versions in total (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4). No local `security-matrix.md` write is needed because no repair was applied.

## Informational observations (not Step 2.1.1 failures)

- **Supportability Matrix first column** is named `Version`, not `Product Version` as in the template. Step 2.1.1 treats Supportability Matrix columns as product-specific and does not validate them, so this is not a warning.
- **`#### Container Images` section is missing** from both matrices. Step 2.1.1 does not enforce it because it is a level-4 heading. However, the "On-demand matrix population" procedure treats a missing Container Images section as a reason to research and propose a matrix update, which requires engineer review before any write.
- **Security Matrix Path column** is missing from the CLAUDE.md Version Streams table. In this eval the matrix content was taken from the provided mock file.
- **Staleness (Step 0.3, context only)**: the mock file has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Against today's date (2026-11-26) that is 151 days old, well past the 14-day threshold. A staleness warning (Refresh now / Proceed anyway / Stop) would have been shown before Step 2.
