# Step 2.1.1 — Matrix Format Validation

## Template Reference

Canonical template loaded from: `docs/templates/security-matrix.template.md`

### Required section headings extracted from template

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

### Ecosystem Mappings column names extracted from template

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |

---

## Validation: Stream 1 — rhtpa-release.0.3.z (2.1.x)

Matrix file: `docs/security-matrix-2.1.x.md` (mock: `security-matrix-mock.md`, Stream 1 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

All required sections found.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Match**: Column names and order match the template exactly.

### 3. Table parsability

**Supportability Matrix table**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present
- Data rows: 2 rows (2.1.0, 2.1.1) — present
- **Parsable**: YES

**Ecosystem Mappings table**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present
- Data rows: 2 rows (Cargo, RPM) — present
- **Parsable**: YES

### Stream 1 Result: **Pass**

---

## Validation: Stream 2 — rhtpa-release.0.4.z (2.2.x)

Matrix file: `docs/security-matrix-2.2.x.md` (mock: `security-matrix-mock.md`, Stream 2 section)

### 1. Required sections present

| Required Section | Present? |
|------------------|----------|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | YES |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

All required sections found.

### 2. Ecosystem Mappings column structure

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Match**: Column names and order match the template exactly.

### 3. Table parsability

**Supportability Matrix table**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present
- Data rows: 5 rows (2.2.0 through 2.2.4) — present
- **Parsable**: YES

**Ecosystem Mappings table**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present
- Data rows: 2 rows (Cargo, RPM) — present
- **Parsable**: YES

### Stream 2 Result: **Pass**

---

## Overall Validation Result: **Pass**

No issues found across either stream. No auto-repairs needed, no warnings emitted, no user prompt required. Triage proceeds silently to matrix aggregation.
