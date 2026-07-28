# Step 2 — Version Impact Analysis

## 2.1 — Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream rhtpa-release.0.4.z (2.2.x).

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 — Dependency Version Extraction

Extracted h2 versions from Cargo.lock at each pinned commit via `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`:

| Version | Tag | h2 version | Source |
|---------|-----|------------|--------|
| 2.2.0 | `v0.4.5` | 0.4.4 | Cargo.lock |
| 2.2.1 | `v0.4.8` | 0.4.4 | Cargo.lock |
| 2.2.2 | `v0.4.9` | -- | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 0.4.5 | Cargo.lock |
| 2.2.4 | `v0.4.12` | 0.4.5 | Cargo.lock |

## 2.4 — Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 — same as 2.2.1 |
| 2.2.3 | 0.4.5 | NO | ships fixed version |
| 2.2.4 | 0.4.5 | NO | ships fixed version |

**Affected versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
**Unaffected versions**: RHTPA 2.2.3, RHTPA 2.2.4

---

## 2.3.5 — Dependency Chain Context

### h2 dependency chain for backend

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Classification**: h2 is a **transitive** dependency. It is NOT a direct dependency of the backend workspace. It enters the dependency tree through the chain:

- `backend` depends on `reqwest` (direct dependency, declared in `[dependencies]`)
- `reqwest` depends on `hyper`
- `hyper` depends on `h2`

**Manifest evidence**:
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions 2.2.0 through 2.2.2)**:
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

**Lock file evidence (fixed versions 2.2.3+)**:
```
[[package]]
name = "h2"
version = "0.4.5"
```

**Remediation approach**: Because h2 is a transitive dependency (3 levels deep), remediation requires a two-tier strategy:

- **Preferred**: Bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: Pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution

## 2.5 — Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | -- (to be checked via `git show release/0.4.z:Cargo.lock`) | -- |

Upstream fix check requires `git show` access to the source repository. The upstream fix PR (https://github.com/hyperium/h2/pull/800) indicates the fix is available in h2 0.4.5.
