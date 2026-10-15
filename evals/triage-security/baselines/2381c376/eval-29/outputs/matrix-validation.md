# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Reference

Template: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

| # | Heading | Enforcement |
|---|---------|-------------|
| 1 | `## Version Stream` | Informational — NOT enforced |
| 2 | `## Supportability Matrix` | REQUIRED |
| 3 | `### Source Pinning Method` | REQUIRED |
| 4 | `## Ecosystem Mappings` | REQUIRED |
| 5 | `## Forward Pointer` | REQUIRED |

### Expected Ecosystem Mappings Columns (from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source**: Security Configuration Version Streams row for stream `2.1.x`

### Check 1 — Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

**Result**: PASS — all 4 required sections found.

### Check 2 — Ecosystem Mappings table column structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column count**: 5 (expected) vs 5 (actual)

**Result**: PASS — exact match in names and order.

### Check 3 — Table parsability

**Supportability Matrix**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — valid (contains `---`)
- Data rows: 2 rows (versions 2.1.0, 2.1.1) — at least one present
- Note: Column names differ from template (`Version` vs `RHTPA Version`, `backend` vs `trustify`/`trustify-ui`). Per 2.1.1 rules, Supportability Matrix columns are product-specific — validate parsability only, not column name match.

**Result**: PASS

**Ecosystem Mappings**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — valid (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — at least one present

**Result**: PASS

### Auto-repair actions

None required.

### Stream 1 Overall Result: PASS

No issues found. Proceed without user interruption.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source**: Security Configuration Version Streams row for stream `2.2.x`

### Check 1 — Required sections present

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

**Result**: PASS — all 4 required sections found.

### Check 2 — Ecosystem Mappings table column structure

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column count**: 5 (expected) vs 5 (actual)

**Result**: PASS — exact match in names and order.

### Check 3 — Table parsability

**Supportability Matrix**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — valid (contains `---`)
- Data rows: 5 rows (versions 2.2.0 through 2.2.4) — at least one present
- Note: Column names differ from template (product-specific). Per 2.1.1 rules, validate parsability only.

**Result**: PASS

**Ecosystem Mappings**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — valid (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — at least one present

**Result**: PASS

### Auto-repair actions

None required.

### Stream 2 Overall Result: PASS

No issues found. Proceed without user interruption.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Auto-repairs | Warnings | Overall |
|--------|-------------------|-------------------|-------------------|--------------|----------|---------|
| 2.1.x (rhtpa-release.0.3.z) | PASS (4/4) | PASS (exact match) | PASS (both tables) | None | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | PASS (4/4) | PASS (exact match) | PASS (both tables) | None | None | PASS |

**Overall validation outcome**: PASS — no issues found for either stream. Both matrix files conform to the canonical template structure. Proceeding silently to matrix aggregation per Step 2.1.1 rules (no user interruption needed when all checks pass).
