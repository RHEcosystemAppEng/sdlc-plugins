# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z) -- scoped stream

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Extracted h2 versions from Cargo.lock at each pinned commit
(simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`):

### Stream 2.1.x

| Version | Tag | h2 version | Source |
|---------|-----|------------|--------|
| 2.1.0 | `v0.3.8` | 0.4.5 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | `v0.3.12` | 0.4.5 | `git show v0.3.12:Cargo.lock` |

### Stream 2.2.x (scoped)

| Version | Tag | h2 version | Source |
|---------|-----|------------|--------|
| 2.2.0 | `v0.4.5` | 0.4.4 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 0.4.4 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.8` | 0.4.4 | retag of 2.2.1 -- same as v0.4.8 |
| 2.2.3 | `v0.4.11` | 0.4.5 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 0.4.5 | `git show v0.4.12:Cargo.lock` |

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions 2.2.0-2.2.2):**
```
[[package]]
name = "h2"
version = "0.4.4"

[[package]]
name = "hyper"
version = "1.4.1"
dependencies = ["h2"]

[[package]]
name = "reqwest"
version = "0.12.5"
dependencies = ["hyper"]
```

**Lock file evidence (fixed versions 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

**Dependency chain summary for remediation:**
- h2 is a **transitive** dependency, pulled in through `reqwest -> hyper -> h2`
- It is NOT a direct dependency of any workspace member
- Remediation requires a two-tier approach:
  - **Preferred**: bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
  - **Fallback**: pin h2 directly via `cargo add h2@0.4.5`

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | NO | |
| 2.1.1 | 2.1.x | 0.4.5 | NO | |
| 2.2.0 | 2.2.x | 0.4.4 | **YES** | |
| 2.2.1 | 2.2.x | 0.4.4 | **YES** | |
| 2.2.2 | 2.2.x | 0.4.4 | **YES** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.5 | NO | |
| 2.2.4 | 2.2.x | 0.4.5 | NO | |

**Scoped stream (2.2.x) summary:** Versions 2.2.0, 2.2.1, and 2.2.2 are affected.
Versions 2.2.3 and 2.2.4 already ship h2 0.4.5 (the fix).

**Cross-stream summary (2.1.x):** NOT affected -- all 2.1.x versions ship h2 0.4.5.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Evidence | Fixed? |
|--------|-----------|-----------------|----------|--------|
| 2.2.x | Cargo | `release/0.4.z` | Versions 2.2.3+ (built from this branch) already ship h2 0.4.5 | **YES** |

The upstream branch `release/0.4.z` already ships the fixed h2 version (0.4.5).
Remediation path: **dependency bump** (`cargo update -p h2`) + downstream propagation.
Since h2 is a transitive dependency, the bump targets the dependency chain
(reqwest -> hyper -> h2) rather than h2 directly.
