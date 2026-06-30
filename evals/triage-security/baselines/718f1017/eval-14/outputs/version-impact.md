# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

Matrix loaded from: 2.2.x stream (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: rpms.lock.yaml
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4 (from Jira description)

### Extracted versions

| Version | Tag | openssl-libs version | Source |
|---------|-----|----------------------|--------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | rpms.lock.yaml |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | rpms.lock.yaml |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | rpms.lock.yaml |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | rpms.lock.yaml |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

| Version | openssl-libs version | Affected? | Notes |
|---------|----------------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fix version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fix version |

### Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- Versions 2.2.0 through 2.2.2 ship openssl-libs below the fix threshold (3.0.7-28.el9_4)
- Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4)

## Cross-Stream Impact

The 2.1.x stream (outside the scope of this issue) also ships vulnerable openssl-libs versions:

| Version | openssl-libs version | Affected? |
|---------|----------------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

This cross-stream impact would be reported via comment on the CVE Jira (Step 7 Case B), but remediation task creation is scoped to the 2.2.x stream only for this issue.
