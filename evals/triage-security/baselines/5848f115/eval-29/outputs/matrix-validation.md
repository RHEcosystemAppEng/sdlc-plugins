# Step 2.1.1 — Matrix Format Validation Results

**CVE**: CVE-2026-31812
**Issue**: TC-8001
**Validation date**: 2026-07-29

## Canonical Template Reference

Template loaded from: `docs/templates/security-matrix.template.md`

**Required section headings extracted from template:**
1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1 rules.

**Ecosystem Mappings columns extracted from template:**
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `security-matrix-mock.md` (Stream 1 section)
**Last-Updated timestamp**: `2026-06-28T10:00:00Z` (31 days ago -- STALE, exceeds 14-day threshold)

### 1. Required Sections Present

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column match**: PASS (exact match in order and naming)

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---` separators) | 2 data rows | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) differ from the template's columns (`RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). This is expected -- per Step 2.1.1 rules, Supportability Matrix columns are product-specific and vary across deployments. Only parsability is validated, not column name matching.

### Auto-Repair Actions

None required.

### Stream 1 Result: **PASS** (no format issues found)

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `security-matrix-mock.md` (Stream 2 section)
**Last-Updated timestamp**: `2026-06-28T10:00:00Z` (31 days ago -- STALE, exceeds 14-day threshold)

### 1. Required Sections Present

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column match**: PASS (exact match in order and naming)

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---` separators) | 5 data rows | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix columns are product-specific (same rationale as Stream 1). Only parsability validated.

### Auto-Repair Actions

None required.

### Stream 2 Result: **PASS** (no format issues found)

---

## Validation Summary

| Stream | Sections | Columns | Parsability | Auto-Repairs | Overall |
|--------|----------|---------|-------------|--------------|---------|
| 2.1.x (rhtpa-release.0.3.z) | PASS (4/4) | PASS | PASS (2/2 tables) | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | PASS (4/4) | PASS | PASS (2/2 tables) | None | PASS |

**Overall validation result**: PASS -- both matrix files conform to the canonical template structure. No warnings, no auto-repairs needed.

**Staleness note**: Both streams share a Last-Updated timestamp of 2026-06-28T10:00:00Z, which is 31 days old and exceeds the 14-day staleness threshold. Per Step 0.3, the user would be prompted to choose: refresh now, proceed anyway, or stop. This staleness concern is separate from the format validation performed here.

**Proceeding**: Both streams are structurally valid and can be aggregated into the working matrix for Step 2.3 dependency version extraction.
