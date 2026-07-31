# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix-mock.md, Stream 2 (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

criterion versions extracted from mock lock file data (Cargo.lock):

| Tag | criterion version |
|-----|-------------------|
| `v0.4.5` | 0.5.1 |
| `v0.4.8` | 0.5.1 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.5.1 |
| `v0.4.12` | 0.5.1 |

Fix threshold: 0.5.2 (from Jira description -- all versions ship 0.5.1 which is below 0.5.2)

## 2.3.5 -- Dependency Chain Context

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

### Dependency Scope Decision Tree

criterion is declared in `[dev-dependencies]` in backend/Cargo.toml. Per the dependency
scope decision tree in version-impact-analysis.md:

- **Classification**: dev-only -- not shipped in production
- **Rationale**: Cargo `[dev-dependencies]` are used for tests and benchmarks only; NOT shipped
  in production binaries or container images
- **Remediation handling modifications**:
  - Add the `dev-dependency` label to the remediation task
  - Set priority to **Normal** regardless of the CVE severity (CVSS 5.3 Medium)
  - Include a note in the remediation task description: "This dependency is dev/build-only
    and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

Even though dev-only dependencies are not shipped, they still represent a supply chain risk
(compromised dev deps can inject malicious code during builds). Remediation tasks are still
created, but with the modifications above.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range
(versions before 0.5.2). All versions are affected.

**Dependency scope**: criterion is a dev-only dependency ([dev-dependencies]) and is NOT
shipped in production builds. Remediation tasks will carry the `dev-dependency` label and
Normal priority per the dependency scope decision tree.
