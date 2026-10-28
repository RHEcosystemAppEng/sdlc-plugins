# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | 1.41.1 | YES | |

All shipped versions across both streams include tokio < 1.42.0 and are therefore vulnerable.

## Cross-Stream Impact Summary

- **Issue stream scope**: rhtpa-2.2 (2.2.x)
- **Scoped versions affected**: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
- **Other streams affected**: rhtpa-2.1 (2.1.x) -- RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
- **Fix threshold**: tokio >= 1.42.0

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (assumed based on tokio being a core async runtime)
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Ecosystem Mappings Used

### Stream 2.1.x (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Affects Versions Correction (Step 3)

- **PSIRT-assigned**: RHTPA 2.2.0, RHTPA 2.2.1
- **Version impact (scoped to rhtpa-2.2)**: RHTPA 2.2.0 (YES), RHTPA 2.2.1 (YES)
- **Assessment**: PSIRT Affects Versions are correct for the scoped stream. No correction needed.
