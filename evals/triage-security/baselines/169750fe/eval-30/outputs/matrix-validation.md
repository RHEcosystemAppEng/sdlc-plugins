# Step 2.1.1 — Matrix Format Validation Results

## Template Reference

Canonical template: `docs/templates/security-matrix.template.md`

### Required section headings extracted from template

| # | Heading | Level |
|---|---------|-------|
| 1 | `## Supportability Matrix` | `##` |
| 2 | `## Ecosystem Mappings` | `##` |
| 3 | `### Source Pinning Method` | `###` |
| 4 | `## Forward Pointer` | `##` |

### Ecosystem Mappings expected columns

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file:** `security-matrix-missing-section-mock.md`

### Section presence check

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | Pass |
| `## Ecosystem Mappings` | **No** | **CRITICAL WARNING** |
| `### Source Pinning Method` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### Table parsability check

| Section | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 | Pass |
| Ecosystem Mappings | N/A | N/A | N/A | **Skipped (section missing)** |

### Auto-repairs applied

None. The missing `## Ecosystem Mappings` section is **not eligible for auto-repair**. Only `## Forward Pointer` is eligible for auto-repair (append with content `None`). Missing critical sections (`## Supportability Matrix` and `## Ecosystem Mappings`) require user decision.

### Warnings

> **WARNING:** Matrix file `security-matrix-missing-section-mock.md` is missing required section `Ecosystem Mappings`. This stream cannot be processed.

Without the Ecosystem Mappings section, the skill cannot determine lock file paths, check commands, or upstream branches for any ecosystem in this stream. Version impact analysis (Step 2.3) and upstream fix checks (Step 2.5) are blocked for this stream.

---

## Validation Summary

| Stream | Result | Details |
|---|---|---|
| 2.2.x | **Warning** | Missing required section: `Ecosystem Mappings` |

## Overall Result: **Warnings** (non-repairable issues)

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** -- skip streams with critical warnings (stream 2.2.x will be excluded from version impact analysis)
2. **Abort triage** -- halt triage to fix the matrix files first

Choose (1/2):
