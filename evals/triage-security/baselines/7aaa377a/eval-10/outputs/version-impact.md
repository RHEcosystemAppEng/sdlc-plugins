# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

The issue is scoped to stream rhtpa-2.2, but per Important Rule 4, ALL supported versions across ALL streams are checked to enable cross-stream impact detection (Case A).

### Full Version Impact Table (all streams)

| Version | Stream | Tag | tokio version | Affected? | Notes |
|---------|--------|-----|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | `v0.3.8` | 1.40.0 | YES | Outside current issue scope |
| RHTPA 2.1.1 | rhtpa-2.1 | `v0.3.12` | 1.40.0 | YES | Outside current issue scope |
| RHTPA 2.2.0 | rhtpa-2.2 | `v0.4.5` | 1.41.1 | YES | Current stream scope |
| RHTPA 2.2.1 | rhtpa-2.2 | `v0.4.8` | 1.41.1 | YES | Current stream scope |
| RHTPA 2.2.2 | rhtpa-2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | rhtpa-2.2 | `v0.4.11` | 1.42.0 | NO | Fixed version shipped |
| RHTPA 2.2.4 | rhtpa-2.2 | `v0.4.12` | 1.42.0 | NO | Fixed version shipped |

### Cross-Stream Impact Summary

| Stream | Affected Versions | Not Affected | Impact |
|--------|-------------------|--------------|--------|
| rhtpa-2.1 | RHTPA 2.1.0, RHTPA 2.1.1 | -- | ALL versions affected |
| rhtpa-2.2 | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 | RHTPA 2.2.3, RHTPA 2.2.4 | PARTIAL -- older versions affected |

Stream **rhtpa-2.1** is also affected but is outside the current issue's scope (`[rhtpa-2.2]`). This triggers Step 8 Case A (cross-stream impact).

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | YES |
| 2.1.x | Cargo | release/0.3.z | 1.40.0 | NO |

- **Stream 2.2.x**: upstream fix is available on `release/0.4.z` -- remediation is a source ref bump in the Konflux release repo.
- **Stream 2.1.x**: upstream fix is NOT yet available on `release/0.3.z` -- remediation requires an upstream PR to bump tokio on `release/0.3.z`, then a Konflux release repo update.
