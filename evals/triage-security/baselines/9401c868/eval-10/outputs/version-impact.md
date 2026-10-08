# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Fix Threshold

- Vulnerable library: tokio
- Affected range: versions before 1.42.0
- Fixed version: **1.42.0**

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** | |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

- **Issue scope**: rhtpa-2.2 (per summary suffix `[rhtpa-2.2]`)
- **In-scope versions affected**: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
- **Out-of-scope versions affected**: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0) -- stream rhtpa-2.1

Stream rhtpa-2.1 is also affected and must be addressed via Case A (cross-stream impact with preemptive remediation).

## Ecosystem Mappings Used

### Stream 2.1.x (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Source Pinning

- Stream 2.1.x: backend pinned via `artifacts.lock.yaml` (download URL contains tag)
- Stream 2.2.x: backend pinned via `artifacts.lock.yaml` (download URL contains tag)
