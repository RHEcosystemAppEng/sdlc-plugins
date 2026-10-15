# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

### Stream 2.2.x (scoped stream)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | 25 < 28 release |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | 27 < 28 release |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Stream 2.1.x (cross-stream reference)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | 24 < 28 release |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | 24 < 28 release |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4). The vulnerability was remediated starting with the 0.4.11 build.
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected. Both ship openssl-libs 3.0.7-24.el9, which is well below the fix threshold.

## Dependency Chain (Step 2.3.5)

### RPM origin classification

openssl-libs is **present in rpms.lock.yaml** for all inspected tags across both streams. Per the RPM origin classification rules:

- **In lock file** --> **explicit install**
- Remediation path: update the package spec in rpms.in.yaml / rpms.lock.yaml

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available in this environment
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

### SBOM Verification (Step 2.3.5)

SBOM verification was **skipped** because cosign is not available in this evaluation environment. The `which cosign` check would fail, so SBOM comparison between final and base image SBOMs could not be performed.

The rpms.lock.yaml classification (explicit install) is used as the sole origin determination. In a production triage with cosign available, the SBOM comparison would cross-check whether openssl-libs appears in both the final image SBOM and the base image SBOM to confirm the lock file classification.

## Upstream Fix Status (Step 2.5)

The RPM ecosystem in the 2.2.x Ecosystem Mappings has no Upstream Branch configured (column value: `--`). Upstream fix check is not applicable for RPM system packages -- the fix is managed through the Konflux release repo's rpms.lock.yaml directly.

Within the 2.2.x stream, the fix is already present: builds v0.4.11 (2.2.3) and v0.4.12 (2.2.4) ship openssl-libs 3.0.7-28.el9_4, confirming the package was updated in the release repo before the 2.2.3 release.
