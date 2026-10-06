# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs
(before 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 ship the fixed version.

### Cross-stream analysis (out of scope for this issue)

The 2.1.x stream is also affected (for Case A cross-stream impact reporting):

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

Both 2.1.x versions ship openssl-libs 3.0.7-24.el9, which is below the fix
threshold of 3.0.7-28.el9_4.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package openssl-libs is found in `rpms.lock.yaml` at each pinned build tag,
indicating it is an explicitly managed RPM dependency (not inherited from the
base image).

SBOM verification via `cosign download sbom` was not performed because `cosign`
is not available in this environment. The rpms.lock.yaml classification
(explicit install) is used as the sole determination of package origin.

## Upstream Fix Status

The RPM ecosystem has no Upstream Branch configured (column value: `--`).
Upstream fix checking is not applicable for system packages managed via
rpms.lock.yaml. The fix was incorporated in build v0.4.11 (version 2.2.3)
by updating the openssl-libs package to 3.0.7-28.el9_4.
