# Step 2 — Version Impact Analysis: TC-8050

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Dependency Chain Context (Step 2.3.5)

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

criterion is declared in `[dev-dependencies]` and is used for benchmarks only. It is **not shipped in production builds**. Per the dependency scope decision tree:

- **Classification**: dev-only dependency (Cargo `[dev-dependencies]`)
- **Production impact**: None -- criterion is not included in the production binary or container image
- **Supply chain risk**: Yes -- compromised dev dependencies can inject malicious code during builds
- **Remediation handling**:
  - Add the `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status (Step 2.5)

The upstream branch for the 2.2.x stream is `release/0.4.z`. Since the mock data shows criterion 0.5.1 at all tags (including the latest v0.4.12), and no development stream data indicates the fix has been applied, the upstream fix status is:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |

Upstream branch does not yet ship criterion >= 0.5.2. Remediation requires an upstream dependency bump followed by downstream propagation.
