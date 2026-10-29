# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z (2.2.x stream)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

Ecosystem mappings for 2.2.x:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## 2.3 -- Dependency Version Extraction

Fix threshold: h2 >= 0.4.5 (from CVE description; to be cross-validated with MITRE/OSV in Step 1.5)

Lock file evidence (from `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`):

| Version | Backend Tag | h2 version in Cargo.lock | Source |
|---------|-------------|--------------------------|--------|
| 2.2.0 | v0.4.5 | 0.4.4 | Lock file at pinned commit |
| 2.2.1 | v0.4.8 | 0.4.4 | Lock file at pinned commit |
| 2.2.2 | v0.4.9 | -- | Retag of 2.2.1 (skipped, carry forward) |
| 2.2.3 | v0.4.11 | 0.4.5 | Lock file at pinned commit |
| 2.2.4 | v0.4.12 | 0.4.5 | Lock file at pinned commit |

Lock file evidence detail (affected versions -- 2.2.0 through 2.2.2):
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

Lock file evidence detail (fixed versions -- 2.2.3+):
```
[[package]]
name = "h2"
version = "0.4.5"
```

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

Manifest evidence:
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

### Remediation complexity assessment

- h2 is a **transitive** dependency, 3 levels deep
- The direct dependency is **reqwest** (version 0.12)
- reqwest depends on **hyper**, which depends on **h2**
- Remediation requires either:
  1. (Preferred) Bumping reqwest to a version whose transitive closure includes h2 >= 0.4.5
  2. (Fallback) Pinning h2 directly via `cargo add h2@0.4.5` to override the transitive resolution

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | fixed at exactly the fix threshold |
| 2.2.4 | 0.4.5 | NO | |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). The fix (h2 0.4.5) was picked up starting with version 2.2.3.

### Cross-stream check (for Case A evaluation)

The 2.1.x stream was checked for cross-stream impact:

| Version | Backend Tag | h2 version | Affected? |
|---------|-------------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO |
| 2.1.1 | v0.3.12 | 0.4.5 | NO |

The 2.1.x stream is NOT affected. No cross-stream remediation is needed (Case A does not apply).

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream branch `release/0.4.z` already ships h2 0.4.5. This confirms the fix is available upstream, so the **dependency bump** variant applies (rather than the upstream backport variant).
