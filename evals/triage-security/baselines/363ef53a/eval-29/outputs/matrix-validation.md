# Step 2.1.1 — Matrix Format Validation Results

**Canonical template**: `docs/templates/security-matrix.template.md`

**Required section headings** (extracted from template):
1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Required Ecosystem Mappings columns** (extracted from template):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Table column structure (Ecosystem Mappings)

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — columns match in name and order

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | `---` separators present | 2 data rows | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | `---` separators present | 2 data rows (Cargo, RPM) | PASS |

### Auto-repairs applied

None required.

### Warnings

None.

### Stream 1 overall: PASS

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | YES | PASS |
| `## Ecosystem Mappings` | YES | PASS |
| `### Source Pinning Method` | YES | PASS |
| `## Forward Pointer` | YES | PASS |

### 2. Table column structure (Ecosystem Mappings)

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — columns match in name and order

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | `---` separators present | 5 data rows | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | `---` separators present | 2 data rows (Cargo, RPM) | PASS |

### Auto-repairs applied

None required.

### Warnings

None.

### Stream 2 overall: PASS

---

## Validation Summary

| Stream | Sections | Columns | Parsability | Auto-repairs | Warnings | Overall |
|--------|----------|---------|-------------|--------------|----------|---------|
| 2.1.x | 4/4 PASS | PASS | PASS | None | None | PASS |
| 2.2.x | 4/4 PASS | PASS | PASS | None | None | PASS |

**Outcome**: All matrix files pass format validation. No issues found — proceeding silently per Step 2.1.1 rules (no user interruption required when all checks pass).

### Notes

- The Supportability Matrix column names (`Version | Build | Build Date | backend | Notes`) are product-specific and differ from the template's placeholder columns (`RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). Per Step 2.1.1 rules, Supportability Matrix columns are validated only for parsability, not for column name matching against the template. Both streams have valid parsable tables.
- Both streams include the optional `## Version Stream` section, which is informational and not enforced by validation.
- The `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) is present in the file header and is 101 days old as of 2026-10-07 — this staleness is handled by Step 0.3, not by Step 2.1.1 format validation.
