# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Template**: `docs/templates/security-matrix.template.md`
**Date**: 2026-08-24

## Template Reference

Required section headings extracted from the canonical template:

| # | Required Heading | Enforced? |
|---|------------------|-----------|
| 1 | `## Supportability Matrix` | Yes (critical) |
| 2 | `### Source Pinning Method` | Yes |
| 3 | `## Ecosystem Mappings` | Yes (critical) |
| 4 | `## Forward Pointer` | Yes (auto-repairable if missing) |

Note: `## Version Stream` is informational and not enforced per the template specification.

Expected Ecosystem Mappings columns (from template):

```
Ecosystem | Repository | Lock File | Check Command | Upstream Branch
```

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `security-matrix-mock.md` (Stream 1 section)
**Last-Updated**: 2026-06-28T10:00:00Z (57 days ago — exceeds 14-day staleness threshold)

### 1. Required Sections Present

| Required Section | Status |
|------------------|--------|
| `## Supportability Matrix` | PRESENT |
| `### Source Pinning Method` | PRESENT |
| `## Ecosystem Mappings` | PRESENT |
| `## Forward Pointer` | PRESENT |

Result: All required sections found.

### 2. Ecosystem Mappings Column Structure

| Check | Result |
|-------|--------|
| Expected columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Actual columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Column count | 5 (expected 5) |
| Column order | Matches template |

Result: PASS — columns match the canonical template exactly.

### 3. Table Parsability

**Supportability Matrix:**

| Check | Result |
|-------|--------|
| Header row | Present (`Version \| Build \| Build Date \| backend \| Notes`) |
| Separator row | Present (contains `---`) |
| Data rows | 2 rows (2.1.0, 2.1.1) |

Note: Supportability Matrix column names are product-specific (`Version`, `backend` vs template's `RHTPA Version`, `trustify`, `trustify-ui`). Per the validation spec, only parsability is checked for this table, not column name matching.

Result: PASS — valid Markdown table with header, separator, and data rows.

**Ecosystem Mappings:**

| Check | Result |
|-------|--------|
| Header row | Present |
| Separator row | Present (contains `---`) |
| Data rows | 2 rows (Cargo, RPM) |

Result: PASS — valid Markdown table with header, separator, and data rows.

### Stream 1 Overall: PASS

No auto-repairs needed. No warnings.

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `security-matrix-mock.md` (Stream 2 section)
**Last-Updated**: 2026-06-28T10:00:00Z (57 days ago — exceeds 14-day staleness threshold)

### 1. Required Sections Present

| Required Section | Status |
|------------------|--------|
| `## Supportability Matrix` | PRESENT |
| `### Source Pinning Method` | PRESENT |
| `## Ecosystem Mappings` | PRESENT |
| `## Forward Pointer` | PRESENT |

Result: All required sections found.

### 2. Ecosystem Mappings Column Structure

| Check | Result |
|-------|--------|
| Expected columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Actual columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` |
| Column count | 5 (expected 5) |
| Column order | Matches template |

Result: PASS — columns match the canonical template exactly.

### 3. Table Parsability

**Supportability Matrix:**

| Check | Result |
|-------|--------|
| Header row | Present (`Version \| Build \| Build Date \| backend \| Notes`) |
| Separator row | Present (contains `---`) |
| Data rows | 5 rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) |

Note: Supportability Matrix column names are product-specific. Only parsability is validated.

Result: PASS — valid Markdown table with header, separator, and data rows.

**Ecosystem Mappings:**

| Check | Result |
|-------|--------|
| Header row | Present |
| Separator row | Present (contains `---`) |
| Data rows | 2 rows (Cargo, RPM) |

Result: PASS — valid Markdown table with header, separator, and data rows.

### Stream 2 Overall: PASS

No auto-repairs needed. No warnings.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Overall |
|--------|-------------------|-------------------|-------------------|---------|
| 2.1.x (rhtpa-release.0.3.z) | PASS (4/4) | PASS (5/5 match) | PASS (all tables valid) | PASS |
| 2.2.x (rhtpa-release.0.4.z) | PASS (4/4) | PASS (5/5 match) | PASS (all tables valid) | PASS |

**Auto-repairs applied**: None
**Warnings**: None
**Staleness**: Both streams have Last-Updated timestamp of 2026-06-28 (57 days ago), which exceeds the 14-day staleness threshold. Staleness is handled in Step 0.3 (separate from format validation).

**Conclusion**: Both matrix files pass format validation. Proceeding silently to matrix aggregation per the validation spec (no user interruption needed for PASS results).
