# Step 2 -- Version Impact Analysis: TC-8060

CVE-2026-99010 (h2 versions before 0.4.5, fixed in 0.4.5)

## Version Impact Table

| Version | Stream | Source Tag | h2 Version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | NO | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | NO | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.4 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.4 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same backend commit v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.5 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.5 | NO | |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4
which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5
which is the fixed version. The 2.1.x stream is not affected (ships h2 0.4.5 in
all versions).

## Step 2.3.5 -- Dependency Chain Context

### h2 dependency chain for backend

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

### Dependency classification

- **Type**: Transitive (3 levels deep)
- **Chain**: backend (workspace) -> reqwest -> hyper -> h2
- **Direct dependency**: reqwest (version 0.12)
- **Intermediate**: hyper (pulled in by reqwest)
- **Vulnerable package**: h2 (pulled in by hyper)
- **Profile**: Production -- reqwest is a runtime dependency, so h2 is included
  in the production binary
- **Scope**: Not dev-only, not build-only, not feature-gated -- standard
  production dependency chain

### Remediation complexity assessment

Because h2 is a transitive dependency (3 levels deep), remediation requires a
two-tier approach:

1. **Preferred**: Bump the direct dependency (reqwest) to a version whose
   transitive closure includes h2 >= 0.4.5. This is the cleanest approach
   as it respects the dependency graph.
2. **Fallback**: If bumping reqwest does not pull in h2 >= 0.4.5 (e.g.,
   reqwest pins an older hyper that pins an older h2), pin h2 directly
   via `cargo add h2@0.4.5` to override the transitive resolution.

This may require coordination with intermediate package maintainers (hyper,
reqwest) if they pin the vulnerable h2 version.

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Latest | Fixed? |
|--------|-----------|-----------------|--------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream branch `release/0.4.z` already ships h2 0.4.5 (confirmed by
versions 2.2.3 and 2.2.4 which are built from this branch). The fix is
already available upstream -- remediation uses the dependency bump variant
(not the upstream backport variant).

## Cross-Stream Impact

The issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`). The 2.1.x
stream ships h2 0.4.5 in all versions (2.1.0 and 2.1.1) and is NOT affected.
No cross-stream impact detected -- Case A does not apply.
