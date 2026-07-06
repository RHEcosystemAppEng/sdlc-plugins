# Step 2 -- Version Impact Analysis: CVE-2026-99001

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range
(< 0.5.2).

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
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

criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. Dev
dependencies in Cargo are used for tests and benchmarks only and are NOT
included in production builds. The vulnerable library is not shipped in the
production container image.

Per the dependency scope decision tree:
- Dev-only dependencies still represent a supply chain risk (compromised dev
  deps can inject malicious code during builds)
- Still create remediation tasks, but with modifications:
  - Add the `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity
  - Include a note that the dependency is dev/build-only

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |

The upstream branch `release/0.4.z` still has criterion 0.5.1 (vulnerable).
Remediation requires an upstream PR to bump the dependency, followed by a
Konflux release repo update.
