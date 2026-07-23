# Step 2.1.1 — Matrix Format Validation Results

Canonical template: `docs/templates/security-matrix.template.md`

## Template Reference (extracted requirements)

**Required section headings:**
- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

**Ecosystem Mappings required columns (in order):**
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

**Supportability Matrix columns:** product-specific, not validated against template (only parsability is checked).

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source:** `security-matrix-mock.md` — Stream 1 section

### 1. Required sections present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Table column structure (Ecosystem Mappings)

- **Expected:** `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual:** `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result:** PASS — columns match template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Present (`---` separators) | 2 data rows | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

### Auto-repairs applied

None required.

### Stream 1 overall result: PASS

No issues found. Proceed without user interruption.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source:** `security-matrix-mock.md` — Stream 2 section

### 1. Required sections present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Table column structure (Ecosystem Mappings)

- **Expected:** `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual:** `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result:** PASS — columns match template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Present (`---` separators) | 5 data rows | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Present (`---` separators) | 2 data rows (Cargo, RPM) | PASS |

### Auto-repairs applied

None required.

### Stream 2 overall result: PASS

No issues found. Proceed without user interruption.

---

## Validation Summary

| Stream | Sections | Ecosystem Columns | Table Parsability | Auto-repairs | Overall |
|---|---|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | PASS | PASS | PASS | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | PASS | PASS | PASS | None | PASS |

**Overall validation result: PASS** — All matrix files conform to the canonical template. No warnings or auto-repairs. Proceeding to matrix aggregation.
