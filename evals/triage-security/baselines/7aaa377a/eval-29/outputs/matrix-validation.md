# Step 2.1.1 — Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

### Extracted required section headings

| # | Required Section Heading |
|---|--------------------------|
| 1 | `## Supportability Matrix` |
| 2 | `## Ecosystem Mappings` |
| 3 | `### Source Pinning Method` |
| 4 | `## Forward Pointer` |

### Extracted Ecosystem Mappings column names (from template)

| Column Position | Column Name |
|-----------------|-------------|
| 1 | Ecosystem |
| 2 | Repository |
| 3 | Lock File |
| 4 | Check Command |
| 5 | Upstream Branch |

---

## Validation: Stream 2.1.x (rhtpa-release.0.3.z)

Matrix file: `security-matrix-mock.md` (Stream 1 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: All required sections present.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: Columns match the template exactly (same names, same order).

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` -- present
- Separator row: `|---------|-------|------------|---------|-------|` -- present (contains `---`)
- Data rows: 2 data rows (2.1.0, 2.1.1) -- at least one present

Result: Parsable.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` -- present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` -- present (contains `---`)
- Data rows: 2 data rows (Cargo, RPM) -- at least one present

Result: Parsable.

### Stream 2.1.x Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings.

---

## Validation: Stream 2.2.x (rhtpa-release.0.4.z)

Matrix file: `security-matrix-mock.md` (Stream 2 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: All required sections present.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: Columns match the template exactly (same names, same order).

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` -- present
- Separator row: `|---------|-------|------------|---------|-------|` -- present (contains `---`)
- Data rows: 5 data rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) -- at least one present

Result: Parsable.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` -- present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` -- present (contains `---`)
- Data rows: 2 data rows (Cargo, RPM) -- at least one present

Result: Parsable.

### Stream 2.2.x Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings.

---

## Overall Validation Summary

| Stream | Matrix Source | Sections | Columns | Tables | Result |
|--------|-------------|----------|---------|--------|--------|
| 2.1.x | security-matrix-mock.md (Stream 1) | All 4 present | Match template | Both parsable | **Pass** |
| 2.2.x | security-matrix-mock.md (Stream 2) | All 4 present | Match template | Both parsable | **Pass** |

**Overall result: Pass** -- no warnings, no auto-repairs, no user prompt required. Triage proceeds silently to aggregation (Step 2.1 matrix loading and version extraction).
