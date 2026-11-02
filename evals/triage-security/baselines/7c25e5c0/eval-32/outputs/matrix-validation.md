# Step 2.1.1 — Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Ecosystem Mappings columns extracted from template:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Validation: Stream 2.2.x (rhtpa-release.0.4.z)

Matrix file: `docs/security-matrix-2.2.x.md` (loaded from configured Security Matrix Path)

### 1. Required sections present

| Required Section | Status |
|------------------|--------|
| `## Supportability Matrix` | Present |
| `## Ecosystem Mappings` | Present |
| `### Source Pinning Method` | Present |
| `## Forward Pointer` | **MISSING** |

### 2. Table column structure (Ecosystem Mappings)

Expected columns (from template): `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual columns (from matrix):     `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **Match** — columns are identical in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Parsable? |
|-------|-----------|---------------|-----------|-----------|
| Supportability Matrix | Present | Present | 2 rows | Yes |
| Ecosystem Mappings | Present | Present | 1 row | Yes |

### Auto-Repair Applied

- **Missing `## Forward Pointer` section**: appended the section to the end of the matrix with content `None`.

Log: "Auto-repaired: appended missing Forward Pointer section to `docs/security-matrix-2.2.x.md`."

The proposed repaired matrix now ends with:

```markdown
## Forward Pointer

None
```

### Validation Result: **Repaired**

Only auto-fixable issues were found (missing Forward Pointer — eligible for auto-repair per Step 2.1.1). The auto-repair was applied and logged. No user prompt is required — triage proceeds silently to aggregation.

No warnings (missing critical sections, wrong columns, unparsable tables) were detected. The matrix is structurally valid after the auto-repair.
