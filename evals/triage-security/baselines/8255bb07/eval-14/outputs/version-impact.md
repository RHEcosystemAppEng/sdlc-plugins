# Step 2 -- Version Impact Analysis

## Stream Scope

This analysis is scoped to the **2.2.x** stream per the issue suffix `[rhtpa-2.2]`.

## Supportability Matrix (2.2.x stream -- rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs version | Affected? | Notes |
|---------|---------------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1: 3.0.7-27.el9_4) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

## Evidence

Lock file evidence obtained via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each pinned tag in the supportability matrix:

- **v0.4.5** (2.2.0): openssl-libs 3.0.7-25.el9_3 -- AFFECTED
- **v0.4.8** (2.2.1): openssl-libs 3.0.7-27.el9_4 -- AFFECTED
- **v0.4.9** (2.2.2): retag of v0.4.8, skipped -- same result as 2.2.1 -- AFFECTED
- **v0.4.11** (2.2.3): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (matches fix version)
- **v0.4.12** (2.2.4): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (matches fix version)

## Summary

Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable version of openssl-libs (below the fix threshold of 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already include the fixed version.

The fix was picked up in version 2.2.3 (build 0.4.11, built 2026-03-23). Remediation is only needed for deployments still running 2.2.0, 2.2.1, or 2.2.2.
