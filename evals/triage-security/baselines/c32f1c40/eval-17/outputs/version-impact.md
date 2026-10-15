# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Matrix loaded from security-matrix-mock.md. Two streams configured:

**Stream 2.1.x** (rhtpa-release.0.3.z):
| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

**Stream 2.2.x** (rhtpa-release.0.4.z):
| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

Lock file: `Cargo.lock` (Cargo ecosystem)
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

Dependency versions extracted at pinned commits from the supportability matrix:

| Version | Pinned Commit Tag | quinn-proto version | Affected? | Notes |
|---------|-------------------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.8 | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

All versions from the supportability matrix across both streams are included (Important Rule 4). Pinned commit tags from the supportability matrix are used for each version (Important Rule 13). Version 2.2.2 is a retag of 2.2.1, so the affected status is carried forward from 2.2.1 (Important Rule 5).

## Summary

- **2.2.x stream (scoped)**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are not affected
- **2.1.x stream (cross-stream)**: versions 2.1.0, 2.1.1 are affected -- cross-stream impact detected
