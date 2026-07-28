# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from local security-matrix.md files for both configured streams.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Fix threshold: 0.11.14 (from Jira description; cross-validated via Step 1.5 external enrichment)
Comparison: versions < 0.11.14 are affected

### Extracted quinn-proto versions (using pinned commits from supportability matrix)

| Version | Tag (pinned commit) | quinn-proto version | Source |
|---------|---------------------|---------------------|--------|
| 2.1.0 | `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| 2.2.0 | `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.8` | -- | retag of 2.2.1 (skipped, carried forward) |
| 2.2.3 | `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

### Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Check | Notes |
|--------|-----------|-----------------|-------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR available (quinn-rs/quinn#2048) | Upstream fix ships quinn-proto 0.11.14 |
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR available (quinn-rs/quinn#2048) | Upstream fix ships quinn-proto 0.11.14 |

## Cross-stream summary

The issue is scoped to stream **2.2.x** via the `[rhtpa-2.2]` suffix. However, the version impact analysis shows that stream **2.1.x** is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This cross-stream impact will be addressed in Step 8 (Case A).
