# Step 2 -- Version Impact Analysis for CVE-2026-31812

## 2.1 -- Supportability Matrix

Loaded from two configured Version Streams:

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

Using the mock lock file data (simulating `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

### Extracted quinn-proto versions

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| `v0.4.9` | _(retag of v0.4.8)_ | Skipped -- same as 2.2.1 |
| `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock` |

### Fix threshold comparison

- **Affected range**: versions before 0.11.14 (< 0.11.14)
- **Fixed version**: 0.11.14
- Versions < 0.11.14 are AFFECTED; versions >= 0.11.14 are NOT affected

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source dependency)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)

First appeared: 2.1.0 (v0.3.8)
Present in all versions checked.
```

quinn-proto is a transitive dependency brought in through the quinn crate. It is a production dependency (not dev-only), so the vulnerability applies to shipped builds.

## 2.5 -- Upstream Fix Check

Upstream fix status (checking branch HEAD of source repos):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs inspection) | TBD |
| 2.2.x | Cargo | release/0.4.z | (needs inspection) | TBD |

Based on the version impact table, versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14), suggesting the upstream fix has been applied to the `release/0.4.z` branch.

## Cross-Stream Impact Summary

This issue is **scoped to stream 2.2.x** (per the `[rhtpa-2.2]` suffix).

- **Stream 2.2.x (in scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (already fixed).
- **Stream 2.1.x (out of scope)**: Versions 2.1.0 and 2.1.1 are also affected. These are tracked separately -- either by a companion CVE Jira for stream 2.1.x or via proactive remediation tasks (Step 7 Case B).
