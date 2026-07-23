# Step 2 -- Version Impact Analysis

## Supportability Matrix

Loaded from two streams configured in Security Configuration Version Streams table:

- **2.1.x** stream: `security-matrix.md` at rhtpa-release.0.3.z
- **2.2.x** stream: `security-matrix.md` at rhtpa-release.0.4.z

Issue is scoped to **2.2.x** stream (from suffix `[rhtpa-2.2]`). Both streams are analyzed for cross-stream impact.

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | Stream | Tag | criterion | Affected? | Notes |
|---------|--------|-----|-----------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.5.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.5.1 | YES | 0.5.1 < 0.5.2 |

## Dependency Chain Context

Dependency chain for criterion (Cargo ecosystem):

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

Manifest evidence:
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

**Dev-dependency impact assessment**: criterion is declared in `[dev-dependencies]` and is NOT present in production builds. It is used only for benchmarks. While it does not affect the shipped product, it still represents a supply chain risk (compromised dev deps can inject malicious code during builds). Per the dependency scope decision tree:

- Add the `dev-dependency` label to remediation tasks
- Override priority to **Normal** regardless of CVE severity (5.3 Medium)
- Include a note in task descriptions: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | `release/0.4.z` | All versions ship criterion 0.5.1 (affected); upstream branch needs fix |
| 2.1.x | Cargo | `release/0.3.z` | All versions ship criterion 0.5.1 (affected); upstream branch needs fix |

## Cross-Stream Impact

This issue is scoped to stream **2.2.x** (from suffix `[rhtpa-2.2]`), but the version impact analysis shows that stream **2.1.x** is also affected:

- 2.1.0 ships criterion 0.5.1 (affected)
- 2.1.1 ships criterion 0.5.1 (affected)

This cross-stream impact would trigger Case B in Step 8, posting a cross-stream impact comment and checking for sibling CVE Jiras for the 2.1.x stream.
