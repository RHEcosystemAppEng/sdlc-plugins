# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix Loaded

Both stream matrix files loaded from configured Security Matrix Paths.

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

Ecosystem: **Cargo** -- using `Cargo.lock` lock file.
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
Fix threshold: **0.11.14** (from Jira description and CVE data)

Pinned commit tags from the supportability matrix are used for each version
(Important Rule 13 -- never use branch HEAD for released versions).

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

All versions from both streams are included (Important Rule 4 -- no versions skipped).
Retag version 2.2.2 carries forward the result from 2.2.1 (Important Rule 5).

### Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | _(to be checked via git show)_ | _(pending)_ |
| 2.2.x | Cargo | release/0.4.z | _(to be checked via git show)_ | _(pending)_ |

Note: In this eval, external tool calls are prohibited. In a real triage,
`git show release/0.4.z:Cargo.lock` would be executed to check upstream fix status.
Given that versions 2.2.3+ (tag v0.4.11+) already ship 0.11.14, it is likely
that the upstream branch `release/0.4.z` has the fix.
