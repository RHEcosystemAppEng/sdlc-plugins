# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Scoped stream: 2.2.x

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2).

### Cross-stream impact (2.1.x)

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.5.1 | YES | |
| 2.1.1 | 0.5.1 | YES | |

The 2.1.x stream is also affected -- all versions ship criterion 0.5.1.

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

criterion is declared in `[dev-dependencies]` and is **not shipped in production builds**. It is used for benchmarks only.

Per the dependency scope decision tree:
- Dev-only dependencies still represent a supply chain risk (compromised dev deps can inject malicious code during builds)
- Remediation tasks will be created, but with:
  - `dev-dependency` label added
  - Priority overridden to **Normal** regardless of CVE severity
  - Description note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |

The upstream branch `release/0.4.z` still ships criterion 0.5.1. An upstream backport is required before downstream propagation.
