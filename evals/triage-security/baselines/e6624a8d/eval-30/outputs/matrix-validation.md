# Step 2.1.1 — Matrix Format Validation

## Template Reference

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Ecosystem Mappings column names extracted from template:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation Results: Stream 2.2.x

**Matrix file:** `security-matrix-missing-section-mock.md` (stream rhtpa-release.0.4.z / 2.2.x)

### 1. Required Sections Check

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | **NO** |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

### 2. Table Column Structure (Ecosystem Mappings)

Skipped — the `## Ecosystem Mappings` section is missing entirely, so no table to validate.

### 3. Table Parsability

- **Supportability Matrix**: Parsable — header row, separator row (`---`), and 2 data rows present.
- **Ecosystem Mappings**: Skipped — section missing.

---

## Validation Outcome: **Warning**

The missing `## Ecosystem Mappings` section is a critical structural issue. This section
is required for version impact analysis (Step 2.3) — without it, the skill cannot determine
which lock file to inspect or which check command to use for dependency version extraction.

**This is NOT eligible for auto-repair.** Only the `## Forward Pointer` section qualifies
for auto-repair (appending with content `None`). The `## Ecosystem Mappings` section
contains product-specific configuration data (ecosystem names, repository mappings, lock
file paths, check commands, and upstream branches) that cannot be generated automatically.

### Warning

> **Warning:** Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

### User Options

Matrix validation found issues that cannot be auto-repaired.

> 1. **Continue with partial data** — skip the 2.2.x stream (it will be excluded from version impact analysis)
> 2. **Abort triage** — stop triage to fix the matrix file first (add the Ecosystem Mappings section with the correct column structure)
>
> Choose (1/2):
