# Step 2 -- Version Impact Analysis: CVE-2026-99010 (h2)

## Version Impact Table

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

Vulnerable library: h2
Affected range: versions before 0.4.5
Fixed version: 0.4.5

| Version | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.1 | `v0.4.8` | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.2 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.5 | NO | h2 0.4.5 = fix threshold |
| 2.2.4 | `v0.4.12` | 0.4.5 | NO | h2 0.4.5 = fix threshold |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed h2 version.

## Dependency Chain Context (Step 2.3.5)

h2 is a **transitive** dependency, not a direct dependency of the backend workspace.

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

### Manifest Evidence

```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

### Lock File Evidence (Affected Versions)

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

### Lock File Evidence (Fixed Versions)

```
# Cargo.lock (versions 2.2.3+)
[[package]]
name = "h2"
version = "0.4.5"
```

### Remediation Path (Transitive Dependency)

Because h2 is transitive (3 levels deep: reqwest -> hyper -> h2), a two-tier remediation approach is required:

1. **Preferred -- bump the direct dependency (reqwest)**: Update reqwest to a version whose transitive closure includes h2 >= 0.4.5. This requires a reqwest release that depends on a hyper version that depends on h2 >= 0.4.5.

2. **Fallback -- pin the transitive dependency directly**: If bumping reqwest is not viable (no compatible release, breaking API changes), add h2 as a direct dependency override:
   - Cargo: `cargo add h2@0.4.5` to override the transitive resolution
   - Document why the reqwest bump was not viable in the PR description

## Affects Versions Assessment

- PSIRT-assigned Affects Versions: `[RHTPA 2.2.0]`
- Actual affected versions (from lock file analysis): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
- PSIRT version is correct but **incomplete** -- 2.2.1 and 2.2.2 are also affected

Proposed correction: `[RHTPA 2.2.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
