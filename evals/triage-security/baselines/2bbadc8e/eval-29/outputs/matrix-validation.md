# Step 2.1.1 -- Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Required Headings Extracted from Template

The following `##` and `###` level headings are required per the canonical template:

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced. `#### Container Images` is a `####` level heading and is not in scope for required-section validation.

## Ecosystem Mappings Template Columns

Expected column order: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

### 1. Required Sections Present

| Required Heading | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS -- exact column match in correct order

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 data rows | PASS |
| Ecosystem Mappings | Yes | Yes | 2 data rows (Cargo, RPM) | PASS |

### Auto-Repair Check

- Missing `## Forward Pointer`: No -- section present
- Extra whitespace in column headers: No -- headers are clean

### Stream 1 Overall Result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

### 1. Required Sections Present

| Required Heading | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS -- exact column match in correct order

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 5 data rows | PASS |
| Ecosystem Mappings | Yes | Yes | 2 data rows (Cargo, RPM) | PASS |

### Auto-Repair Check

- Missing `## Forward Pointer`: No -- section present
- Extra whitespace in column headers: No -- headers are clean

### Stream 2 Overall Result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Validation Summary

| Stream | Result | Warnings | Auto-Repairs |
|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | PASS | 0 | 0 |
| 2.2.x (rhtpa-release.0.4.z) | PASS | 0 | 0 |

**Overall**: Both matrix files pass format validation against the canonical template. All required sections are present, Ecosystem Mappings columns match the template in name and order, and all tables are parsable with valid header rows, separator rows, and data rows. No auto-repairs needed, no warnings to present.

Per Step 2.1.1 rules: when the result is Pass (no issues found), proceed silently without user interruption.

### Observations (informational, not validation findings)

- Neither matrix includes a `#### Container Images` section. This is not a validation finding because `####` headings are outside the `##`/`###` scope defined by Step 2.1.1. The Container Images section may be populated via on-demand matrix population if needed.
- The Supportability Matrix column headers (`Version | Build | Build Date | backend | Notes`) are product-specific as expected. Per Step 2.1.1, only table parsability is validated for the Supportability Matrix, not column names.
