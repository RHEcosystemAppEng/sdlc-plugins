# Step 2.1.1 — Matrix Format Validation Results

## Issue Context

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Canonical Template

Source: `docs/templates/security-matrix.template.md`

### Required section headings extracted from template

| # | Section Heading | Required |
|---|-----------------|----------|
| 1 | `## Supportability Matrix` | Yes |
| 2 | `### Source Pinning Method` | Yes |
| 3 | `## Ecosystem Mappings` | Yes |
| 4 | `## Forward Pointer` | Yes |

Note: `## Version Stream` is informational and not enforced.

### Ecosystem Mappings expected columns

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Validation: Stream 2.2.x (rhtpa-release.0.4.z)

Matrix file: `security-matrix-missing-section-mock.md`

### Section presence check

| Section Heading | Status |
|-----------------|--------|
| `## Supportability Matrix` | PASS - present |
| `### Source Pinning Method` | PASS - present |
| `## Ecosystem Mappings` | **MISSING** |
| `## Forward Pointer` | PASS - present |

### Table parsability check

| Section | Header Row | Separator Row | Data Rows | Status |
|---------|-----------|---------------|-----------|--------|
| `## Supportability Matrix` | Yes | Yes | 2 rows | PASS |
| `## Ecosystem Mappings` | N/A | N/A | N/A | **SKIPPED** - section missing |

### Auto-repairs applied

None. No auto-repairable issues detected. (The `## Forward Pointer` section is present, so no auto-repair needed.)

### Warnings

> **WARNING**: Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

The `## Ecosystem Mappings` section is entirely absent from the matrix file. This section is critical for version impact analysis -- it maps each dependency ecosystem to its lock file and inspection command. Without it, triage-security cannot determine which lock file to inspect or which check command to run for the quinn-proto package in the 2.2.x stream.

## Validation Summary

- **Result**: **Warnings** (non-repairable issues found)
- **Streams with critical warnings**: 2.2.x
- **Streams passing validation**: (none -- only one stream loaded)

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**Recommendation**: Abort triage (option 2) and add the Ecosystem Mappings section to the 2.2.x stream's security-matrix.md before re-running. The section should follow the canonical template format:

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | rhtpa-backend | `Cargo.lock` | `grep -A2 'name = "<package>"'` | `release/0.4.z` |
```
