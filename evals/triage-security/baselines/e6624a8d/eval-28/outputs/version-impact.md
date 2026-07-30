# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from the 2.2.x stream's security-matrix.md (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Lock file evidence from `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`:

| Version | Backend Tag | h2 version | Source |
|---------|-------------|------------|--------|
| 2.2.0 | v0.4.5 | 0.4.4 | Cargo.lock |
| 2.2.1 | v0.4.8 | 0.4.4 | Cargo.lock |
| 2.2.2 | v0.4.8 | -- | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.5 | Cargo.lock |
| 2.2.4 | v0.4.12 | 0.4.5 | Cargo.lock |

## 2.3.5 -- Dependency Chain Context

h2 is a **transitive dependency** (3 levels deep). It is NOT a direct
dependency of the backend workspace -- it enters the dependency tree through
the reqwest HTTP client library.

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

**Remediation approach (transitive dependency -- two-tier):**
1. **Preferred**: bump `reqwest` (the direct dependency) to a version whose
   transitive closure includes h2 >= 0.4.5. Check whether reqwest 0.12.x
   has a release that pulls in hyper with h2 >= 0.4.5.
2. **Fallback**: if bumping reqwest does not resolve the transitive h2 version
   (e.g., reqwest still pulls in h2 < 0.4.5 through hyper), pin h2 directly
   via `cargo add h2@0.4.5` to override the transitive resolution.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | h2 < 0.4.5 |
| 2.2.1 | 0.4.4 | YES | h2 < 0.4.5 |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | h2 >= 0.4.5 (fixed) |
| 2.2.4 | 0.4.5 | NO | h2 >= 0.4.5 (fixed) |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4, which is within
the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which
is the fixed version and therefore NOT affected.

## Cross-Stream Check (2.1.x)

Since this issue is scoped to `[rhtpa-2.2]`, the 2.1.x stream is checked for
cross-stream impact (Case A):

| Version | Backend Tag | h2 version | Affected? |
|---------|-------------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO |
| 2.1.1 | v0.3.12 | 0.4.5 | NO |

The 2.1.x stream is **NOT affected** -- all versions already ship h2 0.4.5
(the fixed version). No cross-stream remediation is needed.

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.2.x | Cargo | release/0.4.z | Fixed in versions 2.2.3+ (h2 bumped to 0.4.5) |

The upstream fix (hyperium/h2#800) has already been incorporated into the
dependency tree for versions 2.2.3+. Remediation for affected versions
(2.2.0-2.2.2) requires backporting the h2 bump to the release/0.4.z branch
at a commit that predates the fix.
