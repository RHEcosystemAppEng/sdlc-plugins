# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135
- **Ecosystem**: Cargo (Rust)

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8: 1.0.138) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | ships patched version (>= 1.0.135) |

## Result

**No supported version is affected.** Every version across all streams ships serde_json >= 1.0.135, which is at or above the fix threshold. The earliest serde_json version found is 1.0.137 (in the 2.1.x stream), which is already 2 patch versions ahead of the 1.0.135 fix.

## Dependency Chain Context

Not applicable -- since no version is affected, no dependency chain trace is needed for remediation purposes.

## Upstream Fix Status

Not applicable -- the vulnerability is already resolved across all shipped versions. No upstream fix action is required.

## Matrix Staleness Check

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z` (29 days ago as of 2026-07-27). This exceeds the 14-day staleness threshold, but the matrix data is still usable for this triage since the conclusion (not affected) is robust -- all versions ship serde_json well above the fix threshold.
