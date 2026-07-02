# Step 2 -- Version Impact Analysis: TC-8005

## Stream Scope

Analysis scoped to **2.2.x stream** per issue suffix `[rhtpa-2.2]`.

## Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Lock File Evidence (rpms.lock.yaml)

Extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`:

| Tag | openssl-libs version |
|-----|----------------------|
| v0.4.5 | 3.0.7-25.el9_3 |
| v0.4.8 | 3.0.7-27.el9_4 |
| v0.4.9 | _(retag of v0.4.8)_ |
| v0.4.11 | 3.0.7-28.el9_4 |
| v0.4.12 | 3.0.7-28.el9_4 |

## Version Impact Table

CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | before fixed version |
| 2.2.1 | 3.0.7-27.el9_4 | YES | before fixed version |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | matches fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | matches fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## Cross-Stream Impact (Case B Assessment)

The 2.1.x stream (rhtpa-release.0.3.z) also ships openssl-libs:

| Tag | openssl-libs version | Affected? |
|-----|----------------------|-----------|
| v0.3.8 (2.1.0) | 3.0.7-24.el9 | YES |
| v0.3.12 (2.1.1) | 3.0.7-24.el9 | YES |

Both 2.1.x versions ship vulnerable openssl-libs. However, because this issue is scoped to `[rhtpa-2.2]`, the 2.1.x stream is out of scope for remediation task creation under this issue. Cross-stream impact should be noted in a comment on TC-8005, and proactive remediation tasks should be created for the 2.1.x stream if no companion CVE Jira exists for that stream.

## Dependency Chain Context

See `sbom-verification.md` for the full dependency chain analysis including SBOM verification results.

## PROPOSAL: Affects Versions Correction (Step 3)

Current PSIRT-assigned Affects Versions: **RHTPA 2.0.0**

Based on lock file evidence, the correct Affects Versions for the 2.2.x stream are:
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

**PSIRT assigned RHTPA 2.0.0 which does not correspond to any version in the 2.2.x stream.** This appears to be a PSIRT assignment error. The Affects Versions should be corrected to reflect actual lock file evidence.

PROPOSAL: Remove RHTPA 2.0.0 and set Affects Versions to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (pending dynamic version discovery from Jira).
