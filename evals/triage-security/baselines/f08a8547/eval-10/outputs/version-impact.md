# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All four supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Summary

- **Stream rhtpa-2.1 (2.1.x)**: All versions affected (tokio 1.40.0 < 1.42.0 threshold)
- **Stream rhtpa-2.2 (2.2.x)**: All versions affected (tokio 1.41.1 < 1.42.0 threshold)

## Issue Scope vs Impact

- **Issue scope**: rhtpa-2.2 (per summary suffix `[rhtpa-2.2]`)
- **Cross-stream impact**: Stream rhtpa-2.1 is also affected but outside this issue's scope

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (Cargo)
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Ecosystem Mappings (from security-matrix.md)

### Stream rhtpa-2.1 (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream rhtpa-2.2 (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Source Pinning

- **backend**: `artifacts.lock.yaml` (download URL contains tag)
- Stream 2.1.x tags: `v0.3.8` (2.1.0), `v0.3.12` (2.1.1)
- Stream 2.2.x tags: `v0.4.5` (2.2.0), `v0.4.8` (2.2.1)
