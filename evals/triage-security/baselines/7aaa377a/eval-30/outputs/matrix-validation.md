# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Reference

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

| # | Required Section | Level |
|---|------------------|-------|
| 1 | Supportability Matrix | `##` |
| 2 | Ecosystem Mappings | `##` |
| 3 | Source Pinning Method | `###` |
| 4 | Forward Pointer | `##` |

**Ecosystem Mappings expected columns (from template):**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream: 2.2.x

**Matrix file path:** `docs/security-matrix-2.2.x.md` (loaded from fixture `security-matrix-missing-section-mock.md`)

### Section Presence Check

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `## Ecosystem Mappings` | **No** | **CRITICAL WARNING** |
| `### Source Pinning Method` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 rows | Pass |
| Ecosystem Mappings | N/A | N/A | N/A | **Skipped — section missing** |

### Ecosystem Mappings Column Check

Skipped — the `## Ecosystem Mappings` section is entirely absent from the matrix file. Column validation cannot proceed without the section.

### Auto-Repair Assessment

The missing `## Ecosystem Mappings` section is **not eligible for auto-repair**. Only the `## Forward Pointer` section qualifies for auto-repair (appending with content `None`). The Ecosystem Mappings section is a critical data section containing lock file paths and check commands required for version impact analysis — it cannot be safely generated or defaulted.

---

## Validation Result: WARNING (non-repairable)

> **Warning:** Matrix file `docs/security-matrix-2.2.x.md` is missing required section `Ecosystem Mappings`. This stream cannot be processed.

The `Ecosystem Mappings` section is required for version impact analysis (Step 2.3). Without it, the skill cannot determine which lock files to inspect or which check commands to use for dependency version extraction. Processing is halted for the 2.2.x stream.

---

## User Decision Required

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** — skip the 2.2.x stream and proceed with triage using any remaining valid streams
2. **Abort triage** — halt triage so the matrix file can be fixed first (re-run `/setup` to populate the Ecosystem Mappings section)

Choose (1/2):
