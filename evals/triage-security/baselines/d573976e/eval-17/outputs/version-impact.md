# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

The security-matrix.md file was loaded from the configured Security Matrix Path. Both streams are covered:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Using the mock lock file data, the quinn-proto version at each pinned commit tag:

### Stream 2.2.x (scoped stream)

| Version | Tag | quinn-proto version | Method |
|---------|-----|---------------------|--------|
| 2.2.0 | `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| 2.2.1 | `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| 2.2.2 | `v0.4.9` | -- | retag of v0.4.8 (same as 2.2.1: 0.11.12) |
| 2.2.3 | `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| 2.2.4 | `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |

### Stream 2.1.x (cross-stream analysis)

| Version | Tag | quinn-proto version | Method |
|---------|-----|---------------------|--------|
| 2.1.0 | `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| 2.1.1 | `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | 0.11.12 | **YES** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | ships fixed version |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)

  Present in all versions across both streams.
  Affected versions ship quinn-proto < 0.11.14 (the fix threshold).
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **Stream 2.2.x**: Fixed upstream on `release/0.4.z` -- the latest tags (v0.4.11, v0.4.12) already ship quinn-proto 0.11.14. Remediation for affected versions (2.2.0, 2.2.1, 2.2.2) requires a Konflux release repo update to pick up a newer source tag.
- **Stream 2.1.x**: Not fixed upstream on `release/0.3.z` -- the latest tag (v0.3.12) still ships quinn-proto 0.11.9. Remediation requires an upstream PR first to bump the dependency.

**Cross-stream impact summary**: Stream 2.1.x (all versions) is also affected. Since this issue is scoped to 2.2.x, the 2.1.x impact will be addressed in Step 8 Case B (cross-stream notice).
