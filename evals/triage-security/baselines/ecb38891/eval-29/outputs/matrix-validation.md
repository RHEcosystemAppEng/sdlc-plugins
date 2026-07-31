# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Loaded

**Template path**: `docs/templates/security-matrix.template.md`

### Extracted required section headings

The following section headings were extracted from the canonical template:

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

(Note: `## Version Stream` is informational and not enforced per the validation rules.)

### Extracted Ecosystem Mappings column names (from template)

| Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|----------|----------|----------|----------|----------|
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |

---

## Matrix File Validation: Stream 2.1.x (rhtpa-release.0.3.z)

### Check 1: Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: **All required sections present.**

### Check 2: Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix file): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **Columns match the template exactly (same names, same order).**

### Check 3: Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` -- present
- Separator row: `|---------|-------|------------|---------|-------|` -- present (contains `---`)
- Data rows: 2 data rows (2.1.0, 2.1.1) -- at least one present

Result: **Parsable.**

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` -- present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` -- present (contains `---`)
- Data rows: 2 data rows (Cargo, RPM) -- at least one present

Result: **Parsable.**

### Stream 2.1.x Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings emitted.

---

## Matrix File Validation: Stream 2.2.x (rhtpa-release.0.4.z)

### Check 1: Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | Yes |
| `## Ecosystem Mappings` | Yes |
| `### Source Pinning Method` | Yes |
| `## Forward Pointer` | Yes |

Result: **All required sections present.**

### Check 2: Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix file): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **Columns match the template exactly (same names, same order).**

### Check 3: Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` -- present
- Separator row: `|---------|-------|------------|---------|-------|` -- present (contains `---`)
- Data rows: 5 data rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) -- at least one present

Result: **Parsable.**

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` -- present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` -- present (contains `---`)
- Data rows: 2 data rows (Cargo, RPM) -- at least one present

Result: **Parsable.**

### Stream 2.2.x Validation Result: **Pass**

No issues found. No auto-repairs needed. No warnings emitted.

---

## Overall Validation Summary

| Stream | Sections | Columns | Parsability | Result |
|--------|----------|---------|-------------|--------|
| 2.1.x (rhtpa-release.0.3.z) | All present | Match template | Both tables parsable | **Pass** |
| 2.2.x (rhtpa-release.0.4.z) | All present | Match template | Both tables parsable | **Pass** |

**Overall result: Pass** -- no warnings, no auto-repairs, no user prompt required.

Proceeding silently to aggregation. All versions from both streams are aggregated into a single working matrix for version impact analysis in Step 2.3.
