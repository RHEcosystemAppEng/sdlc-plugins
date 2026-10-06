# Step 2 -- Version Impact Analysis

## Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z

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
| 2.2.3 | 0.4.5 | NO | ships fixed version |
| 2.2.4 | 0.4.5 | NO | ships fixed version |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is the fixed version.

## Cross-Stream Impact Check

Since this issue is scoped to 2.2.x, also checked the 2.1.x stream for cross-stream impact (Case A):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | NO | ships fixed version |
| 2.1.1 | 0.4.5 | NO | ships fixed version |

The 2.1.x stream is **not affected** -- all versions ship h2 >= 0.4.5. No cross-stream impact notice required.

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

### Remediation Context

- h2 is a **transitive** dependency (3 levels deep): backend -> reqwest -> hyper -> h2
- h2 is NOT a direct dependency of backend -- it cannot be bumped by editing backend/Cargo.toml alone
- The dependency chain is: reqwest (direct dep) -> hyper (transitive) -> h2 (transitive)
- **Remediation approach**: two-tier strategy required (see remediation.md)
  - Preferred: bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
  - Fallback: pin h2 directly via `cargo add h2@0.4.5`

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.2.x | Cargo | release/0.4.z | Partially fixed | 2.2.3+ ship h2 0.4.5 (fixed); 2.2.0-2.2.2 ship h2 0.4.4 (affected) |
