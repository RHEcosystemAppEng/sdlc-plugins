# Step 2 — Version Impact Analysis: TC-8001

## CVE Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo (lock file: `Cargo.lock`)

## Version Impact Table

### Stream 2.2.x (issue scope: rhtpa-release.0.4.z)

| Version | Build | Build Date | Pinned Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|------------|------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | 0.11.12 | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

### Stream 2.1.x (cross-stream: rhtpa-release.0.3.z)

| Version | Build | Build Date | Pinned Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|------------|------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

## Summary

- **2.2.x stream** (issue scope): Versions 2.2.0, 2.2.1, and 2.2.2 are affected. The vulnerability was fixed starting in version 2.2.3 (build 0.4.11), which upgraded quinn-proto to 0.11.14.
- **2.1.x stream** (cross-stream): All versions (2.1.0, 2.1.1) are affected. quinn-proto remains at 0.11.9 across all 2.1.x builds, which is below the fix threshold of 0.11.14.

## First Fixed Version

The fix was first introduced in **2.2.3** (build 0.4.11, tag `v0.4.11`), which ships quinn-proto 0.11.14.

## Cross-Stream Impact

Stream 2.1.x is also affected but is outside this issue's scope (scoped to 2.2.x). Cross-stream impact will be reported in Step 7.
