# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | pinned at v0.3.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | pinned at v0.3.12 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships fixed version |

## Lock File Evidence

Dependency versions extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
at pinned backend commits from security-matrix.md:

| Tag | h2 version | Comparison to fix threshold (0.4.8) |
|-----|------------|-------------------------------------|
| `v0.3.8` (2.1.0) | 0.4.5 | 0.4.5 < 0.4.8 -- VULNERABLE |
| `v0.3.12` (2.1.1) | 0.4.5 | 0.4.5 < 0.4.8 -- VULNERABLE |
| `v0.4.5` (2.2.0) | 0.4.8 | 0.4.8 >= 0.4.8 -- NOT VULNERABLE |
| `v0.4.8` (2.2.1) | 0.4.8 | 0.4.8 >= 0.4.8 -- NOT VULNERABLE |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ | same as 2.2.1 -- NOT VULNERABLE |
| `v0.4.11` (2.2.3) | 0.4.9 | 0.4.9 >= 0.4.8 -- NOT VULNERABLE |
| `v0.4.12` (2.2.4) | 0.4.9 | 0.4.9 >= 0.4.8 -- NOT VULNERABLE |

## Stream-Level Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable) |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (fixed version or later) |

This is a **mixed impact** scenario: the 2.1.x stream ships the vulnerable
dependency while the 2.2.x stream already ships the patched version.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency)
  Ecosystem: Cargo (Cargo.lock)

Present in: all versions across both streams
2.1.x versions ship h2 0.4.5 (vulnerable)
2.2.x versions ship h2 >= 0.4.8 (fixed)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 version at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | _(check required)_ | _(unknown -- requires git show)_ |
| 2.2.x | Cargo | release/0.4.z | _(not affected -- skipped)_ | N/A |

Note: The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812).
The fix was released in h2 0.4.8. Since 2.2.x already ships 0.4.8+, only the 2.1.x
stream's upstream branch needs to be checked for fix availability.
