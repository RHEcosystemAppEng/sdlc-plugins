# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for stream rhtpa-release.0.4.z (2.2.x)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Matrix staleness: Last-Updated 2026-06-28 (31 days ago -- stale, but proceeding per eval instructions).

## 2.3 -- Dependency Version Extraction

Lock file evidence from `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`:

| Version | backend tag | h2 version | Source |
|---------|-------------|------------|--------|
| 2.2.0 | `v0.4.5` | 0.4.4 | Cargo.lock |
| 2.2.1 | `v0.4.8` | 0.4.4 | Cargo.lock |
| 2.2.2 | `v0.4.9` | -- | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.5 | Cargo.lock |
| 2.2.4 | `v0.4.12` | 0.4.5 | Cargo.lock |

## 2.3.5 -- Dependency Chain Context

h2 is a **transitive** dependency, not a direct dependency of the backend workspace.

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

**Lock file evidence (affected versions 2.2.0 through 2.2.2):**

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

**Remediation approach (transitive dependency -- two-tier):**

- **Preferred**: Bump the direct dependency `reqwest` to a version whose transitive closure includes h2 >= 0.4.5. Since reqwest 0.12.5 pulls in h2 0.4.4, a newer reqwest version (or hyper version) that resolves h2 >= 0.4.5 is needed.
- **Fallback**: If no reqwest/hyper release is available that pulls in the fixed h2, pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | fixed version |
| 2.2.4 | 0.4.5 | NO | fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is the fixed version.

## Cross-Stream Analysis (for Case A check)

The 2.1.x stream is also checked to determine if cross-stream remediation is needed:

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | NO | already at fixed version |
| 2.1.1 | 0.4.5 | NO | already at fixed version |

The 2.1.x stream is NOT affected. No cross-stream impact -- Case A does not apply.

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status | Notes |
|--------|-----------|-----------------|--------|-------|
| 2.2.x | Cargo | release/0.4.z | FIXED | Versions 2.2.3+ (tags v0.4.11, v0.4.12) already ship h2 0.4.5; the upstream branch has the fix |

The upstream branch `release/0.4.z` already contains the fix. Versions built from tag v0.4.11 onward ship h2 0.4.5. The remediation downstream propagation confirms that the Konflux release repo already references fixed source tags for versions 2.2.3+. Older versions (2.2.0-2.2.2) were built from source tags that included h2 0.4.4.
