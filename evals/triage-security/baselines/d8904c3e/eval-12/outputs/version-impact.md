# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 **< 0.4.8** is affected (fix threshold: 0.4.8).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- |
| 2.2.x (issue scope) | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

## Key Findings

1. **Issue-scoped stream (2.2.x): NOT affected.** All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold. The earliest 2.2.x version (2.2.0, tag v0.4.5) already ships h2 0.4.8.

2. **Cross-stream impact (2.1.x): AFFECTED.** Both 2.1.x versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

3. **Retag handling**: Version 2.2.2 (tag v0.4.9) is a retag of 2.2.1 (tag v0.4.8) -- lock file check skipped, result carried forward from 2.2.1.

## Dependency Chain Context

The h2 crate is a Cargo dependency in the backend repository. Based on the ecosystem mappings, the lock file is `Cargo.lock` and the upstream branch for 2.1.x is `release/0.3.z` and for 2.2.x is `release/0.4.z`.

Ecosystem: Cargo (source dependency)
Remediation type: 2 tasks per affected stream (upstream backport + downstream propagation)
