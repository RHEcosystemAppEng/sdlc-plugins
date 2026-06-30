# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5 external CVE data enrichment:
- **Source**: MITRE CVE API and OSV.dev (agreement)
- **Threshold**: h2 < 0.4.8 is affected; h2 >= 0.4.8 is not affected

Note: The Jira description provided only imprecise data ("versions prior to the fix" / "see advisory"). The enriched threshold from external CVE databases is used instead.

## 2.1 -- Supportability Matrix

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Stream 2.1.x (rhtpa-release.0.3.z) -- out-of-scope (cross-stream check)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

## 2.3 -- Dependency Version Extraction (h2)

Using enriched fix threshold: h2 < 0.4.8 (from Step 1.5)

### Stream 2.2.x (issue-scoped)

| Version | backend tag | h2 version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (above fix threshold) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (above fix threshold) |

### Stream 2.1.x (cross-stream check)

| Version | backend tag | h2 version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | out-of-scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.4.5 | YES | out-of-scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | above fix threshold |
| 2.2.4 | 2.2.x | 0.4.9 | NO | above fix threshold |

## Summary

- **Stream 2.2.x (issue-scoped)**: NO versions affected. All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.
- **Stream 2.1.x (cross-stream)**: ALL versions affected. Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Triage Outcome

Since this issue is scoped to stream 2.2.x (per the `[rhtpa-2.2]` suffix) and NO 2.2.x versions are affected, this falls under **Case C: No supported versions affected**.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

All 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold (< 0.4.8). The vulnerability does not affect any version in the issue's scoped stream.

VEX Justification (since customfield_12345 is configured): **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version.

### Cross-stream impact note

Stream 2.1.x IS affected (h2 0.4.5 in versions 2.1.0 and 2.1.1). This cross-stream impact should be noted:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x is tracked by a companion issue or may require separate PSIRT triage.
