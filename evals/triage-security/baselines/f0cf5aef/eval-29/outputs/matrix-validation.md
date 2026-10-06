# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template

Loaded from: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced.

### Ecosystem Mappings Columns (extracted from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `### Source Pinning Method` | Yes | Pass |
| `## Ecosystem Mappings` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### 2. Ecosystem Mappings column structure

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **Pass** — columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | Pass |
| Ecosystem Mappings | Yes | Yes | 2 | Pass |

### Stream 1 Overall: **Pass** — no issues found.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `### Source Pinning Method` | Yes | Pass |
| `## Ecosystem Mappings` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### 2. Ecosystem Mappings column structure

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **Pass** — columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 5 | Pass |
| Ecosystem Mappings | Yes | Yes | 2 | Pass |

### Stream 2 Overall: **Pass** — no issues found.

---

## Summary

| Stream | Required Sections | Column Structure | Table Parsability | Overall |
|--------|-------------------|------------------|-------------------|---------|
| 2.1.x (rhtpa-release.0.3.z) | Pass | Pass | Pass | **Pass** |
| 2.2.x (rhtpa-release.0.4.z) | Pass | Pass | Pass | **Pass** |

**Auto-repairs performed**: None
**Warnings**: None

**Result: Pass** — All matrix files passed validation with no warnings. Proceeding to matrix aggregation.
