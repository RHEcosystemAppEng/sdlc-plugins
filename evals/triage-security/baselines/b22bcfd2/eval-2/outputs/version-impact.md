# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from local security-matrix.md. Two streams are configured:

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

CVE-2026-28940 affects **serde_json** versions before **1.0.135**. The fix threshold
is **1.0.135**.

Ecosystem: **Cargo** -- using `Cargo.lock` at pinned commit tags for each version.

### serde_json versions extracted from lock files

| Version | Pinned Commit (tag) | serde_json version | Source |
|---------|--------------------|--------------------|--------|
| 2.1.0 | `v0.3.8` | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | `v0.3.12` | 1.0.137 | `git show v0.3.12:Cargo.lock` |
| 2.2.0 | `v0.4.5` | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | `v0.4.8` | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | `v0.4.8` | 1.0.138 | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | `v0.4.12` | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fix threshold) |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fix threshold) |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | 2.2.x | 1.0.138 | **NO** | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |

**Result**: All supported versions ship serde_json >= 1.0.135, which is at or above
the fix threshold. **No supported version is affected by CVE-2026-28940.**

Every version across both the 2.1.x and 2.2.x streams ships a patched version of
serde_json (1.0.137, 1.0.138, or 1.0.139), all of which are well above the
vulnerable range (< 1.0.135).
