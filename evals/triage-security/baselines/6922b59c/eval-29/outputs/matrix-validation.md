# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Reference

Template loaded from: `docs/templates/security-matrix.template.md`

### Required section headings (## and ### level)

| # | Heading | Level |
|---|---------|-------|
| 1 | `## Supportability Matrix` | `##` |
| 2 | `### Source Pinning Method` | `###` |
| 3 | `## Ecosystem Mappings` | `##` |
| 4 | `## Forward Pointer` | `##` |

Note: `## Version Stream` is informational and not enforced per the skill specification.

### Expected Ecosystem Mappings columns

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected columns: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **PASS** -- columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes (`---` separators) | 2 data rows (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | Yes (`Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`) | Yes (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix column names are product-specific and vary across deployments. Per the skill specification, only parsability is validated, not column name matching against the template.

### Auto-repair proposals

None required.

### Warnings

None.

### Stream 1 overall result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected columns: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **PASS** -- columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes (`---` separators) | 5 data rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | Yes (`Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`) | Yes (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

Note: Supportability Matrix column names are product-specific and vary across deployments. Per the skill specification, only parsability is validated, not column name matching against the template.

### Auto-repair proposals

None required.

### Warnings

None.

### Stream 2 overall result: **PASS**

No issues found. Proceed silently without user interruption.

---

## Aggregate Validation Summary

| Stream | Sections | Columns | Parsability | Auto-repairs | Warnings | Overall |
|--------|----------|---------|-------------|--------------|----------|---------|
| 2.1.x (rhtpa-release.0.3.z) | PASS | PASS | PASS | None | None | **PASS** |
| 2.2.x (rhtpa-release.0.4.z) | PASS | PASS | PASS | None | None | **PASS** |

**Disposition**: Both streams pass format validation. Proceed to matrix aggregation without user interruption.

### Notable observations

- Neither stream includes a `#### Container Images` subsection. This is a `####`-level heading and is not among the enforced `##`/`###`-level required headings per the validation specification. On-demand matrix population (Step 2.1 on-demand population procedure) would address missing Container Images data if needed.
- Both streams use `Version` rather than `Product Version` as the first Supportability Matrix column header. This is acceptable because Supportability Matrix columns are product-specific and the validation only checks parsability, not column name matching.
- The `## Version Stream` heading is present in both streams but is informational and not enforced by the validation.
