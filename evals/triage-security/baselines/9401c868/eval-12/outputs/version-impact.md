# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8** (all versions below 0.4.8 are vulnerable; 0.4.8+ is fixed)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | ships fixed version (0.4.8 >= 0.4.8) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | ships fixed version (0.4.8 >= 0.4.8) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Combined Impact Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 (all) | -- |
| 2.2.x (scoped) | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all) |

## Scoped Stream Assessment

The issue is scoped to stream **2.2.x** via the `[rhtpa-2.2]` suffix.

**Within the scoped stream (2.2.x)**: No versions are affected. All versions in the 2.2.x stream ship h2 >= 0.4.8 (the fixed version). The earliest version in this stream (2.2.0, built from tag v0.4.5) already includes h2 0.4.8.

**Outside the scoped stream (2.1.x)**: All versions are affected. Both versions in the 2.1.x stream (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 is a direct Cargo dependency)
  Ecosystem: Cargo (crates.io)
  Profile: production (h2 is a runtime dependency for HTTP/2 support)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.1.x | Cargo | release/0.3.z | YES | h2 0.4.8 is a published crate on crates.io; fix is available via dependency update |
| 2.2.x | Cargo | release/0.4.z | N/A | Stream not affected |

The upstream fix (h2 0.4.8) is already published on crates.io. For affected streams, remediation is a dependency bump (`cargo update -p h2`), not an upstream backport.
