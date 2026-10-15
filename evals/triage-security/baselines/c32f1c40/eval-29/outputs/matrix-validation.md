# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Reference

Loaded canonical template from `docs/templates/security-matrix.template.md`.

### Extracted required section headings

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced.

### Extracted Ecosystem Mappings column names (from template)

| Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|----------|----------|----------|----------|----------|
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |

---

## Validation: Stream 1 — rhtpa-release.0.3.z (2.1.x stream)

Matrix file: `security-matrix-mock.md` (Stream 1 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

All four required sections are present.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Column names match exactly, in the same order.

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present (contains `---`)
- Data rows: 2 rows (2.1.0, 2.1.1) — present

Result: parsable.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — present

Result: parsable.

### Stream 1 Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings.

---

## Validation: Stream 2 — rhtpa-release.0.4.z (2.2.x stream)

Matrix file: `security-matrix-mock.md` (Stream 2 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

All four required sections are present.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Column names match exactly, in the same order.

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present (contains `---`)
- Data rows: 5 rows (2.2.0 through 2.2.4) — present

Result: parsable.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — present

Result: parsable.

### Stream 2 Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings.

---

## Overall Validation Summary

| Stream | Matrix Source | Sections | Columns | Tables | Result |
|--------|-------------|----------|---------|--------|--------|
| 2.1.x (rhtpa-release.0.3.z) | security-matrix-mock.md | All 4 present | Match template | Both parsable | **Pass** |
| 2.2.x (rhtpa-release.0.4.z) | security-matrix-mock.md | All 4 present | Match template | Both parsable | **Pass** |

**Outcome**: All matrix files pass format validation. No warnings, no auto-repairs, no user prompt required. Proceeding silently to matrix aggregation.
