# Step 2.1.1 — Matrix Format Validation Results

## Issue: TC-8001

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Affected range**: versions before 0.11.14
**Fixed version**: 0.11.14

## Canonical Template Reference

Template: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

| # | Required Section | Enforced? |
|---|------------------|-----------|
| 1 | `## Supportability Matrix` | Yes (critical) |
| 2 | `### Source Pinning Method` | Yes |
| 3 | `## Ecosystem Mappings` | Yes (critical) |
| 4 | `## Forward Pointer` | Yes (auto-repairable if missing) |
| 5 | `## Version Stream` | No (informational only) |

## Validation: Stream 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-missing-section-mock.md` (local path for stream 2.2.x)

### Section Presence Check

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | **CRITICAL WARNING** |
| `## Forward Pointer` | Yes | PASS |

### Table Parsability Check

| Section | Header Row? | Separator Row? | Data Rows? | Status |
|---------|-------------|----------------|------------|--------|
| `## Supportability Matrix` | Yes | Yes | 2 rows | PASS |
| `## Ecosystem Mappings` | N/A | N/A | N/A | SKIPPED (section missing) |

### Ecosystem Mappings Column Check

Skipped -- the `## Ecosystem Mappings` section is entirely absent from the matrix file. Column structure cannot be validated.

### Auto-Repairs Applied

None. No auto-repairable issues detected (the `## Forward Pointer` section is already present).

## Warnings

> **WARNING**: Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`. This stream cannot be processed.

The `## Ecosystem Mappings` section is critical for version impact analysis. Without it, the triage-security skill cannot determine:
- Which lock file to inspect for the vulnerable dependency
- Which check command to use for dependency version extraction
- Which upstream branch to verify for fix availability

This is a non-auto-repairable issue. The matrix file must be updated to include the `## Ecosystem Mappings` section before triage can proceed for the 2.2.x stream.

## Validation Summary

| Stream | Matrix File | Result | Blocking Issues |
|--------|-------------|--------|-----------------|
| 2.2.x | `security-matrix-missing-section-mock.md` | **FAIL** | Missing `## Ecosystem Mappings` section |

## Recommended Action

Matrix validation found issues that cannot be auto-repaired.

1. **Continue with partial data** (skip streams with critical warnings)
2. **Abort triage** to fix the matrix files first

The 2.2.x stream cannot be processed until the `## Ecosystem Mappings` section is added to its security matrix file. The section should follow the canonical template format:

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | rhtpa-backend | `Cargo.lock` | `grep -A2 'name = "<library>"'` | `release/0.4.z` |
```

Without this section, dependency version extraction (Step 2.3), dependency chain tracing (Step 2.3.5), and upstream fix checking (Step 2.5) cannot proceed for this stream.
