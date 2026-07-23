# Step 2 -- Version Impact Analysis

## Supportability Matrix (2.2.x stream)

Loaded from: rhtpa-release.0.4.z security-matrix.md (2.2.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------------------------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable version of openssl-libs. Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).

## Cross-Stream Overview (informational, outside issue scope)

The 2.1.x stream is also affected (outside this issue's scope):

| Version | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------------------------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

This cross-stream impact is noted for Case B handling in Step 8.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` at each pinned tag, classifying it as an **explicit install** (not inherited from the base image).

SBOM verification via cosign was not performed because cosign is not available in this environment. The rpms.lock.yaml classification is used as the sole source for package origin determination.

## Upstream Fix Status

No upstream branch is configured for the RPM ecosystem (Upstream Branch column is empty in the Ecosystem Mappings table). Upstream fix check is not applicable for system packages -- the fix comes from the RPM vendor (Red Hat) via RHSA-2026:4021.

The fixed package version (3.0.7-28.el9_4) is already available per the advisory and is already shipping in versions 2.2.3+.
