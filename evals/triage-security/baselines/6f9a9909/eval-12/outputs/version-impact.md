# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8** (affected); **h2 >= 0.4.8** (fixed)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend Tag | h2 version | Affected? | Notes |
|--------|---------|-------------|------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix version) |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | **AFFECTED** -- all versions ship h2 0.4.5 (vulnerable) |
| 2.2.x | (none) | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 (fixed) |

## Issue Scope Analysis

- **Issue stream scope**: 2.2.x (from suffix `[rhtpa-2.2]`)
- **In-scope (2.2.x)**: NO versions affected -- all 2.2.x versions ship h2 >= 0.4.8
- **Cross-stream (2.1.x)**: YES -- 2.1.x versions ship h2 0.4.5 (vulnerable)

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock at all inspected tags)
  Ecosystem: Cargo (crates.io)
  Profile: production (h2 is an HTTP/2 runtime dependency)

  Stream 2.1.x: h2 0.4.5 (affected, present since 2.1.0)
  Stream 2.2.x: h2 0.4.8+ (not affected, already at fix version since 2.2.0)

Remediation approach: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at branch tag | Fixed? |
|--------|-----------|-----------------|------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | **NO** -- requires upstream backport |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES -- already fixed |

The 2.1.x upstream branch (`release/0.3.z`) still ships h2 0.4.5 and requires an upstream backport to bump h2 to >= 0.4.8. The 2.2.x upstream branch already ships h2 >= 0.4.8.
