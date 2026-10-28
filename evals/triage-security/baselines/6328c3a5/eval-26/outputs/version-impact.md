# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

Scope: 2.2.x stream only (issue scoped by `[rhtpa-2.2]` suffix).

| Version | Build | Tag | criterion version | Affected? | Notes |
|---------|-------|-----|-------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` and is used for benchmarks only. It is NOT included in production builds or shipped in container images. Per the dependency scope decision tree:

- **Label**: `dev-dependency` added to remediation tasks
- **Priority override**: Normal (regardless of CVE severity)
- **Risk classification**: supply chain risk only -- not a runtime vulnerability

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |

The upstream branch `release/0.4.z` still ships criterion 0.5.1 (based on the latest released tag `v0.4.12`). The fix (0.5.2) is not yet available on the upstream branch.

**Remediation path**: Upstream backport required -- bump criterion to >= 0.5.2 on `release/0.4.z`, then propagate to the Konflux release repo.

## Cross-stream Impact (informational)

The 2.1.x stream also ships criterion 0.5.1 (tags `v0.3.8` and `v0.3.12`), but is outside this issue's scope (`[rhtpa-2.2]`). Cross-stream impact would be noted per Case A (Step 8), but remediation tasks are only created for the scoped 2.2.x stream.
