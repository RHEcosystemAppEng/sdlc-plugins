# Step 2.1.1 — Matrix Format Validation Results

## Canonical Template Reference

Template: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

| # | Section Heading | Level | Required |
|---|-----------------|-------|----------|
| 1 | `## Supportability Matrix` | H2 | Yes |
| 2 | `## Ecosystem Mappings` | H2 | Yes |
| 3 | `### Source Pinning Method` | H3 | Yes |
| 4 | `## Forward Pointer` | H2 | Yes (auto-repairable if missing) |

Note: `## Version Stream` is informational and not enforced.

---

## Stream: 2.2.x

**Matrix file**: `security-matrix-missing-section-mock.md`
**Last-Updated**: 2026-06-28T10:00:00Z (33 days ago — exceeds 14-day staleness threshold, but staleness is a Step 0.3 concern, not a format validation blocker)

### Section Presence Check

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | **FAIL — CRITICAL WARNING** |
| `### Source Pinning Method` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Status |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 rows (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | N/A — section missing | N/A | N/A | **FAIL — section not present** |

### Auto-Repair Eligibility

Per Step 2.1.1 rules, only the following issues are eligible for auto-repair:

| Issue Type | Eligible for Auto-Repair? |
|------------|--------------------------|
| Missing `## Forward Pointer` section | Yes — append with content `None` |
| Extra whitespace in column headers | Yes — normalize by trimming |
| Missing `## Supportability Matrix` | **No — critical section, requires user decision** |
| Missing `## Ecosystem Mappings` | **No — critical section, requires user decision** |

The missing `## Ecosystem Mappings` section is **NOT eligible for auto-repair**. Only the `## Forward Pointer` section can be auto-repaired. The Ecosystem Mappings section contains configuration data (lock file paths, check commands, upstream branches) that cannot be generated without user input.

### Validation Outcome: WARNING (non-repairable)

> **WARNING**: Matrix file `security-matrix-missing-section-mock.md` is missing required section `Ecosystem Mappings`.
> This stream cannot be processed.

Without the Ecosystem Mappings section, the triage-security skill cannot:
- Determine which lock file to inspect for dependency version extraction (Step 2.3)
- Identify the check command to run against lock files
- Look up the upstream branch for fix status checks (Step 2.5)
- Classify the ecosystem for remediation task structure (Step 8)

**Processing for the 2.2.x stream is halted.**

---

## Validation Summary

| Stream | Matrix File | Result | Issues |
|--------|-------------|--------|--------|
| 2.2.x | `security-matrix-missing-section-mock.md` | **WARNING** | Missing required section: `Ecosystem Mappings` |

### User Decision Required

Matrix validation found issues that cannot be auto-repaired.

> 1. **Continue with partial data** — skip the 2.2.x stream (which has critical warnings) and proceed with any remaining valid streams
> 2. **Abort triage** — halt triage to fix the matrix files first
>
> Choose (1/2):

**Note**: Since the issue TC-8001 is scoped to the 2.2.x stream (per summary suffix `[rhtpa-2.2]`), choosing option 1 would effectively skip the only relevant stream, leaving no streams to analyze. The recommended action is option 2: abort triage and populate the Ecosystem Mappings section in the matrix file before re-running.
