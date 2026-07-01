# Step 2 -- Version Impact Analysis for CVE-2026-40215

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Cross-stream versions (out of scope, for Case B reference)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | stream 2.1.x |
| 2.1.1 | 3.0.7-24.el9 | YES | stream 2.1.x |

**Summary**: Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are not affected.

The 2.1.x stream is also affected (all versions ship 3.0.7-24.el9) but is outside this issue's scope.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

**Package origin classification**: openssl-libs is present in rpms.lock.yaml, classifying it as an **explicit install**. The package is directly specified in the Konflux release repo's RPM lock file, not inherited from the base image.

**SBOM verification**: cosign is not available in this environment, so SBOM cross-validation of the rpms.lock.yaml classification was skipped. Using rpms.lock.yaml classification only.

## Upstream Fix Status

The RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table (the Upstream Branch column is empty for the RPM row). Upstream fix checking is not applicable for system packages -- the fix is provided by the RPM vendor (Red Hat) via errata. The advisory RHSA-2026:4021 confirms the fix is available in openssl-libs-3.0.7-28.el9_4.
