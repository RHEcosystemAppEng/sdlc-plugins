# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix-mock.md. The issue is scoped to stream `[rhtpa-2.2]`, so analysis covers the 2.2.x stream versions.

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Extracted serde_json versions from Cargo.lock at each pinned commit tag:

| Tag | serde_json version | Source |
|-----|-------------------|--------|
| `v0.4.5` | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| `v0.4.8` | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| `v0.4.9` | _(retag of v0.4.8)_ | Carried forward from v0.4.8 |
| `v0.4.11` | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| `v0.4.12` | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | serde_json | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fixed) |
| 2.2.1 | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fixed) |
| 2.2.2 | 1.0.138 | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fixed) |
| 2.2.4 | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fixed) |

**Result: No supported versions in the 2.2.x stream are affected.** All versions ship serde_json >= 1.0.135, which is at or above the fixed version. The vulnerable range (< 1.0.135) does not apply to any version in this stream.

### Cross-stream check (informational)

Although the issue is scoped to 2.2.x, the 2.1.x stream also ships patched versions:

| Version | serde_json | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fixed) |
| 2.1.1 | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fixed) |

No versions in any stream are affected by this CVE.
