# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 external CVE data enrichment:
- **Affected range**: h2 < 0.4.8
- **Fixed version**: h2 >= 0.4.8
- **Source**: MITRE CVE API and OSV.dev (cross-validated agreement)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (scoped stream -- issue [rhtpa-2.2])

| Version | Source Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same source commits) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

**Result: No 2.2.x versions are affected.** All versions in the scoped stream ship h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream)

| Version | Source Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |

**Result: All 2.1.x versions are affected.** Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

Dependency chain for h2:
- Ecosystem: Cargo (source dependency)
- Type: direct dependency (h2 is a direct dependency of the backend workspace)
- Profile: production (h2 is a runtime HTTP/2 dependency)

## Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | 0 | 5 (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) |
| 2.1.x (cross-stream) | 2 (2.1.0, 2.1.1) | 0 |

The scoped stream (2.2.x) is **not affected** -- all versions ship h2 >= 0.4.8.
The cross-stream (2.1.x) **is affected** -- all versions ship h2 0.4.5, which is below the fix threshold.

This cross-stream finding means the vulnerability does impact the product, but only in the 2.1.x stream, not in the 2.2.x stream that this issue (TC-8030) tracks.
