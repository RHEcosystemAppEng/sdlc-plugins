# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### 2.2.x Stream (scoped stream)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | v0.4.5 pinned commit |
| 2.2.1 | 3.0.7-27.el9_4 | YES | v0.4.8 pinned commit |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | v0.4.11 pinned commit; equals fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | v0.4.12 pinned commit; equals fixed version |

### 2.1.x Stream (cross-stream check for Case A)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | v0.3.8 pinned commit |
| 2.1.1 | 3.0.7-24.el9 | YES | v0.3.12 pinned commit |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are NOT affected.
- **2.1.x stream**: all released versions (2.1.0, 2.1.1) are affected. This triggers Case A (cross-stream impact) in Step 8.

## Dependency Chain

### openssl-libs (RPM)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available in this environment
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package openssl-libs is present in `rpms.lock.yaml` at the pinned commits for each version, confirming it is an **explicit install** (not inherited from the base image).

SBOM verification via cosign was not performed because cosign is not available in the current environment. The rpms.lock.yaml classification is used as the sole determination of package origin.

## Upstream Fix Status

RPM ecosystem does not have an Upstream Branch configured in the Ecosystem Mappings table. Upstream fix status check is not applicable for system packages managed via rpms.lock.yaml. The fix is tracked via the Red Hat Security Advisory [RHSA-2026:4021](https://access.redhat.com/errata/RHSA-2026:4021).
