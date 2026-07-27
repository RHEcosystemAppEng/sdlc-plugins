# Step 2.1.1 — Matrix Format Validation Results

**Canonical template**: `docs/templates/security-matrix.template.md`

## Template Reference

**Required section headings** (extracted from template):
1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1 rules.

**Ecosystem Mappings expected columns** (from template):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

**Result**: All 4 required sections present — PASS

### 2. Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column count**: 5 (expected 5)
- **Column order**: matches template

**Result**: Ecosystem Mappings columns match template exactly — PASS

Note: Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) differ from the template's placeholder columns (`RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). Per Step 2.1.1 rules, Supportability Matrix columns are product-specific and vary across deployments — only parsability is validated, not column name matching.

### 3. Table Parsability

**Supportability Matrix**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present (contains `---`)
- Data rows: 2 rows (2.1.0, 2.1.1) — present

**Result**: Valid Markdown table syntax — PASS

**Ecosystem Mappings**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — present

**Result**: Valid Markdown table syntax — PASS

### Auto-Repair Actions

None required — no missing sections or whitespace issues detected.

### Stream 1 Overall: PASS

No issues found. Proceed silently.

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

**Result**: All 4 required sections present — PASS

### 2. Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Column count**: 5 (expected 5)
- **Column order**: matches template

**Result**: Ecosystem Mappings columns match template exactly — PASS

Note: Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) differ from the template's placeholder columns. Per Step 2.1.1 rules, only parsability is validated for Supportability Matrix columns.

### 3. Table Parsability

**Supportability Matrix**:
- Header row: `| Version | Build | Build Date | backend | Notes |` — present
- Separator row: `|---------|-------|------------|---------|-------|` — present (contains `---`)
- Data rows: 5 rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) — present

**Result**: Valid Markdown table syntax — PASS

**Ecosystem Mappings**:
- Header row: `| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |` — present
- Separator row: `|-----------|------------|-----------|---------------|-----------------|` — present (contains `---`)
- Data rows: 2 rows (Cargo, RPM) — present

**Result**: Valid Markdown table syntax — PASS

### Auto-Repair Actions

None required — no missing sections or whitespace issues detected.

### Stream 2 Overall: PASS

No issues found. Proceed silently.

---

## Validation Summary

| Stream | Required Sections | Ecosystem Columns | Table Parsability | Auto-Repairs | Warnings | Overall |
|---|---|---|---|---|---|---|
| 2.1.x | PASS (4/4) | PASS | PASS | None | None | PASS |
| 2.2.x | PASS (4/4) | PASS | PASS | None | None | PASS |

**Outcome**: All matrix files pass validation. No auto-repairs needed. No warnings. Proceeding with version impact analysis.
