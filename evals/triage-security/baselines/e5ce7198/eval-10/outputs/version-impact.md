# Step 2 -- Version Impact Analysis: TC-8020

## 2.1 -- Supportability Matrix

Loaded from configured Version Streams:

- **Stream 2.1.x**: rhtpa-release.0.3.z (Local Path: /home/dev/repos/rhtpa-release.0.3.z)
- **Stream 2.2.x**: rhtpa-release.0.4.z (Local Path: /home/dev/repos/rhtpa-release.0.4.z)

## 2.3 -- Dependency Version Extraction

Lock file inspection results for tokio (Cargo ecosystem) at pinned source commits:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Backend Tag | tokio version | Source |
|---------|-------------|---------------|--------|
| RHTPA 2.1.0 | v0.3.8 | 1.40.0 | `git show v0.3.8:Cargo.lock` |
| RHTPA 2.1.1 | v0.3.12 | 1.40.0 | `git show v0.3.12:Cargo.lock` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Backend Tag | tokio version | Source |
|---------|-------------|---------------|--------|
| RHTPA 2.2.0 | v0.4.5 | 1.41.1 | `git show v0.4.5:Cargo.lock` |
| RHTPA 2.2.1 | v0.4.8 | 1.41.1 | `git show v0.4.8:Cargo.lock` |
| RHTPA 2.2.2 | v0.4.9 | -- | retag of 2.2.1 (same as v0.4.8) |
| RHTPA 2.2.3 | v0.4.11 | (to be checked) | `git show v0.4.11:Cargo.lock` |
| RHTPA 2.2.4 | v0.4.12 | (to be checked) | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Fix threshold: tokio >= 1.42.0 (from Step 1 / Step 1.5)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | 2.1.x | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | 2.2.x | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | 2.2.x | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | 2.2.x | -- | **YES** | retag of 2.2.1 (same as v0.4.8) |
| RHTPA 2.2.3 | 2.2.x | (to be checked) | (to be checked) | |
| RHTPA 2.2.4 | 2.2.x | (to be checked) | (to be checked) | |

### Cross-stream Summary

- **Stream 2.2.x** (issue scope): RHTPA 2.2.0, 2.2.1, 2.2.2 are **affected** (tokio 1.41.1 < 1.42.0)
- **Stream 2.1.x** (out of scope): RHTPA 2.1.0, 2.1.1 are **affected** (tokio 1.40.0 < 1.42.0)

Both streams ship tokio versions below the fix threshold of 1.42.0.

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  backend (workspace) -> tokio (direct runtime dependency)
  Profile: production (tokio is the async runtime -- core dependency)

  Present in all versions across both streams.
  Stream 2.1.x: tokio 1.40.0
  Stream 2.2.x: tokio 1.41.1
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Status |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | To be verified |
| 2.2.x | Cargo | release/0.4.z | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | To be verified |

The upstream fix PR (tokio-rs/tokio#7001) addresses the use-after-free in tokio.
Remediation requires bumping tokio to >= 1.42.0 on both upstream branches, then
propagating to the respective Konflux release repos.
