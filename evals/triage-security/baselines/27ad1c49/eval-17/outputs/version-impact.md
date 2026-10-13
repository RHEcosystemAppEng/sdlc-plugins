# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Supportability Matrix Source

Matrix data loaded from two streams configured in Version Streams:

- **2.1.x** stream: rhtpa-release.0.3.z (Last-Updated: 2026-06-28T10:00:00Z -- 107 days ago, exceeds 14-day staleness threshold)
- **2.2.x** stream: rhtpa-release.0.4.z (Last-Updated: 2026-06-28T10:00:00Z -- 107 days ago, exceeds 14-day staleness threshold)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same source as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Stream-Scoped Impact Summary

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

**Within-scope (2.2.x) affected versions**: 2.2.0, 2.2.1, 2.2.2
**Within-scope (2.2.x) not affected versions**: 2.2.3, 2.2.4

**Cross-stream (2.1.x) affected versions**: 2.1.0, 2.1.1
The 2.1.x stream is outside this issue's scope but is also affected. This triggers Case A (cross-stream impact) in Step 8.

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock across all versions)
  Ecosystem: Cargo
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
```

quinn-proto is a direct dependency of the backend workspace. Remediation is a straightforward dependency version bump.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | 0.11.14 | YES |
| 2.1.x | Cargo | `release/0.3.z` | 0.11.9 | NO |

- **Stream 2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (confirmed by v0.4.11 and v0.4.12 tags). Remediation is a dependency bump (`cargo update`) plus downstream propagation.
- **Stream 2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation for this stream requires an upstream backport before downstream propagation.
