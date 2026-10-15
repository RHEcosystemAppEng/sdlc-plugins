# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded security-matrix.md covering two version streams:

- **Stream 2.1.x** (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **Stream 2.2.x** (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

Total: 7 released versions across all streams.

Since this issue is **unscoped** (no stream suffix), ALL versions from ALL streams are included in the analysis.

## 2.3 -- Dependency Version Extraction

Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Library: **h2**
Fix threshold: **0.4.8** (versions before 0.4.8 are affected)

### Extracted h2 versions at pinned commits

| Version | Stream | Pinned Commit Tag | h2 version | Affected? | Notes |
|---------|--------|-------------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Version Impact Summary

**Mixed impact across streams:**
- **2.1.x stream**: ALL versions affected (2.1.0 and 2.1.1 both ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8, at or above the fix threshold)

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock as a direct dependency of the backend workspace)
  Profile: production (h2 is a runtime HTTP/2 protocol dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock
```

The h2 crate is a direct dependency used for HTTP/2 protocol handling. It is a production dependency (not dev-only, not feature-gated).

## 2.5 -- Upstream Fix Check

Upstream fix status for affected streams:

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | Would check `git show release/0.3.z:Cargo.lock` for h2 version at branch HEAD |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). Since external tools are not invoked in this eval, the upstream fix status at the branch HEAD of `release/0.3.z` would need to be verified to determine whether the remediation is an upstream backport task or a dependency bump task.

For this analysis, the upstream backport task template is used (the conservative default when upstream fix status is not confirmed at the branch HEAD).
