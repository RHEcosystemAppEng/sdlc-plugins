# Step 2 -- Version Impact Analysis for TC-8050

## Version Impact Table

Issue is scoped to the **2.2.x** stream per suffix `[rhtpa-2.2]`.

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | tag v0.4.5 |
| 2.2.1 | 0.5.1 | YES | tag v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same source commit v0.4.8) |
| 2.2.3 | 0.5.1 | YES | tag v0.4.11 |
| 2.2.4 | 0.5.1 | YES | tag v0.4.12 |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the
affected range (< 0.5.2).

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

criterion is declared in `[dev-dependencies]` and is used for benchmarks only.
It is **NOT shipped in production builds**. Per the dependency scope decision tree:

- Dev-only dependencies still represent a supply chain risk (compromised dev deps
  can inject malicious code during builds)
- Remediation tasks will carry the `dev-dependency` label
- Priority is overridden to **Normal** regardless of CVE severity (5.3 Medium)

## Cross-Stream Impact (for Case A)

Although this issue is scoped to 2.2.x, the version impact analysis across all
streams shows that the 2.1.x stream is also affected:

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.5.1 | YES | tag v0.3.8 (stream 2.1.x) |
| 2.1.1 | 0.5.1 | YES | tag v0.3.12 (stream 2.1.x) |

Stream 2.1.x is affected and is outside this issue's scope. Case A cross-stream
impact applies.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 (at v0.4.12) | NO |

The upstream branch `release/0.4.z` does not yet ship criterion >= 0.5.2.
Remediation requires an upstream backport to bump the dependency, followed by
downstream propagation.
