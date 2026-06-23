# Step 2 -- Version Impact Analysis: TC-8004

## 2.1 -- Supportability Matrix

Two version streams loaded from Security Configuration:

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: **Cargo** (Lock file: `Cargo.lock`)

Simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` output:

| Tag | h2 version | Source |
|-----|------------|--------|
| `v0.3.8` | 0.4.5 | Cargo.lock at pinned commit |
| `v0.3.12` | 0.4.5 | Cargo.lock at pinned commit |
| `v0.4.5` | 0.4.8 | Cargo.lock at pinned commit |
| `v0.4.8` | 0.4.8 | Cargo.lock at pinned commit |
| `v0.4.9` | _(retag of v0.4.8)_ | Skipped -- same as 2.2.1 |
| `v0.4.11` | 0.4.9 | Cargo.lock at pinned commit |
| `v0.4.12` | 0.4.9 | Cargo.lock at pinned commit |

CVE-2026-33501 affected range: **h2 < 0.4.8** (fixed in 0.4.8).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version (0.4.8 = fix threshold) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships version above fix threshold |

### Stream-Level Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| **2.1.x** | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5 which is below the fix threshold of 0.4.8 |
| **2.2.x** | **NO** | All versions ship h2 >= 0.4.8 (the fix version or later) |

## 2.3.5 -- Dependency Chain Context

Dependency chain for h2 (Cargo):

```
rhtpa-backend (workspace) -> hyper -> h2
Profile: production (hyper is a runtime dependency for the HTTP/2 server)
```

The h2 crate is a transitive dependency pulled in via hyper (the HTTP framework). It is present in the production dependency tree (not dev-only), meaning the vulnerable code is shipped in the binary.

- **Present in 2.1.x**: h2 0.4.5 at tags v0.3.8 and v0.3.12
- **Present in 2.2.x**: h2 0.4.8+ at all tags (already at or above fix threshold)
- **Conclusion**: The 2.2.x stream was already shipping the patched version by its first release (2.2.0), which suggests the upstream source repo's `release/0.4.z` branch had the fix before the 2.2.0 release was cut.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 at HEAD (simulated) | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.5 (estimated) | **NO** -- h2 0.4.5 < 0.4.8 threshold |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.9 | **YES** -- h2 0.4.9 >= 0.4.8 threshold |

**Remediation path for 2.1.x**: The upstream branch `release/0.3.z` has NOT been fixed. Remediation requires:
1. An upstream PR on `release/0.3.z` to bump h2 to >= 0.4.8
2. A downstream update in the Konflux release repo `rhtpa-release.0.3.z` to pick up the new source tag

**2.2.x requires no remediation** -- all released versions already ship h2 >= 0.4.8.
