# Step 2 -- Version Impact Analysis

## Version Impact Table

The issue is scoped to the 2.2.x stream. Using pinned commit tags from the supportability matrix for each version.

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | tag v0.4.5 |
| 2.2.1 | 0.5.1 | YES | tag v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | tag v0.4.11 |
| 2.2.4 | 0.5.1 | YES | tag v0.4.12 |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Step 2.3.5 -- Dependency Chain Context

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

### Dependency Scope Decision Tree

criterion is declared in `[dev-dependencies]` in the Cargo.toml manifest. This means:

- **Classification**: dev-only dependency -- used for benchmarks only, NOT shipped in production builds
- **Risk assessment**: While not shipped in production, dev-only dependencies represent a supply chain risk (compromised dev deps can inject malicious code during builds)
- **Remediation handling**:
  - Still create remediation tasks (supply chain risk)
  - Add the `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include a note in remediation task description that the dependency is dev/build-only
