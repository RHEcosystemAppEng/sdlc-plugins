# Step 2 -- Version Impact Analysis: TC-8005

## Stream Scope

This issue is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`).
Konflux Release Repo: rhtpa-release.0.4.z

## Supportability Matrix (2.2.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4

| Tag | openssl-libs version (rpms.lock.yaml) |
|-----|---------------------------------------|
| v0.4.5 | 3.0.7-25.el9_3 |
| v0.4.8 | 3.0.7-27.el9_4 |
| v0.4.9 | _(retag of v0.4.8)_ |
| v0.4.11 | 3.0.7-28.el9_4 |
| v0.4.12 | 3.0.7-28.el9_4 |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fixed version |

## Cross-Stream Analysis

The issue is scoped to 2.2.x only. The 2.1.x stream data (from rhtpa-release.0.3.z) shows:

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 (out of scope for this issue) |
| 2.1.1 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 (out of scope for this issue) |

Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue or may require separate PSIRT triage.

## Summary

- **Affected versions (in scope)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (in scope)**: 2.2.3, 2.2.4
- **Cross-stream impact**: 2.1.x stream is also affected (all versions)
