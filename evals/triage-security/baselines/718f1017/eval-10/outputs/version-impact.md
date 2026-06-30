# Step 2 -- Version Impact Analysis for CVE-2026-55123 (tokio < 1.42.0)

## 2.1 -- Supportability Matrix

Loaded from two version streams configured in Security Configuration:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

Ecosystem Mappings:
- Cargo: Repository=backend, Lock File=`Cargo.lock`, Check Command=`git show <tag>:Cargo.lock`, Upstream Branch=`release/0.3.z`

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings:
- Cargo: Repository=backend, Lock File=`Cargo.lock`, Check Command=`git show <tag>:Cargo.lock`, Upstream Branch=`release/0.4.z`

## 2.3 -- Dependency Version Extraction

Fix threshold (from Step 1.5 cross-validation): **1.42.0**

Extracted tokio versions from lock files at pinned commits:

| Version | Stream | Tag | tokio version | Affected? | Notes |
|---------|--------|-----|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | `v0.3.8` | 1.40.0 | YES | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 | `v0.3.12` | 1.40.0 | YES | 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 | `v0.4.5` | 1.41.1 | YES | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 | `v0.4.8` | 1.41.1 | YES | 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | rhtpa-2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | rhtpa-2.2 | `v0.4.11` | _(not provided)_ | _(requires lock file check)_ | |
| RHTPA 2.2.4 | rhtpa-2.2 | `v0.4.12` | _(not provided)_ | _(requires lock file check)_ | |

**Note**: The cross-stream version impact data from the issue description confirms tokio 1.40.0 for stream rhtpa-2.1 and tokio 1.41.1 for stream rhtpa-2.2 versions 2.2.0 and 2.2.1. Both are below the fix threshold of 1.42.0.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.2 | rhtpa-2.2 | -- | YES | retag of 2.2.1 |

### Cross-stream summary

- **Stream rhtpa-2.2** (issue scope): RHTPA 2.2.0, 2.2.1, 2.2.2 are all affected (tokio 1.41.1 < 1.42.0)
- **Stream rhtpa-2.1** (outside issue scope): RHTPA 2.1.0, 2.1.1 are affected (tokio 1.40.0 < 1.42.0)

This triggers **Case B** (cross-stream impact) in addition to **Case A** (remediation for current stream).

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| rhtpa-2.2 | Cargo | release/0.4.z | Upstream fix PR available: tokio-rs/tokio#7001 |
| rhtpa-2.1 | Cargo | release/0.3.z | Upstream fix PR available: tokio-rs/tokio#7001 |

The upstream fix PR (https://github.com/tokio-rs/tokio/pull/7001) provides the fix. Remediation requires bumping tokio to >= 1.42.0 on the respective upstream branches, then propagating to Konflux release repos.
