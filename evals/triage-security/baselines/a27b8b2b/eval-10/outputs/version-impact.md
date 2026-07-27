# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

The version impact table includes ALL versions from both streams in the
supportability matrix. Since the issue is scoped to stream rhtpa-2.2,
the primary analysis targets the 2.2.x stream, but cross-stream analysis
extends to 2.1.x per Step 8 Case A.

### Full Cross-Stream Version Impact Table

| Version | Stream | Backend Tag | tokio version | Affected? | Notes |
|---------|--------|-------------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | `v0.3.8` | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | `v0.3.12` | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | `v0.4.5` | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | `v0.4.8` | 1.41.1 | YES | |
| RHTPA 2.2.2 | rhtpa-2.2 | `v0.4.9` | 1.41.1 | YES | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | rhtpa-2.2 | `v0.4.11` | 1.42.0 | NO | ships fixed version |
| RHTPA 2.2.4 | rhtpa-2.2 | `v0.4.12` | 1.42.0 | NO | ships fixed version |

### Cross-Stream Impact Summary

- **Stream rhtpa-2.2 (current issue scope):** 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions not affected (2.2.3, 2.2.4)
- **Stream rhtpa-2.1 (other stream):** ALL 2 versions affected (2.1.0, 2.1.1)

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime async executor)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | YES |
| 2.1.x | Cargo | release/0.3.z | 1.40.0 | NO |

The upstream branch `release/0.4.z` already carries tokio 1.42.0. The
upstream branch `release/0.3.z` still has tokio 1.40.0 -- an upstream
backport PR is needed first.
