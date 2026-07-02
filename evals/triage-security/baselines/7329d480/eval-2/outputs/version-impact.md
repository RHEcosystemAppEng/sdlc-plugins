# Version Impact Analysis: CVE-2026-28940

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135** (fixed in 1.0.135).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | ships patched version (>= 1.0.135) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.2 | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | ships patched version (>= 1.0.135) |

### Combined Impact Summary

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 1.0.137 | NO | |
| 2.1.1 | 1.0.137 | NO | |
| 2.2.0 | 1.0.138 | NO | |
| 2.2.1 | 1.0.138 | NO | |
| 2.2.2 | 1.0.138 | NO | retag of 2.2.1 |
| 2.2.3 | 1.0.139 | NO | |
| 2.2.4 | 1.0.139 | NO | |

**Result: NO supported versions are affected.** Every supported version across both streams ships serde_json >= 1.0.135, which is at or above the fix threshold.

## Evidence

All serde_json versions were extracted from `Cargo.lock` at each pinned build tag. The earliest version found (1.0.137 in the 2.1.x stream) is already above the fix threshold of 1.0.135. The vulnerability (versions before 1.0.135) was never present in any shipped product version.

## Upstream Fix Status

Not applicable. The vulnerability was already resolved before any supported version was built. All streams ship a patched serde_json version. No upstream backport or remediation is needed.
