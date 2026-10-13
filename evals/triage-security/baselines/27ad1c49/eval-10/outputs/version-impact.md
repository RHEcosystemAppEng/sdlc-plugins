# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

All supported versions across both configured streams are analyzed against
the fix threshold of tokio 1.42.0.

| Version | Stream | Build Tag | tokio version | Affected? | Notes |
|---------|--------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | v0.3.8 | 1.40.0 | **YES** | |
| RHTPA 2.1.1 | 2.1.x | v0.3.12 | 1.40.0 | **YES** | |
| RHTPA 2.2.0 | 2.2.x | v0.4.5 | 1.41.1 | **YES** | |
| RHTPA 2.2.1 | 2.2.x | v0.4.8 | 1.41.1 | **YES** | |
| RHTPA 2.2.2 | 2.2.x | v0.4.9 | -- | **YES** | retag of 2.2.1 (same source commits) |
| RHTPA 2.2.3 | 2.2.x | v0.4.11 | 1.42.0 | NO | ships fixed version |
| RHTPA 2.2.4 | 2.2.x | v0.4.12 | 1.42.0 | NO | ships fixed version |

**Fix threshold**: tokio >= 1.42.0 (from CVE description, cross-validated with external sources)

## Cross-Stream Impact Summary

- **Stream rhtpa-2.2 (issue scope)**: RHTPA 2.2.0, 2.2.1, 2.2.2 are affected. RHTPA 2.2.3 and 2.2.4 ship tokio 1.42.0 and are NOT affected.
- **Stream rhtpa-2.1 (cross-stream)**: RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0 < 1.42.0 threshold). **No sibling CVE Jira exists for rhtpa-2.1.**

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | YES |
| 2.1.x | Cargo | release/0.3.z | 1.40.0 | NO |

- **Stream 2.2.x**: the upstream branch `release/0.4.z` already ships tokio 1.42.0 (confirmed by RHTPA 2.2.3+ shipping the fix). Remediation is a dependency bump (`cargo update -p tokio`) + downstream propagation.
- **Stream 2.1.x**: the upstream branch `release/0.3.z` still ships tokio 1.40.0. Remediation requires an upstream backport to bump tokio on `release/0.3.z`, then downstream propagation.

## Affects Versions Correction (Scoped to rhtpa-2.2)

Since this issue is scoped to stream rhtpa-2.2, Affects Versions correction covers only 2.2.x versions:

- **Current (PSIRT-assigned)**: RHTPA 2.2.0, RHTPA 2.2.1
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1
- **Assessment**: PSIRT Affects Versions are already correct for the scoped stream. RHTPA 2.2.2 is a retag of 2.2.1 and is also affected but shares the same Jira version. RHTPA 2.2.3 and 2.2.4 are NOT affected (ship tokio 1.42.0).

No correction needed.
