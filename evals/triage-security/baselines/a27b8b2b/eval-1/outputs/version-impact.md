# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix Loaded

Matrix loaded from fixture data (security-matrix-mock.md). Both streams (2.1.x and 2.2.x) are included per Important Rule 4: "Check ALL supported versions."

## 2.3 -- Dependency Version Extraction

All dependency versions extracted using **pinned commit tags** from the supportability matrix (Important Rule 13). Released versions use the exact commit from the matrix, never HEAD or any branch tip.

### quinn-proto versions by pinned tag

| Version | Stream | Pinned Tag | quinn-proto version | Source |
|---------|--------|------------|---------------------|--------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | 2.2.x | `v0.4.8` | _(retag of 2.2.1)_ | Carried forward from 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | 0.11.12 | **YES** | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |

### Retag Handling (Important Rule 5)

Version 2.2.2 is identified as a retag of 2.2.1 (both use backend tag `v0.4.8`). The lock file check was skipped for 2.2.2 and the affected status was carried forward from 2.2.1: quinn-proto 0.11.12, **YES** (affected).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: quinn-rs/quinn#2048 |

The upstream fix PR (quinn-rs/quinn#2048) addresses the vulnerability. Versions 2.2.3+ (tag v0.4.11+) already ship the fix, confirming the upstream backport landed on the release/0.4.z branch.

## Summary

- **Affected versions (2.2.x stream)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected (2.2.x stream)**: 2.2.3, 2.2.4
- **Cross-stream impact**: 2.1.x stream (versions 2.1.0, 2.1.1) is also affected -- this will be noted in Step 8 Case A
