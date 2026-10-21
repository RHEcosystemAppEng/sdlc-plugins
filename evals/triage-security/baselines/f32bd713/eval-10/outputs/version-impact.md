# Step 2 -- Version Impact Analysis: TC-8020

## CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: **1.42.0** (from Jira description, advisory, and CVE record)

## Version Impact Table

All supported versions across both configured streams are analyzed. The issue is scoped to stream rhtpa-2.2 (`[rhtpa-2.2]`), but cross-stream analysis covers all streams for Case A evaluation.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | v0.3.8 | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | v0.3.12 | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |

- Upstream Branch: `release/0.3.z`
- Repository: backend (rhtpa-backend)
- Lock File: `Cargo.lock`

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.2.0 | v0.4.5 | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | v0.4.8 | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | v0.4.9 | -- | **YES** | retag of 2.2.1 (same backend commit v0.4.8) |

- Upstream Branch: `release/0.4.z`
- Repository: backend (rhtpa-backend)
- Lock File: `Cargo.lock`

## Combined Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | 1.40.0 | **YES** | |
| RHTPA 2.1.1 | 2.1.x | 1.40.0 | **YES** | |
| RHTPA 2.2.0 | 2.2.x | 1.41.1 | **YES** | |
| RHTPA 2.2.1 | 2.2.x | 1.41.1 | **YES** | |
| RHTPA 2.2.2 | 2.2.x | -- | **YES** | retag of 2.2.1 |

## Cross-Stream Impact Summary

- **Issue stream scope**: 2.2.x (rhtpa-2.2)
- **Other affected streams**: 2.1.x (rhtpa-2.1)
- **Stream 2.1.x tokio version**: 1.40.0 (below fix threshold 1.42.0)
- **Sibling CVE Jiras for rhtpa-2.1**: **None found** (JQL search for label CVE-2026-55123 with stream suffix [rhtpa-2.1] returned no results)
- **Conclusion**: Stream 2.1.x is affected and has no CVE Jira -- preemptive remediation tasks required (Case A)

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (Cargo)
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml / Cargo.lock
```
