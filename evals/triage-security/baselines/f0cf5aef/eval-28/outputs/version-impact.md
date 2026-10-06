# Step 2 -- Version Impact Analysis: CVE-2026-99010

## Version Impact Table

Issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

### Stream 2.2.x (scoped)

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | Build | backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.4 | YES | h2 0.4.4 < 0.4.5 fix threshold |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.4 | YES | h2 0.4.4 < 0.4.5 fix threshold |
| 2.2.2 | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 fix threshold |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 fix threshold |

**Affected versions in scope**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### Cross-stream check: 2.1.x

Since this is a scoped issue, checking other streams for Case A (cross-stream impact):

| Version | Build | backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 fix threshold |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 fix threshold |

**Cross-stream impact**: None. The 2.1.x stream is not affected -- all versions ship h2 >= 0.4.5.

## Step 2.3.5 -- Dependency Chain Context

h2 is a **transitive** dependency in the backend workspace. It is not declared
directly in `backend/Cargo.toml` -- it enters the dependency tree through
intermediate packages.

### Dependency chain

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

### Manifest evidence

```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

### Lock file evidence (affected versions: 2.2.0 through 2.2.2)

```
# Cargo.lock
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

### Lock file evidence (fixed versions: 2.2.3+)

```
# Cargo.lock
[[package]]
name = "h2"
version = "0.4.5"
```

### Remediation implications

Because h2 is transitive (3 levels deep), remediation requires a **two-tier approach**:

1. **Preferred**: Bump `reqwest` (the direct dependency) to a version whose transitive
   closure includes h2 >= 0.4.5. This resolves the vulnerability without adding h2
   as a direct dependency.
2. **Fallback**: If no reqwest version is available with the fix, pin h2 directly via
   `cargo add h2@0.4.5` to override the transitive resolution. Document why the
   direct dep bump was not viable in the PR description.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.2.x | Cargo | `release/0.4.z` | Partially fixed | h2 0.4.5 in 2.2.3+ but 2.2.0-2.2.2 still ship 0.4.4 |

Upstream fix PR: https://github.com/hyperium/h2/pull/800
