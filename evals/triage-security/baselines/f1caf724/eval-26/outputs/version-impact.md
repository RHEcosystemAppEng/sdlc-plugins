# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Scoped stream: 2.2.x

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | dev-dependency only |
| 2.2.1 | 0.5.1 | YES | dev-dependency only |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | dev-dependency only |
| 2.2.4 | 0.5.1 | YES | dev-dependency only |

All versions in the 2.2.x stream ship criterion 0.5.1, which is below the fix threshold of 0.5.2.

### Cross-stream analysis: 2.1.x

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.5.1 | YES | dev-dependency only |
| 2.1.1 | 0.5.1 | YES | dev-dependency only |

The 2.1.x stream is also affected. This triggers Case A (cross-stream impact) for the scoped issue.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Dependency type**: direct dependency
**Scope**: dev-only (`[dev-dependencies]` in `backend/Cargo.toml`)
**Production impact**: NONE -- criterion is used for benchmarks only and is not included in production builds or shipped container images.

### Dependency Scope Decision

Per the dependency scope decision tree, `criterion` is a Cargo `[dev-dependencies]` entry. Dev-only dependencies are not shipped in production but still represent a supply chain risk (compromised dev deps can inject malicious code during builds). Remediation tasks are still created with the following modifications:

- Add the `dev-dependency` label to remediation tasks
- Set priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
- Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | criterion at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | (simulated -- not checked in eval) | Unknown |
