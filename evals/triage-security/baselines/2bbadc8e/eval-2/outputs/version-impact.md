# Version Impact Analysis -- Step 2

## CVE Details

- **CVE**: CVE-2026-28940
- **Library**: serde_json
- **Affected range**: versions before 1.0.135 (< 1.0.135)
- **Fixed version**: 1.0.135

## Version Impact Table

All supported product versions across both streams (2.1.x and 2.2.x) are checked, per the skill's requirement to check ALL supported versions regardless of issue stream scope.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | **NO** | Ships 1.0.137 >= 1.0.135 (fixed) |
| 2.1.1 | v0.3.12 | 1.0.137 | **NO** | Ships 1.0.137 >= 1.0.135 (fixed) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | **NO** | Ships 1.0.138 >= 1.0.135 (fixed) |
| 2.2.1 | v0.4.8 | 1.0.138 | **NO** | Ships 1.0.138 >= 1.0.135 (fixed) |
| 2.2.2 | v0.4.9 | 1.0.138 | **NO** | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | **NO** | Ships 1.0.139 >= 1.0.135 (fixed) |
| 2.2.4 | v0.4.12 | 1.0.139 | **NO** | Ships 1.0.139 >= 1.0.135 (fixed) |

## Summary

**No supported versions are affected.** Every shipped version of the backend component includes serde_json >= 1.0.135, which is at or above the fixed version threshold. The vulnerability (CVE-2026-28940, affecting serde_json < 1.0.135) does not apply to any released product version.

- Earliest serde_json version across all releases: **1.0.137** (in 2.1.x stream)
- Latest serde_json version across all releases: **1.0.139** (in 2.2.x stream)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold

## Dependency Chain Context (Step 2.3.5)

Not applicable -- no versions are affected, so no dependency chain analysis is needed for remediation purposes. The library serde_json is present in Cargo.lock across all versions but at a version that is already patched.

## Upstream Fix Status (Step 2.5)

Not applicable -- since no supported versions ship the vulnerable version of serde_json, upstream fix status is moot. All pinned commits already include a fixed version.
