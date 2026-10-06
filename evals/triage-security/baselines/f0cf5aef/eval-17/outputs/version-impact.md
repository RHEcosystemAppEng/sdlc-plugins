# Step 2 -- Version Impact Analysis

## Vulnerability Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo (lock file: `Cargo.lock`)
- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)

## Stream 2.2.x (rhtpa-release.0.4.z) -- In Scope

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|-------------|---------------------|-----------|----------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.8 | _(same as 2.2.1)_ | **YES** | retag of v0.4.8; 0.11.12 < 0.11.14 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

**Stream 2.2.x summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable quinn-proto version. The fix was picked up in version 2.2.3 (build 0.4.11) which bumped quinn-proto to 0.11.14. The latest release (2.2.4) also ships the fixed version.

## Stream 2.1.x (rhtpa-release.0.3.z) -- Out of Scope (Cross-Stream)

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|-------------|---------------------|-----------|----------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

**Stream 2.1.x summary**: All versions in this stream ship quinn-proto 0.11.9, which is vulnerable. No version in this stream has picked up the fix. This stream is outside the issue's scope (issue is scoped to 2.2.x) and triggers Case A (cross-stream impact).

## Overall Impact Summary

| Stream | Affected Versions | Fixed In | Status |
|--------|-------------------|----------|--------|
| 2.2.x (in scope) | 2.2.0, 2.2.1, 2.2.2 | 2.2.3+ (quinn-proto 0.11.14) | Already fixed in latest |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | Not fixed | Remediation needed |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions field currently contains `RHTPA 2.0.0`, which does not correspond to any configured version stream. Based on lock file evidence:

- **Remove**: RHTPA 2.0.0 (no 2.0.x stream exists; incorrect assignment)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (confirmed vulnerable via lock file analysis)
- **Do not add**: RHTPA 2.2.3, RHTPA 2.2.4 (these ship the fixed version)
- **Note**: 2.1.x versions are not added because the issue is scoped to the 2.2.x stream. Cross-stream impact is handled via Case A.
