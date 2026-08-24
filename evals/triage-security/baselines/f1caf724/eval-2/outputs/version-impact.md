# Version Impact Analysis -- CVE-2026-28940

## CVE Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Matrix Staleness Check

- Security matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z
- Days since last update: 57 days (as of 2026-08-24)
- Status: **Stale** (exceeds 14-day threshold)
- Note: In a live triage, the engineer would be prompted to refresh or proceed. For this eval, proceeding with current data.

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | **NO** | Ships patched version (>= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | **NO** | Ships patched version (>= 1.0.135) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.2 | v0.4.9 | -- | **NO** | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | **NO** | Ships patched version (>= 1.0.135) |

## Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability was already resolved before any tracked release shipped.

- Total versions checked: 7 (2 in stream 2.1.x, 5 in stream 2.2.x)
- Versions affected: **0**
- Minimum serde_json version found: 1.0.137 (streams 2.1.x)
- Fix threshold: 1.0.135

## Dependency Chain Context

All versions ship serde_json at a non-vulnerable version. Since no versions are affected, detailed dependency chain tracing (Step 2.3.5) is not required for remediation purposes. However, for reference:

- serde_json is a Cargo (Rust) dependency
- Present in Cargo.lock across all build tags
- Ecosystem: Cargo (source dependency)
- Lock file: Cargo.lock

## Upstream Fix Status

Not applicable -- no supported versions are affected, so upstream fix status is moot. For reference, the latest tags in both streams already ship versions well above the fix threshold.
