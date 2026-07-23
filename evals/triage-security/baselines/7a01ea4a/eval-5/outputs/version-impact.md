# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Scoped stream**: 2.2.x (per issue suffix `[rhtpa-2.2]`)

### Cross-stream data (2.1.x -- outside issue scope, for Case B analysis)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 3.0.7-24.el9 | YES | |

## Evidence Sources

All openssl-libs versions extracted from `rpms.lock.yaml` at pinned tags per the security matrix:

| Tag | rpms.lock.yaml openssl-libs version |
|-----|-------------------------------------|
| v0.4.5 (2.2.0) | 3.0.7-25.el9_3 |
| v0.4.8 (2.2.1) | 3.0.7-27.el9_4 |
| v0.4.9 (2.2.2) | retag of v0.4.8 -- skipped, same as 2.2.1 |
| v0.4.11 (2.2.3) | 3.0.7-28.el9_4 |
| v0.4.12 (2.2.4) | 3.0.7-28.el9_4 |

## Dependency Chain

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml: present -- explicit install
- SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
- Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.

## Upstream Fix Status

Not applicable for RPM ecosystem -- no upstream branch configured. The fix is available in the RPM repository as version 3.0.7-28.el9_4 per RHSA-2026:4021. Versions 2.2.3 and 2.2.4 already ship the fixed version.
