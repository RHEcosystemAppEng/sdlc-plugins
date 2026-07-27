# Step 2.1.1 — Matrix Format Validation

## Canonical Template

Loaded canonical template from `docs/templates/security-matrix.template.md`.

**Required section headings extracted from template:**

| # | Section Heading | Level |
|---|-----------------|-------|
| 1 | Supportability Matrix | `##` |
| 2 | Ecosystem Mappings | `##` |
| 3 | Source Pinning Method | `###` |
| 4 | Forward Pointer | `##` |

**Ecosystem Mappings column names extracted from template:**

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation Results: Stream 2.2.x

**Matrix file:** `security-matrix-missing-section-mock.md` (rhtpa-release.0.4.z, 2.2.x stream)

### 1. Required Sections Check

| Required Section | Present? | Result |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `## Ecosystem Mappings` | **No** | **FAIL — critical warning** |
| `### Source Pinning Method` | Yes | Pass |
| `## Forward Pointer` | Yes | Pass |

### 2. Ecosystem Mappings Column Structure Check

Skipped — the `## Ecosystem Mappings` section is entirely absent from the matrix file. Column validation cannot be performed without the section.

### 3. Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|-----------|---------------|-----------|--------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 rows | Pass |
| Ecosystem Mappings | N/A | N/A | N/A | Skipped (section missing) |

### Auto-Repair Assessment

The missing `## Ecosystem Mappings` section is **NOT eligible for auto-repair**. Per Step 2.1.1, only the `## Forward Pointer` section may be auto-repaired (by appending with content `None`). The Ecosystem Mappings section is a critical data section required for lock file inspection and ecosystem detection — it cannot be safely synthesized.

---

## Warning

> **Warning:** Matrix file `security-matrix-missing-section-mock.md` is missing required section `Ecosystem Mappings`. This stream cannot be processed.
>
> Without the Ecosystem Mappings section, the triage skill cannot determine which lock files to inspect or which check commands to use for dependency version extraction. Version impact analysis for the 2.2.x stream is blocked.

---

## Validation Outcome: Warning (non-repairable issues found)

Matrix validation found issues that cannot be auto-repaired.

**Options:**

1. **Continue with partial data** — skip the 2.2.x stream (which has the critical warning) and proceed with triage using any remaining valid streams
2. **Abort triage** — halt triage to fix the matrix file first by adding the missing `## Ecosystem Mappings` section with the correct column structure (`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`) and at least one data row

Choose (1/2):

---

**Note:** If option 1 is chosen, the 2.2.x stream will be excluded from the version impact analysis in Step 2.3. Any versions belonging to this stream (2.2.0, 2.2.1) will not appear in the version impact table. This may result in an incomplete triage if the CVE affects versions in this stream.

If option 2 is chosen, the engineer should populate the Ecosystem Mappings section in the matrix file following the canonical template structure, then re-run triage.
