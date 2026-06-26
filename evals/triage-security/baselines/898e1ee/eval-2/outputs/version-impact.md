# Step 2 -- Version Impact Analysis: CVE-2026-28940 (serde_json < 1.0.135)

## Supportability Matrix Sources

- Stream 2.1.x: `rhtpa-release.0.3.z` security-matrix.md
- Stream 2.2.x: `rhtpa-release.0.4.z` security-matrix.md

## Version Impact Table

All supported versions across both streams are analyzed, even though the issue is scoped to 2.2.x, to provide complete impact visibility.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Fix threshold (1.0.135) | Affected? | Notes |
|---------|-----------|-------------------|------------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | >= 1.0.135 | NO | Ships patched version |
| 2.1.1 | v0.3.12 | 1.0.137 | >= 1.0.135 | NO | Ships patched version |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scope

| Version | Build Tag | serde_json version | Fix threshold (1.0.135) | Affected? | Notes |
|---------|-----------|-------------------|------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | >= 1.0.135 | NO | Ships patched version |
| 2.2.1 | v0.4.8 | 1.0.138 | >= 1.0.135 | NO | Ships patched version |
| 2.2.2 | v0.4.9 | 1.0.138 | >= 1.0.135 | NO | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | >= 1.0.135 | NO | Ships patched version |
| 2.2.4 | v0.4.12 | 1.0.139 | >= 1.0.135 | NO | Ships patched version |

## Summary

**No supported versions are affected.** Every supported version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.135, which is at or above the fix threshold.

- Earliest serde_json version shipped: **1.0.137** (in 2.1.0 and 2.1.1)
- Latest serde_json version shipped: **1.0.139** (in 2.2.3 and 2.2.4)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 patch versions

The vulnerable version range (serde_json < 1.0.135) does not overlap with any version shipped in any supported product release.
