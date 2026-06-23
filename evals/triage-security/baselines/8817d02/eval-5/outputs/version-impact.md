# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream, scoped)

The issue is scoped to stream 2.2.x (Konflux release repo: rhtpa-release.0.4.z).

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM. Lock file: `rpms.lock.yaml`.
CVE-2026-40215 affects openssl-libs versions before 3.0.7-28.el9_4. Fixed version: 3.0.7-28.el9_4.

Simulated `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` results:

| Tag | openssl-libs version |
|-----|----------------------|
| `v0.4.5` | 3.0.7-25.el9_3 |
| `v0.4.8` | 3.0.7-27.el9_4 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 3.0.7-28.el9_4 |
| `v0.4.12` | 3.0.7-28.el9_4 |

## 2.3.5 -- Dependency Chain Context

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml confirms: openssl-libs present in lock file at each tag
- Origin: **explicit install** (package is present in rpms.lock.yaml, not just inherited from base image)
- Remediation path: update the package spec in rpms.lock.yaml (or rpms.in.yaml) in the Konflux release repo

The package is present in rpms.lock.yaml across all 2.2.x versions, indicating it is an explicitly locked RPM dependency. Remediation requires updating the locked RPM version in the Konflux release repo.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 already ship the fixed version.

## Cross-Stream Analysis (2.1.x stream)

Although this issue is scoped to 2.2.x, the version impact analysis also examines the 2.1.x stream for cross-stream impact (Step 7 Case B):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |
| 2.1.1 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |

Both 2.1.x versions ship vulnerable openssl-libs. This is relevant for Case B cross-stream proactive remediation.

## 2.5 -- Upstream Fix Check

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table. Upstream fix check is not applicable for system packages -- the fix comes from the RPM vendor (Red Hat) via errata, not from source repo branches.

The Red Hat Security Advisory RHSA-2026:4021 confirms the fix is available as openssl-libs-3.0.7-28.el9_4.
