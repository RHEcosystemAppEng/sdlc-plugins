# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001
**CVE**: CVE-2026-31812
**Canonical template**: `docs/templates/security-matrix.template.md`

## Required Sections (from template, ## and ### level headings)

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1 rules.

---

## Stream 1: rhtpa-release.0.3.z (2.1.x stream)

### Section Presence Check

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### Ecosystem Mappings Column Structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — exact match in name and order

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 rows | PASS |
| Ecosystem Mappings | Yes (`Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`) | Yes | 2 rows (Cargo, RPM) | PASS |

### Auto-Repair Actions

None required.

### Overall Result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x stream)

### Section Presence Check

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### Ecosystem Mappings Column Structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — exact match in name and order

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 5 rows | PASS |
| Ecosystem Mappings | Yes (`Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`) | Yes | 2 rows (Cargo, RPM) | PASS |

### Auto-Repair Actions

None required.

### Overall Result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Validation Summary

| Stream | Sections | Columns | Parsability | Auto-Repairs | Overall |
|---|---|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | PASS | PASS | PASS | None | **PASS** |
| 2.2.x (rhtpa-release.0.4.z) | PASS | PASS | PASS | None | **PASS** |

**Conclusion**: Both matrix files pass format validation. All required sections are present, Ecosystem Mappings columns match the canonical template exactly (in name and order), and all tables are well-formed with valid header rows, separator rows, and data rows. No auto-repairs needed, no warnings to present. Proceeding to matrix aggregation.
