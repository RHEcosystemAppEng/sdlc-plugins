# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Template Reference

**Required section headings** (extracted from canonical template):
1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1 rules.

**Required Ecosystem Mappings columns** (from template, in order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source file**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Table Column Structure (Ecosystem Mappings)

| Check | Result |
|-------|--------|
| Expected columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Actual columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Column count match | Yes (5 expected, 5 actual) |
| Column names match | Yes (exact match in order) |
| **Result** | **PASS** |

### 3. Table Parsability

**Supportability Matrix table:**

| Check | Result |
|-------|--------|
| Header row present | Yes (`\| Version \| Build \| Build Date \| backend \| Notes \|`) |
| Separator row present | Yes (`\|---------|-------|------------|---------|-------\|`) |
| Data rows (minimum 1) | Yes (2 data rows: 2.1.0, 2.1.1) |
| **Result** | **PASS** |

Note: Supportability Matrix column names (`Version`, `Build`, `Build Date`, `backend`, `Notes`) differ from the template's column names (`RHTPA Version`, `Build`, `Build Date`, `trustify`, `trustify-ui`, `Notes`). This is expected — per Step 2.1.1, Supportability Matrix columns are product-specific and vary across deployments; only parsability is validated, not column name matching.

**Ecosystem Mappings table:**

| Check | Result |
|-------|--------|
| Header row present | Yes |
| Separator row present | Yes |
| Data rows (minimum 1) | Yes (2 data rows: Cargo, RPM) |
| **Result** | **PASS** |

### Auto-Repair Actions

None required. No missing `## Forward Pointer` section or extra whitespace in column headers detected.

### Stream 1 Overall Result: **PASS**

No issues found. Proceeding without user interruption.

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source file**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Table Column Structure (Ecosystem Mappings)

| Check | Result |
|-------|--------|
| Expected columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Actual columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Column count match | Yes (5 expected, 5 actual) |
| Column names match | Yes (exact match in order) |
| **Result** | **PASS** |

### 3. Table Parsability

**Supportability Matrix table:**

| Check | Result |
|-------|--------|
| Header row present | Yes (`\| Version \| Build \| Build Date \| backend \| Notes \|`) |
| Separator row present | Yes (`\|---------|-------|------------|---------|-------\|`) |
| Data rows (minimum 1) | Yes (5 data rows: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) |
| **Result** | **PASS** |

Note: Same product-specific column name differences as Stream 1 — expected and not enforced per Step 2.1.1.

**Ecosystem Mappings table:**

| Check | Result |
|-------|--------|
| Header row present | Yes |
| Separator row present | Yes |
| Data rows (minimum 1) | Yes (2 data rows: Cargo, RPM) |
| **Result** | **PASS** |

### Auto-Repair Actions

None required. No missing `## Forward Pointer` section or extra whitespace in column headers detected.

### Stream 2 Overall Result: **PASS**

No issues found. Proceeding without user interruption.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Auto-Repairs | Warnings | Overall |
|--------|-------------------|-------------------|-------------------|--------------|----------|---------|
| 2.1.x | PASS (4/4) | PASS (exact match) | PASS (all tables valid) | None | None | **PASS** |
| 2.2.x | PASS (4/4) | PASS (exact match) | PASS (all tables valid) | None | None | **PASS** |

**Outcome**: All matrix files pass validation. No auto-repairs performed, no warnings issued. Both streams are valid for aggregation into the working matrix for version impact analysis.
