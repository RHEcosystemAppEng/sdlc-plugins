# Version Impact Analysis -- Step 2

## Configuration

| Setting | Value |
|---------|-------|
| Project key | TC |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| VEX Justification custom field | customfield_12345 |
| Component label pattern | pscomponent: |

### Version Streams

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.1.x | rhtpa-release.0.3.z |
| 2.2.x | rhtpa-release.0.4.z |

## Supportability Matrix (Aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend Tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend Tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Version Impact Table

CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.1 | 2.1.x | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.2.0 | 2.2.x | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.1 | 2.2.x | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.4 | 2.2.x | 1.0.139 | NO | ships patched version (>= 1.0.135) |

## Summary

**All supported versions ship serde_json >= 1.0.135**, which is at or above the fix threshold. No supported version is affected by CVE-2026-28940.

- Stream 2.1.x: all versions ship serde_json 1.0.137 -- NOT affected
- Stream 2.2.x: all versions ship serde_json 1.0.138 or 1.0.139 -- NOT affected

The lowest serde_json version across all supported releases is **1.0.137** (in the 2.1.x stream), which is above the fix threshold of 1.0.135.

## Dependency Chain Context (Step 2.3.5)

Since no supported version is affected, detailed dependency chain tracing is not required. For reference:

- **Library**: serde_json
- **Ecosystem**: Cargo (Rust)
- **Type**: Likely a direct dependency (serde_json is a fundamental serialization crate in the Rust ecosystem)

## Upstream Fix Status (Step 2.5)

Not applicable -- no versions are affected, so no upstream fix check is needed. For completeness, all shipped versions already include the fix (serde_json >= 1.0.135).
