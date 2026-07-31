# Step 2 -- Version Impact Analysis

## Fix Threshold

**Enriched fix threshold from Step 1.5**: < **0.4.8** (cross-validated by MITRE CVE API and OSV.dev)

This threshold replaces the imprecise Jira description data ("versions prior to the fix"). All version comparisons below use the enriched value 0.4.8.

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.9 | -- | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |

## Impact Summary

- **Stream 2.2.x** (issue-scoped): **No versions affected.** All versions ship h2 >= 0.4.8 which is at or above the enriched fix threshold.
- **Stream 2.1.x** (out of issue scope): **All versions affected.** Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the 0.4.8 fix threshold.

## Comparison Method

All "Affected?" determinations use the **enriched fix threshold of 0.4.8** from Step 1.5 (cross-validated by MITRE CVE API `lessThan` field and OSV.dev `fixed` event), NOT the imprecise Jira description data which stated only "versions prior to the fix" with no version number.
