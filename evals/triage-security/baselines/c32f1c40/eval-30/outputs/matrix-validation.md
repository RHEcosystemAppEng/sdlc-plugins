# Step 2.1.1 -- Matrix Format Validation Results

## Canonical Template Reference

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

**Ecosystem Mappings columns extracted from template:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation: Stream 2.2.x

**Matrix file:** `security-matrix-missing-section-mock.md` (for Konflux release repo `rhtpa-release.0.4.z`)

### Section Presence Check

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `## Ecosystem Mappings` | **No** | **FAIL -- Missing** |
| `### Source Pinning Method` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### Table Parsability Check

| Section | Header Row | Separator Row | Data Rows | Status |
|---------|-----------|---------------|-----------|--------|
| `## Supportability Matrix` | Yes | Yes | 2 rows | Pass |
| `## Ecosystem Mappings` | N/A | N/A | N/A | Skipped (section missing) |

### Ecosystem Mappings Column Check

Skipped -- the `## Ecosystem Mappings` section is entirely absent from the matrix file. Column validation cannot be performed.

---

## Validation Result: WARNING (non-repairable)

The missing `## Ecosystem Mappings` section is a **critical** structural issue that **cannot be auto-repaired**. Only the `## Forward Pointer` section is eligible for auto-repair (appending with content `None`). The `## Ecosystem Mappings` section contains essential configuration data (ecosystem names, repository mappings, lock file paths, check commands, and upstream branch references) that cannot be inferred or generated automatically.

Without the Ecosystem Mappings section, the triage-security skill cannot:
- Determine which lock files to inspect for dependency versions
- Identify the correct check commands for extracting package versions
- Map ecosystems to their upstream branches for fix verification
- Classify the ecosystem type (source dependency vs. system package) for remediation task structure

**Processing for the 2.2.x stream is halted.**

### Warning Emitted

> WARNING: Matrix file `security-matrix-missing-section-mock.md` is missing required section `Ecosystem Mappings`. This stream cannot be processed.

### User Options

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** -- skip the 2.2.x stream and proceed with triage using only streams that have valid matrix files
2. **Abort triage** -- halt triage to fix the matrix files first (re-run `/setup` to populate the missing Ecosystem Mappings section)

Choose (1/2):

---

## Summary

| Stream | Matrix File | Validation Result | Action |
|--------|------------|-------------------|--------|
| 2.2.x | `security-matrix-missing-section-mock.md` | WARNING: missing `## Ecosystem Mappings` | Processing halted for this stream |

**Note:** The `## Supportability Matrix`, `### Source Pinning Method`, and `## Forward Pointer` sections are all present and valid. Only the `## Ecosystem Mappings` section is missing. This is not an auto-repairable issue -- the Ecosystem Mappings section contains user-specific configuration data that must be provided by the engineer or populated via `/setup`.
