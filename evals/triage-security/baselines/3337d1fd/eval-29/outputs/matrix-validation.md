# Step 2.1.1 — Matrix Format Validation Results

Canonical template: `docs/templates/security-matrix.template.md`

## Template Reference

**Required section headings** (extracted from template):
- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per the validation spec.

**Required Ecosystem Mappings columns** (from template):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source**: security-matrix-mock.md (Stream 1 section)

### 1. Required sections present

| Required Section | Present? | Status |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected columns: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Column count: 5 (expected 5) — **PASS**
Column names match: **PASS**
Column order matches: **PASS**

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present
- Data rows: 2 rows (2.1.0, 2.1.1) — present
- Result: **PASS**

Note: Supportability Matrix columns are product-specific (`Version | Build | Build Date | backend | Notes` vs template's `RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). Per spec, only parsability is validated, not column name matching.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present
- Data rows: 2 rows (Cargo, RPM) — present
- Result: **PASS**

### Auto-repairs applied

None required.

### Warnings

None.

### Stream 1 overall result: **PASS** — no issues found, proceed silently.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source**: security-matrix-mock.md (Stream 2 section)

### 1. Required sections present

| Required Section | Present? | Status |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected columns: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Column count: 5 (expected 5) — **PASS**
Column names match: **PASS**
Column order matches: **PASS**

### 3. Table parsability

**Supportability Matrix table:**
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present
- Data rows: 5 rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) — present
- Result: **PASS**

Note: Supportability Matrix columns are product-specific. Per spec, only parsability is validated.

**Ecosystem Mappings table:**
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present
- Data rows: 2 rows (Cargo, RPM) — present
- Result: **PASS**

### Auto-repairs applied

None required.

### Warnings

None.

### Stream 2 overall result: **PASS** — no issues found, proceed silently.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Auto-Repairs | Warnings | Result |
|---|---|---|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | 4/4 PASS | PASS | PASS | None | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | 4/4 PASS | PASS | PASS | None | None | PASS |

**Overall**: All matrix files pass validation. No auto-repairs needed, no warnings. Proceeding silently to matrix aggregation.
