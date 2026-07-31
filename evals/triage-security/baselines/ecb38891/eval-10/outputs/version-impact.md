# Step 2 — Version Impact Analysis

## 2.1 — Supportability Matrix

Loaded from local security-matrix.md files for both configured Version Streams:

- **Stream 2.1.x** (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **Stream 2.2.x** (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

Matrix Last-Updated timestamp: 2026-06-28T10:00:00Z (within 14-day threshold, Step 0.3 passed silently).

## 2.3 — Dependency Version Extraction

Ecosystem: **Cargo** (lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock`)

Extracted tokio versions from Cargo.lock at each pinned commit:

### Stream 2.1.x (cross-stream analysis)

| Version | Tag | tokio version | Source |
|---------|-----|---------------|--------|
| 2.1.0 | `v0.3.8` | 1.40.0 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | `v0.3.12` | 1.40.0 | `git show v0.3.12:Cargo.lock` |

### Stream 2.2.x (scoped stream)

| Version | Tag | tokio version | Source |
|---------|-----|---------------|--------|
| 2.2.0 | `v0.4.5` | 1.41.1 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 1.41.1 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.9` | 1.41.1 | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 1.42.0 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 1.42.0 | `git show v0.4.12:Cargo.lock` |

## 2.4 — Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| 2.1.0 | 2.1.x | 1.40.0 | YES | |
| 2.1.1 | 2.1.x | 1.40.0 | YES | |
| 2.2.0 | 2.2.x | 1.41.1 | YES | |
| 2.2.1 | 2.2.x | 1.41.1 | YES | |
| 2.2.2 | 2.2.x | 1.41.1 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.42.0 | NO | |
| 2.2.4 | 2.2.x | 1.42.0 | NO | |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Cross-Stream Impact Summary

The issue is scoped to stream **rhtpa-2.2**, but the version impact analysis reveals that stream **rhtpa-2.1** is also affected:

| Stream | Affected Versions | tokio version | Affected? |
|--------|-------------------|---------------|-----------|
| rhtpa-2.1 | 2.1.0, 2.1.1 | 1.40.0 | YES |
| rhtpa-2.2 | 2.2.0, 2.2.1, 2.2.2 | 1.41.1 | YES |
| rhtpa-2.2 | 2.2.3, 2.2.4 | 1.42.0 | NO |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0. This triggers Case A (cross-stream impact) in Step 8.

## 2.5 — Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | (would check via git show) | TBD |
| 2.1.x | Cargo | release/0.3.z | (would check via git show) | TBD |
