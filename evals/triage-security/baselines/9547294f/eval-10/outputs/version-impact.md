# Step 2 -- Version Impact Analysis

## Version Impact Table

The version impact analysis covers ALL versions from ALL streams in the supportability matrix, since cross-stream analysis is needed to determine if other streams are also affected.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | `v0.3.8` | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | `v0.3.12` | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scope

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.2.0 | `v0.4.5` | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | `v0.4.8` | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | `v0.4.11` | 1.42.0 | NO | 1.42.0 >= 1.42.0 (fixed) |
| RHTPA 2.2.4 | `v0.4.12` | 1.42.0 | NO | 1.42.0 >= 1.42.0 (fixed) |

### Combined Version Impact Summary

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | 1.40.0 | **YES** | |
| RHTPA 2.1.1 | 2.1.x | 1.40.0 | **YES** | |
| RHTPA 2.2.0 | 2.2.x | 1.41.1 | **YES** | |
| RHTPA 2.2.1 | 2.2.x | 1.41.1 | **YES** | |
| RHTPA 2.2.2 | 2.2.x | -- | **YES** | retag of 2.2.1 |
| RHTPA 2.2.3 | 2.2.x | 1.42.0 | NO | |
| RHTPA 2.2.4 | 2.2.x | 1.42.0 | NO | |

## Cross-Stream Impact Summary

- **Stream 2.2.x (issue scope)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fix.
- **Stream 2.1.x (outside issue scope)**: ALL versions (2.1.0, 2.1.1) are affected. Stream 2.1.x ships tokio 1.40.0, which is below the fix threshold of 1.42.0.

## Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  Ecosystem: Cargo (source dependency)
  Profile: production (tokio is a runtime dependency)
  
  Stream 2.2.x: tokio 1.41.1 in versions 2.2.0-2.2.1, fixed at 1.42.0 in 2.2.3+
  Stream 2.1.x: tokio 1.40.0 in all versions (2.1.0, 2.1.1)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | tokio-rs/tokio#7001 | Upstream PR available |
| 2.1.x | Cargo | release/0.3.z | tokio-rs/tokio#7001 | Upstream PR available |
