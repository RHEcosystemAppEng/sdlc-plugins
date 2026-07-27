# Step 2.1.1 -- Matrix Format Validation

## Canonical Template Loaded

**Template path**: `docs/templates/security-matrix.template.md`

### Extracted Required Section Headings

The following section headings were extracted from the canonical template for validation:

| # | Section Heading | Level |
|---|-----------------|-------|
| 1 | Supportability Matrix | `##` |
| 2 | Ecosystem Mappings | `##` |
| 3 | Source Pinning Method | `###` |
| 4 | Forward Pointer | `##` |

Note: The `## Version Stream` heading is informational and not enforced per the skill specification.

### Extracted Ecosystem Mappings Column Names

The following column names were extracted from the template's Ecosystem Mappings table header row, in order:

| Position | Column Name |
|----------|-------------|
| 1 | Ecosystem |
| 2 | Repository |
| 3 | Lock File |
| 4 | Check Command |
| 5 | Upstream Branch |

---

## Validation Results

### Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Matrix file**: `security-matrix-mock.md` (Stream 1 section)

#### 1. Required Sections Present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

Result: All 4 required sections present.

#### 2. Ecosystem Mappings Column Structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: Column names match exactly, in the correct order.

#### 3. Table Parsability

| Table | Header Row? | Separator Row? | Data Rows? | Parsable? |
|-------|-------------|----------------|------------|-----------|
| Supportability Matrix | YES | YES | 2 data rows | YES |
| Ecosystem Mappings | YES | YES | 2 data rows | YES |

Result: Both tables are parsable with valid Markdown table syntax.

#### Stream 1 Validation Result: **PASS**

No issues found. No warnings, no auto-repairs required.

---

### Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-mock.md` (Stream 2 section)

#### 1. Required Sections Present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

Result: All 4 required sections present.

#### 2. Ecosystem Mappings Column Structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Actual columns (from matrix): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: Column names match exactly, in the correct order.

#### 3. Table Parsability

| Table | Header Row? | Separator Row? | Data Rows? | Parsable? |
|-------|-------------|----------------|------------|-----------|
| Supportability Matrix | YES | YES | 5 data rows | YES |
| Ecosystem Mappings | YES | YES | 2 data rows | YES |

Result: Both tables are parsable with valid Markdown table syntax.

#### Stream 2 Validation Result: **PASS**

No issues found. No warnings, no auto-repairs required.

---

## Overall Validation Summary

| Stream | Matrix Source | Result | Issues |
|--------|-------------|--------|--------|
| 2.1.x | security-matrix-mock.md (Stream 1) | PASS | None |
| 2.2.x | security-matrix-mock.md (Stream 2) | PASS | None |

**Overall result: PASS** -- All matrix files passed all structural checks. No warnings were emitted, no auto-repairs were applied, and no user prompt is required. Triage proceeds silently to version aggregation.
