# Step 2 — Version Impact Analysis

## Version Impact Table

CVE-2026-99001 affects criterion versions < 0.5.2. Scoped to the 2.2.x stream.

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | pinned at v0.4.5 |
| 2.2.1 | 0.5.1 | YES | pinned at v0.4.8 |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | pinned at v0.4.11 |
| 2.2.4 | 0.5.1 | YES | pinned at v0.4.12 |

All 2.2.x versions ship criterion 0.5.1 which is < 0.5.2 (the fix threshold), so all versions are affected.

## Step 2.3.5 — Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Dependency scope classification**: criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. It is used for benchmarks only and is NOT shipped in production builds. The criterion crate is not included in the final binary or container image.

### Dependency Scope Decision Tree

criterion is a **dev-only** dependency (Cargo `[dev-dependencies]`):

- **Not shipped in production** — used for benchmarks only
- **Supply chain risk remains** — a compromised dev dependency can inject malicious code during builds
- **Remediation handling**:
  - Still create remediation tasks (supply chain risk)
  - Add `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include a note that the dependency is dev/build-only and not shipped in production
