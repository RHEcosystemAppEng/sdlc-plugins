# Version Impact Analysis -- CVE-2026-28940

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135** (fixed in 1.0.135).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | ships 1.0.137 >= 1.0.135 (fix threshold) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | ships 1.0.137 >= 1.0.135 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | ships 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | ships 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | ships 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | ships 1.0.139 >= 1.0.135 (fix threshold) |

## Summary

**All supported versions ship serde_json >= 1.0.135, which is at or above the fix threshold.**

- Stream 2.1.x: 0 of 2 versions affected (all ship 1.0.137)
- Stream 2.2.x: 0 of 5 versions affected (all ship 1.0.138 or 1.0.139)
- Total: 0 of 7 versions affected across all streams

No supported version ships a vulnerable version of serde_json (i.e., no version ships serde_json < 1.0.135).

This triggers **Step 8 Case C: No supported versions affected**.
