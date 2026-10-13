# Step 2.1.1 -- Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Template Reference (extracted from canonical template)

**Required section headings:**

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per the template specification.

**Ecosystem Mappings expected columns (in order):**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `security-matrix-mock.md` (Stream 1 section)
**Last-Updated timestamp**: `2026-06-28T10:00:00Z`

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS -- columns match exactly in name and order.

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---` separators) | 2 data rows (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix column names (`Version | Build | Build Date | backend | Notes`) differ from the template (`RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). This is expected -- per the specification, Supportability Matrix columns are product-specific and vary across deployments. Only parsability is validated, not column name matching.

### Auto-Repair Checks

- Missing `## Forward Pointer` section: Not applicable -- section is present.
- Extra whitespace in column headers: None detected.

### Stream 1 Overall Result: **PASS**

No issues found. No auto-repairs needed. No warnings.

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `security-matrix-mock.md` (Stream 2 section)
**Last-Updated timestamp**: `2026-06-28T10:00:00Z`

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS -- columns match exactly in name and order.

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---` separators) | 5 data rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix column names are product-specific (same as Stream 1). Only parsability is validated.

### Auto-Repair Checks

- Missing `## Forward Pointer` section: Not applicable -- section is present.
- Extra whitespace in column headers: None detected.

### Stream 2 Overall Result: **PASS**

No issues found. No auto-repairs needed. No warnings.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Auto-Repairs | Warnings | Overall |
|---|---|---|---|---|---|---|
| 2.1.x | PASS (4/4) | PASS | PASS (2/2 tables) | None | None | PASS |
| 2.2.x | PASS (4/4) | PASS | PASS (2/2 tables) | None | None | PASS |

**Outcome**: All matrix files pass format validation. Proceeding silently per the specification (no user interruption required for clean pass).
