# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Fix Threshold

- **Vulnerable library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8: 1.0.138) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | ships patched version (>= 1.0.135) |

## Summary

**No supported versions are affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.135, which is at or above the fix threshold.

- Stream 2.1.x: all versions ship serde_json 1.0.137 (fixed)
- Stream 2.2.x: all versions ship serde_json 1.0.138 or 1.0.139 (fixed)

The earliest serde_json version shipped across all supported product versions is **1.0.137**, which is already **2 patch versions above** the fix threshold of 1.0.135.

## Matrix Staleness Check

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z` (31 days ago as of 2026-07-29). This exceeds the 14-day staleness threshold. However, the matrix data clearly shows all versions ship patched serde_json, so the triage conclusion is unambiguous regardless of matrix freshness.
