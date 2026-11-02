# Step 2.1.1 — Matrix Format Validation

## Template Reference

Canonical template loaded from: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

### Ecosystem Mappings Expected Columns (extracted from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Validation Results: Stream 2.2.x

**Matrix file**: `security-matrix-missing-section-mock.md` (rhtpa-release.0.4.z)

### Section Presence Check

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `## Ecosystem Mappings` | **NO — MISSING** |
| `### Source Pinning Method` | YES |
| `## Forward Pointer` | YES |

### Table Parsability Check

| Section | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 rows | YES |
| Ecosystem Mappings | — | — | — | **N/A — section missing** |

### Ecosystem Mappings Column Check

Column validation cannot be performed — the `## Ecosystem Mappings` section is entirely absent from the matrix file.

---

## Validation Result: **Warning** (non-repairable)

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

The missing `## Ecosystem Mappings` section is a **critical** structural issue. Without ecosystem mappings, the triage-security skill cannot determine:
- Which lock files to inspect for dependency version extraction (Step 2.3)
- Which check commands to use for each ecosystem
- Which upstream branches to verify for fix availability (Step 2.5)

### Auto-Repair Eligibility

This issue is **NOT eligible for auto-repair**. Only the `## Forward Pointer` section is eligible for auto-repair (appending with content `None`). Missing `## Supportability Matrix` or `## Ecosystem Mappings` sections are critical structural issues that require manual intervention.

### User Options

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. **Continue with partial data** — skip streams with critical warnings (stream 2.2.x will be excluded from version impact analysis)
> 2. **Abort triage** — stop triage to fix the matrix files first
>
> Choose (1/2):

Processing is halted for stream 2.2.x pending the user's decision. If the user chooses option 1, this stream is excluded from the aggregated matrix and version impact analysis proceeds with remaining valid streams only. If the user chooses option 2, triage stops entirely.
