# Step 2 -- Version Impact Analysis: CVE-2026-99001

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Scoped stream: 2.2.x

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0   | 0.5.1     | YES       |       |
| 2.2.1   | 0.5.1     | YES       |       |
| 2.2.2   | --        | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 0.5.1     | YES       |       |
| 2.2.4   | 0.5.1     | YES       |       |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the
affected range (< 0.5.2).

### Cross-stream analysis (for Case B evaluation)

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0   | 0.5.1     | YES       |       |
| 2.1.1   | 0.5.1     | YES       |       |

The 2.1.x stream is also affected (criterion 0.5.1 across all versions).

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

### Dependency scope assessment

- **Scope**: `[dev-dependencies]` -- dev-only
- **Shipped in production?**: NO -- criterion is used for benchmarks only and is
  excluded from production builds
- **Risk type**: Supply chain risk only -- a compromised dev dependency could
  inject malicious code during builds, but the vulnerability itself (path
  traversal in benchmark output) does not affect production artifacts
- **Remediation handling per decision tree**:
  - Still create remediation tasks (supply chain risk)
  - Add the `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (Medium/5.3)
  - Include note in task description: "This dependency is dev/build-only and is
    not shipped in production. Remediation priority is Normal (supply chain risk
    only)."

### Manifest evidence

```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.5.1           | NO     |

Upstream branch `release/0.4.z` still has criterion 0.5.1 -- the fix (bump
to >= 0.5.2) has not been applied upstream yet. Remediation requires an
upstream PR first, then a downstream Konflux release repo update.
