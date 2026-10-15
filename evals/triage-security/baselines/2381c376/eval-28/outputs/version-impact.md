# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream, scoped)

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

Lock file evidence (from mock fixture data):

- **Versions 2.2.0 through 2.2.2** (`v0.4.5`, `v0.4.8` tags): h2 **0.4.4**
- **Versions 2.2.3+** (`v0.4.11`, `v0.4.12` tags): h2 **0.4.5**

Fix threshold: h2 >= 0.4.5 (from Jira description, confirmed by CVE record)

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

**Key observations:**

- h2 is a **transitive dependency** at 3 levels deep in the dependency tree
- The direct dependency is **reqwest** (version 0.12), which depends on **hyper** (1.4.1), which depends on **h2**
- h2 is included in **production** profile (reqwest is a runtime dependency, not dev-only)
- Since h2 is transitive, remediation requires a **two-tier approach**: prefer bumping the direct dependency (reqwest) to a version whose transitive closure includes h2 >= 0.4.5; fall back to pinning h2 directly if reqwest bump is not viable

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.4 | **YES** | |
| 2.2.1 | 0.4.4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | |
| 2.2.4 | 0.4.5 | NO | |

**Affected versions (2.2.x stream):** 2.2.0, 2.2.1, 2.2.2
**Not affected versions (2.2.x stream):** 2.2.3, 2.2.4

### Cross-stream check (2.1.x)

For the Case A cross-stream impact assessment, the 2.1.x stream was also checked:

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.4.5 | NO | |
| 2.1.1 | 0.4.5 | NO | |

The 2.1.x stream is **not affected** -- all versions ship h2 0.4.5 which meets the fix threshold. No cross-stream impact to report (Case A does not apply).

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status | Evidence |
|--------|-----------|-----------------|--------|----------|
| 2.2.x | Cargo | `release/0.4.z` | **FIXED** | Versions 2.2.3+ (tags v0.4.11, v0.4.12) ship h2 0.4.5 |

The upstream fix is already available on the `release/0.4.z` branch. The vulnerability was fixed in the source repository and shipped in versions 2.2.3+. Remediation for affected versions (2.2.0--2.2.2) uses the **dependency bump** variant (not upstream backport), since the upstream branch already ships the fix.

Upstream fix PR: [hyperium/h2#800](https://github.com/hyperium/h2/pull/800)
