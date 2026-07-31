# Step 2.1.1 — Matrix Format Validation Results

## Template Reference

Canonical template loaded from: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1 spec.

### Ecosystem Mappings Columns (extracted from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation: Stream 2.1.x (rhtpa-release.0.3.z)

Matrix file: `security-matrix-mock.md` (Stream 1 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes (line 10) | PASS |
| `## Ecosystem Mappings` | Yes (line 21) | PASS |
| `### Source Pinning Method` | Yes (line 17) | PASS |
| `## Forward Pointer` | Yes (line 28) | PASS |

**Result: All 4 required sections present.**

### 2. Ecosystem Mappings Column Structure

| Expected Columns | Actual Columns | Match? |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | PASS |

**Result: Columns match template exactly, in the same order.**

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `\| Version \| Build \| Build Date \| backend \| Notes \|` | `\|-------\|-------\|----------\|-------\|-------\|` | 2 data rows | PASS |
| Ecosystem Mappings | `\| Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch \|` | `\|---------\|----------\|---------\|-------------\|---------------\|` | 2 data rows | PASS |

**Result: Both tables are parsable with valid Markdown table syntax.**

### Stream 2.1.x Validation Summary: PASS

- No warnings
- No auto-repairs needed
- No user prompt required

---

## Validation: Stream 2.2.x (rhtpa-release.0.4.z)

Matrix file: `security-matrix-mock.md` (Stream 2 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes (line 40) | PASS |
| `## Ecosystem Mappings` | Yes (line 54) | PASS |
| `### Source Pinning Method` | Yes (line 50) | PASS |
| `## Forward Pointer` | Yes (line 61) | PASS |

**Result: All 4 required sections present.**

### 2. Ecosystem Mappings Column Structure

| Expected Columns | Actual Columns | Match? |
|---|---|---|
| `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | PASS |

**Result: Columns match template exactly, in the same order.**

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `\| Version \| Build \| Build Date \| backend \| Notes \|` | `\|-------\|-------\|----------\|-------\|-------\|` | 5 data rows | PASS |
| Ecosystem Mappings | `\| Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch \|` | `\|---------\|----------\|---------\|-------------\|---------------\|` | 2 data rows | PASS |

**Result: Both tables are parsable with valid Markdown table syntax.**

### Stream 2.2.x Validation Summary: PASS

- No warnings
- No auto-repairs needed
- No user prompt required

---

## Overall Validation Result: PASS

All matrix files validated successfully against the canonical template. No warnings, no auto-repairs, no user prompts. Triage proceeds silently to aggregation.
