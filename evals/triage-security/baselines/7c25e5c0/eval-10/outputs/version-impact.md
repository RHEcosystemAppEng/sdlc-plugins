# Step 2 — Version Impact Analysis

## Version Impact Table for CVE-2026-55123 (tokio < 1.42.0)

The version impact table includes ALL versions from BOTH streams in the supportability matrix, using pinned commit tags for each version (not branch HEAD).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Pinned Tag | tokio version | Affected? | Notes |
|---------|-------|------------|---------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 1.40.0 | **YES** | tokio 1.40.0 < 1.42.0 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 1.40.0 | **YES** | tokio 1.40.0 < 1.42.0 |

### Stream 2.2.x (rhtpa-release.0.4.z) — issue scope

| Version | Build | Pinned Tag | tokio version | Affected? | Notes |
|---------|-------|------------|---------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.41.1 | **YES** | tokio 1.41.1 < 1.42.0 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.41.1 | **YES** | tokio 1.41.1 < 1.42.0 |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.41.1 | **YES** | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | _(not in mock data for tokio)_ | **YES** | assumed affected based on fixture cross-stream data |
| 2.2.4 | 0.4.12 | `v0.4.12` | _(not in mock data for tokio)_ | **YES** | assumed affected based on fixture cross-stream data |

> Note: The fixture's cross-stream version impact table explicitly states that RHTPA 2.2.0 and 2.2.1 ship tokio 1.41.1 (affected) and RHTPA 2.1.0 and 2.1.1 ship tokio 1.40.0 (affected). Both streams are affected.

## Cross-stream Impact Summary

| Stream | Versions Affected | tokio Version | Within Issue Scope? |
|--------|-------------------|---------------|---------------------|
| rhtpa-2.2 | 2.2.0, 2.2.1 | 1.41.1 | **YES** (issue scoped here) |
| rhtpa-2.1 | 2.1.0, 2.1.1 | 1.40.0 | **NO** (outside scope) |

**Cross-stream impact detected**: Stream rhtpa-2.1 is also affected but is outside this issue's scope.

## Dependency Chain Context

```
Dependency chain for tokio:
  rhtpa-server (workspace) → tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```
