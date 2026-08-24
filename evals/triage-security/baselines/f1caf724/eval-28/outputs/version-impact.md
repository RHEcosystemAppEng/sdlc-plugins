# Step 2 -- Version Impact Analysis: CVE-2026-99010 (h2 < 0.4.5)

## Supportability Matrix (2.2.x stream -- scoped)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | |
| 2.2.4 | 0.4.5 | NO | |

**Summary**: Versions 2.2.0 through 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3+ ship h2 0.4.5 (the fix version) and are not affected.

## Cross-Stream Impact (2.1.x)

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | NO | |
| 2.1.1 | 0.4.5 | NO | |

The 2.1.x stream is **not affected** -- all versions ship h2 0.4.5, which is at or above the fix threshold. No cross-stream remediation needed (Case A does not apply).

## Dependency Chain Context (Step 2.3.5)

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

### Dependency Type Assessment

- h2 is a **transitive** dependency (3 levels deep: reqwest -> hyper -> h2)
- h2 is **NOT** a direct dependency in backend/Cargo.toml
- The direct dependency is **reqwest** (version 0.12)
- reqwest pulls in hyper, which pulls in h2
- This is a **production** dependency (reqwest is in `[dependencies]`, not `[dev-dependencies]`)

### Remediation Complexity

Because h2 is a transitive dependency, remediation requires a **two-tier approach**:
1. **Preferred**: Bump reqwest (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5
2. **Fallback**: If no reqwest version is available with the fix, pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Fixed in versions 2.2.3+ (h2 0.4.5) |

The upstream fix is already present on the release branch for versions 2.2.3+. The affected versions (2.2.0-2.2.2) are older releases that shipped before the fix was incorporated.
