# Step 2 -- Version Impact Analysis

## Scope

Triage scoped to the **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion versions before 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | pinned commit v0.4.5 |
| 2.2.1 | 0.5.1 | YES | pinned commit v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | pinned commit v0.4.11 |
| 2.2.4 | 0.5.1 | YES | pinned commit v0.4.12 |

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (versions before 0.5.2).

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

- **Dependency type**: direct
- **Profile**: `[dev-dependencies]` -- dev-only
- **Shipped in production?**: NO -- used for benchmarks only, not present in production builds
- **Decision**: Dev-only dependency. Still create remediation tasks (supply chain risk), but:
  - Add `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include note in task description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Not determined from available data |

The upstream fix status for criterion on `release/0.4.z` was not available in the mock data. Since criterion 0.5.1 is the version present at all pinned commits and the fix requires 0.5.2, a dependency bump is needed.
