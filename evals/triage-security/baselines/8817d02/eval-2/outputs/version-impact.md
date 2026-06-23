# Step 2 -- Version Impact Analysis for CVE-2026-28940

## Supportability Matrix Source

Loaded from mock security-matrix.md covering two streams:
- **2.1.x** stream: rhtpa-release.0.3.z (versions 2.1.0, 2.1.1)
- **2.2.x** stream: rhtpa-release.0.4.z (versions 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

## Dependency Version Extraction

CVE-2026-28940 affects `serde_json` versions **before 1.0.135** (fixed in 1.0.135).

Extracted serde_json versions from Cargo.lock at each pinned source commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Source Tag | serde_json version | Source |
|---------|-----------|-------------------|--------|
| 2.1.0 | `v0.3.8` | 1.0.137 | Cargo.lock at v0.3.8 |
| 2.1.1 | `v0.3.12` | 1.0.137 | Cargo.lock at v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Source Tag | serde_json version | Source |
|---------|-----------|-------------------|--------|
| 2.2.0 | `v0.4.5` | 1.0.138 | Cargo.lock at v0.4.5 |
| 2.2.1 | `v0.4.8` | 1.0.138 | Cargo.lock at v0.4.8 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | Same as 2.2.1 (retag) |
| 2.2.3 | `v0.4.11` | 1.0.139 | Cargo.lock at v0.4.11 |
| 2.2.4 | `v0.4.12` | 1.0.139 | Cargo.lock at v0.4.12 |

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 (fix threshold) |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 (fix threshold) |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 (fix threshold) |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 (fix threshold) |
| 2.2.2 | 2.2.x | -- | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 (fix threshold) |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 (fix threshold) |

## Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.137, which is well above the CVE fix threshold of 1.0.135.

- The earliest serde_json version found across all streams is **1.0.137** (in versions 2.1.0 and 2.1.1).
- 1.0.137 > 1.0.135, so even the oldest supported version already includes the fix.
- The issue is scoped to stream 2.2.x, where the minimum serde_json version is **1.0.138** (versions 2.2.0 and 2.2.1). This is also above the fix threshold.

## Upstream Fix Status

Not applicable -- no versions are affected, so upstream fix status is moot. For completeness, all streams already ship patched versions of serde_json.
