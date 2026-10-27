# Step 2 -- Version Impact Analysis

## Supportability Matrix (2.2.x stream)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` |

## Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (vulnerable) |
| 2.2.1 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (vulnerable) |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (fixed) |
| 2.2.4 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (fixed) |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

- **Dependency type**: transitive
- **Chain**: backend -> reqwest -> hyper -> h2
- **Depth**: 3 levels deep
- **Direct dependency**: reqwest (declared in backend/Cargo.toml)
- **Intermediate dependencies**: reqwest -> hyper -> h2
- h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2

### Manifest Evidence

```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

### Lock File Evidence (affected versions 2.2.0-2.2.2)

```
# Cargo.lock (versions 2.2.0 through 2.2.2)
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

### Lock File Evidence (fixed versions 2.2.3+)

```
# Cargo.lock (versions 2.2.3+)
[[package]]
name = "h2"
version = "0.4.5"
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream branch `release/0.4.z` already ships h2 0.4.5 (the fixed version), as confirmed by versions 2.2.3+ shipping h2 0.4.5. Remediation uses the dependency bump variant (not upstream backport).
