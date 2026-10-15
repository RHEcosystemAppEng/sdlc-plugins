# Step 2 — Version Impact Analysis

## 2.1 — Supportability Matrix (2.2.x stream)

Loaded from the local security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 — Dependency Version Extraction

Ecosystem: Cargo
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

Extracted h2 versions at each pinned commit:

| Version | Tag | h2 version | Method |
|---------|-----|------------|--------|
| 2.2.0 | `v0.4.5` | 0.4.4 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 0.4.4 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.8` | — | retag of 2.2.1 (carry forward) |
| 2.2.3 | `v0.4.11` | 0.4.5 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 0.4.5 | `git show v0.4.12:Cargo.lock` |

## 2.4 — Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | 0.4.4 < 0.4.5 |
| 2.2.1 | 0.4.4 | YES | 0.4.4 < 0.4.5 |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | 0.4.5 >= 0.4.5 |
| 2.2.4 | 0.4.5 | NO | 0.4.5 >= 0.4.5 |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).

## 2.3.5 — Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in all versions
```

**Classification**: h2 is a **transitive** dependency, not a direct dependency of the backend workspace. It is pulled in through the chain:

  **backend** --> **reqwest** (direct dependency) --> **hyper** --> **h2** (vulnerable)

**Manifest evidence**:
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency — it comes through reqwest → hyper → h2
```

The direct dependency in the workspace is `reqwest`. The vulnerable package `h2` is 3 levels deep in the dependency tree. This means remediation requires a **two-tier approach**:

- **Preferred**: Bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: Pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution

## 2.5 — Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | `release/0.4.z` | Versions 2.2.3+ already ship h2 0.4.5 (fixed); upstream fix is available |

The upstream branch `release/0.4.z` already includes the fix (versions 2.2.3 and 2.2.4 ship h2 0.4.5). The fix is available upstream, so remediation follows the **dependency bump** variant (not a backport).
