# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from local security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

Extracted h2 versions from Cargo.lock at each pinned commit:

| Version | Tag | h2 version | Method |
|---------|-----|------------|--------|
| 2.2.0 | `v0.4.5` | 0.4.4 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 0.4.4 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.8` | -- | retag of 2.2.1 (same backend commit) |
| 2.2.3 | `v0.4.11` | 0.4.5 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 0.4.5 | `git show v0.4.12:Cargo.lock` |

Fix threshold: h2 >= 0.4.5 (from Jira description: fixed in 0.4.5).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 |
| 2.2.1 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 |
| 2.2.4 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

## Cross-stream check (for Case A evaluation)

Stream 2.1.x h2 versions (from security-matrix.md mock lock file data):

| Version | Tag | h2 version | Affected? |
|---------|-----|------------|-----------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO |

Stream 2.1.x is NOT affected -- all versions ship h2 >= 0.4.5. No cross-stream impact notice required.

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
- `backend/Cargo.toml` declares `reqwest = { version = "0.12", features = ["json"] }` as a direct `[dependencies]` entry
- `h2` is NOT a direct dependency -- it enters the dependency tree transitively through reqwest -> hyper -> h2
- reqwest is a production (runtime) dependency, so h2 is included in production builds

**Dependency classification**: transitive (3 levels deep)
- Level 1: backend -> reqwest (direct dependency)
- Level 2: reqwest -> hyper (transitive)
- Level 3: hyper -> h2 (transitive -- vulnerable package)

**Remediation approach**:
- **Preferred**: bump reqwest (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5. Check if a newer reqwest release pulls in hyper with h2 >= 0.4.5.
- **Fallback**: pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution. Document why the direct dep bump was not viable.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.2.x | Cargo | release/0.4.z | (check pending) | (check pending) |

The upstream fix PR is https://github.com/hyperium/h2/pull/800. The upstream branch `release/0.4.z` in the backend repository would need to be inspected at HEAD to determine if the fix has been merged.
