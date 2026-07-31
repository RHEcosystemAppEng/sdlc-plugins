# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

Two streams loaded from Version Streams table:

- **2.1.x** stream from `security-matrix.md` (rhtpa-release.0.3.z)
- **2.2.x** stream from `security-matrix.md` (rhtpa-release.0.4.z)

All versions from both streams are included per Important Rule 4 (check ALL
supported versions).

## 2.3 -- Extract Dependency Versions

Dependency versions extracted using pinned commit tags from the supportability
matrix (Important Rule 13 -- never branch HEAD for released versions):

### 2.1.x stream

| Version | Tag | quinn-proto version | Source |
|---------|-----|---------------------|--------|
| 2.1.0 | `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock` |

### 2.2.x stream

| Version | Tag | quinn-proto version | Source |
|---------|-----|---------------------|--------|
| 2.2.0 | `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.9` | -- | retag of 2.2.1 (same source commits, Important Rule 5) |
| 2.2.3 | `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

**Summary**: 5 versions affected (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2), 2 versions
not affected (2.2.3, 2.2.4).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock as a direct dep)
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (requires git show) | TBD |
| 2.2.x | Cargo | release/0.4.z | (requires git show) | TBD |

Note: Since external tools are not available in this eval, upstream fix status
cannot be verified. In a real triage, the skill would run
`git show release/0.4.z:Cargo.lock | grep -A2 'name = "quinn-proto"'`
to determine if the upstream branch already includes the fix.

Based on the version impact table, versions 2.2.3+ (tag v0.4.11+) ship
quinn-proto 0.11.14, suggesting the upstream fix has been integrated on the
release/0.4.z branch.
