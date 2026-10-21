# Step 2 -- Version Impact Analysis: TC-8050

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Scoped stream: 2.2.x

| Version | Build Tag | criterion | Affected? | Notes |
|---------|-----------|-----------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.5.1 | YES | |
| 2.2.1 | v0.4.8 | 0.5.1 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.5.1 | YES | |
| 2.2.4 | v0.4.12 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

### Cross-stream impact: 2.1.x

| Version | Build Tag | criterion | Affected? | Notes |
|---------|-----------|-----------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.5.1 | YES | cross-stream (outside issue scope) |
| 2.1.1 | v0.3.12 | 0.5.1 | YES | cross-stream (outside issue scope) |

Stream 2.1.x is also affected -- all versions ship criterion 0.5.1 (< 0.5.2). This will trigger Case A cross-stream impact handling.

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

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. Per the dependency scope decision tree:

- **Category**: Dev-only dependency (Cargo `[dev-dependencies]`)
- **Shipped in production**: NO -- dev-dependencies are used for tests and benchmarks only and are NOT included in production builds
- **Supply chain risk**: YES -- compromised dev deps can inject malicious code during builds
- **Remediation handling**:
  - Add `dev-dependency` label to all remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | criterion at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |
| 2.1.x | Cargo | release/0.3.z | 0.5.1 | NO |

The upstream fix is NOT yet available on either branch -- criterion remains at 0.5.1 on both `release/0.4.z` and `release/0.3.z`. Remediation requires an upstream backport to bump criterion to >= 0.5.2, followed by downstream propagation.
