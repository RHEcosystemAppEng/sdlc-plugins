# Step 2 - Version Impact Analysis: TC-8001

## Vulnerability Parameters

- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: >= 0.11.14

## Stream 2.2.x (scoped stream) -- rhtpa-release.0.4.z

| Version | Build | Build Date | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|------------|-------------|---------------------|-----------|----------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | 0.11.12 | **YES** | Retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

**Development stream status**: The latest build tag (`v0.4.12`) on branch `release/0.4.z` ships quinn-proto 0.11.14 (the fixed version). The fix is already present in the development stream.

**Upstream fix status (release/0.4.z)**: Already fixed. No upstream backport needed for this stream.

## Stream 2.1.x (cross-stream) -- rhtpa-release.0.3.z

| Version | Build | Build Date | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|------------|-------------|---------------------|-----------|----------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

**Development stream status**: The latest build tag (`v0.3.12`) on branch `release/0.3.z` ships quinn-proto 0.11.9 (vulnerable). The fix is NOT present in the development stream.

**Upstream fix status (release/0.3.z)**: Not fixed. Upstream backport needed.

## Summary

| Stream | Versions Affected | Latest Version Fixed? | Remediation Needed? |
|--------|-------------------|-----------------------|---------------------|
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | Yes (2.2.3+) | No -- fix already shipped |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | No | Yes -- upstream backport + downstream propagation |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. There is no 2.0.x stream.

Since the issue is scoped to 2.2.x, the corrected Affects Versions should be:
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Remove**: RHTPA 2.0.0

Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed quinn-proto 0.11.14.
