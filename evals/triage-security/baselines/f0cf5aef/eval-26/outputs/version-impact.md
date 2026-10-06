# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

Scope: **2.2.x stream** (from issue suffix [rhtpa-2.2])

| Version | Build | Tag | criterion | Affected? | Notes |
|---------|-------|-----|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.9` | 0.5.1 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Cross-Stream Impact (Case A check)

The 2.1.x stream is also affected:

| Version | Build | Tag | criterion | Affected? | Notes |
|---------|-------|-----|-----------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES | |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES | |

All versions in the 2.1.x stream also ship criterion 0.5.1 (affected).

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Dependency scope assessment:**

- **Type**: Direct dependency (declared directly in backend/Cargo.toml)
- **Profile**: `[dev-dependencies]` -- dev-only, used for benchmarks
- **Production impact**: NONE -- criterion is NOT shipped in production builds
- **Risk classification**: Supply chain risk only (compromised dev deps can inject malicious code during builds)

Per the dependency scope decision tree:
- Add `dev-dependency` label to remediation tasks
- Override priority to **Normal** regardless of CVE severity (Medium / 5.3)
- Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | (not checked -- simulated eval) | Unknown |
