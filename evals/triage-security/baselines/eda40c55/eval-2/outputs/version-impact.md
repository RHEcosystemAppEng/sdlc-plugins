# Version Impact Analysis -- CVE-2026-28940 (Step 2)

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fix threshold**: 1.0.135
- **Ecosystem**: Cargo (Rust)

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | ships patched version (>= 1.0.135) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | ships patched version (>= 1.0.135) |

## Impact Summary

**No supported versions are affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json at version 1.0.137 or later, which is above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested input) was fixed before any currently supported version was built.

- Earliest serde_json version found: **1.0.137** (in 2.1.0, build v0.3.8, dated 2025-09-15)
- Latest serde_json version found: **1.0.139** (in 2.2.3 and 2.2.4)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold

## Dependency Chain Context (Step 2.3.5)

serde_json is a direct or near-direct dependency in the Cargo ecosystem (it is one of the most commonly used Rust crates for JSON serialization/deserialization). Since no version is affected, detailed dependency chain tracing is not required for remediation purposes. The key finding is that the patched version was already present in all supported builds.

## Upstream Fix Check (Step 2.5)

Not applicable -- no versions are affected, so upstream fix status is moot. For completeness:

| Stream | Ecosystem | Upstream Branch | Latest Shipped Version | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 | YES (already patched) |
| 2.2.x | Cargo | release/0.4.z | 1.0.139 | YES (already patched) |
