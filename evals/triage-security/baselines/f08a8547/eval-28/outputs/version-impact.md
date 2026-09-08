# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## 2.3 -- Dependency Version Extraction

Lock file evidence (simulated `git show <tag>:Cargo.lock` output):

| Version | backend tag | h2 version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.4 | **YES** | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.1 | `v0.4.8` | 0.4.4 | **YES** | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.2 | `v0.4.8` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |
| 2.2.4 | `v0.4.12` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

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

### Remediation implications

Because h2 is transitive (3 levels deep through reqwest -> hyper -> h2), remediation requires a **two-tier approach**:

1. **Preferred**: Bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5. This is the cleanest fix since it preserves the natural dependency resolution.

2. **Fallback**: If no reqwest version is available that transitively pulls in h2 >= 0.4.5, pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution. This should be documented as a temporary workaround.

## Cross-Stream Analysis

The issue is scoped to the 2.2.x stream via summary suffix `[rhtpa-2.2]`. Checking the other configured stream for cross-stream impact:

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | backend tag | h2 version | Affected? |
|---------|-------------|------------|-----------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO |

The 2.1.x stream ships h2 0.4.5 (the fix version) in all supported versions. **No cross-stream impact** -- the 2.1.x stream is not affected.

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | Upstream fix PR available: [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |

The upstream fix exists (h2 PR #800). Versions 2.2.3+ already ship the fix (h2 0.4.5), confirming the fix was picked up in later releases. Remediation for affected versions (2.2.0-2.2.2) requires backporting the dependency bump to the relevant source commits.
