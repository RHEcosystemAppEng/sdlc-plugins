# Step 2 -- Version Impact Analysis for CVE-2026-48901

## Enriched Fix Threshold

- Library: h2
- Affected range: < 0.4.8 (from Step 1.5 cross-validated external CVE data)
- Fixed version: 0.4.8

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Tag | h2 Version | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Stream Affected? |
|--------|-------------------|-----------------------|------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- | YES |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NO |

## Scoped Stream Analysis (2.2.x)

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

Within the scoped stream, **no versions are affected**. All versions in the 2.2.x
stream ship h2 >= 0.4.8, which is at or above the fix threshold.

- 2.2.0 ships h2 0.4.8 (exactly the fix version)
- 2.2.1 ships h2 0.4.8
- 2.2.2 is a retag of 2.2.1 (same h2 version)
- 2.2.3 ships h2 0.4.9
- 2.2.4 ships h2 0.4.9

## Cross-Stream Impact

The 2.1.x stream IS affected (h2 0.4.5 < 0.4.8 for both 2.1.0 and 2.1.1).
However, the 2.1.x stream is outside this issue's scope. Cross-stream impact
is tracked by companion issues per PSIRT's per-stream Vulnerability tracking.
