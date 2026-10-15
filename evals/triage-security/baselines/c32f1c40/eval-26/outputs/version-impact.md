# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability matrix (scoped to 2.2.x stream)

Loaded from security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend (tag) | Notes |
|---------|-------|------------|---------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency version extraction

Using Cargo ecosystem lock file (`Cargo.lock`) with check command `git show <tag>:Cargo.lock` at each pinned commit tag.

Extracted criterion versions from mock lock file data:

| Tag | criterion version | Comparison vs < 0.5.2 |
|-----|-------------------|-----------------------|
| `v0.4.5` | 0.5.1 | 0.5.1 < 0.5.2 -- AFFECTED |
| `v0.4.8` | 0.5.1 | 0.5.1 < 0.5.2 -- AFFECTED |
| `v0.4.9` | _(retag of v0.4.8)_ | carry forward -- AFFECTED |
| `v0.4.11` | 0.5.1 | 0.5.1 < 0.5.2 -- AFFECTED |
| `v0.4.12` | 0.5.1 | 0.5.1 < 0.5.2 -- AFFECTED |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

---

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

criterion is declared in `[dev-dependencies]` in the Cargo manifest. Per the dependency scope decision tree:

- **Classification**: dev-only -- not shipped in production
- **Rationale**: Cargo `[dev-dependencies]` are used for tests and benchmarks only; they are NOT compiled into the production binary or shipped in container images
- **Risk**: Supply chain risk remains (a compromised dev dependency can inject malicious code during builds), so remediation tasks are still created
- **Remediation handling modifications**:
  - Add the `dev-dependency` label to remediation tasks
  - Set priority to **Normal** regardless of the CVE severity (CVSS 5.3 Medium)
  - Include a note in remediation task descriptions: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

---

## 2.5 -- Upstream fix check

Upstream Branch for Cargo ecosystem in 2.2.x stream: `release/0.4.z`

Upstream fix status (not executed -- eval mode, would require `git show` on source repo):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | (not checked -- eval mode) | Unknown |

Since the upstream fix status cannot be determined in eval mode, remediation will use the standard upstream backport + downstream propagation template (not the dependency bump variant).
