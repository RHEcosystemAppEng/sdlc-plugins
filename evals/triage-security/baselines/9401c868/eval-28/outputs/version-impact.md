# Step 2 -- Version Impact Analysis: CVE-2026-99010

## Stream Scope

Triage is scoped to the **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings (2.2.x):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Fix threshold: h2 >= 0.4.5 (from CVE-2026-99010)

Lock file evidence (simulated git show output):

- Versions 2.2.0 through 2.2.2: h2 = **0.4.4** (below fix threshold)
- Versions 2.2.3+: h2 = **0.4.5** (at fix threshold)

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
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions):**
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

**Lock file evidence (fixed versions):**
```
# Cargo.lock (versions 2.2.3+)
[[package]]
name = "h2"
version = "0.4.5"
```

**Remediation context:** h2 is a transitive dependency (3 levels deep). Remediation
requires a two-tier approach: prefer bumping the direct dependency (reqwest) to a version
whose transitive closure includes h2 >= 0.4.5; fall back to pinning h2 directly via
`cargo add h2@0.4.5` if the reqwest bump is not viable.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | **YES** | |
| 2.2.1 | 0.4.4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | at fix threshold |
| 2.2.4 | 0.4.5 | NO | at fix threshold |

**Summary:** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4
ship h2 0.4.5 which is at the fix threshold and are NOT affected.

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | **YES** |

The upstream branch `release/0.4.z` already ships h2 >= 0.4.5. Remediation is a
dependency bump (`cargo update -p h2`) plus downstream propagation to the Konflux
release repo. No upstream backport PR is needed.

## Cross-Stream Impact (Case A check)

This issue is scoped to the 2.2.x stream. Checking other configured streams:

- **2.1.x stream**: h2 version at tags v0.3.8 and v0.3.12 is 0.4.5 (per mock lock
  file data). NOT affected. No cross-stream impact.

**Result:** No cross-stream impact detected. Proceed to Case B for the 2.2.x stream only.
