# Step 2.3.5 -- SBOM Verification Results

## Dependency Chain for openssl-libs (RPM)

### Cosign availability

`which cosign` returned `/usr/bin/cosign` -- cosign is available. SBOM verification will be performed.

### Classification by version

#### Version 2.2.0 (build tag v0.4.5)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-25.el9_3) | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in both final and base image SBOMs | base image |

> **Discrepancy**: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

#### Version 2.2.1 (build tag v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-27.el9_4) | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in both final and base image SBOMs | base image |

> **Discrepancy**: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

#### Version 2.2.2 (build tag v0.4.9 -- retag of 2.2.1)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-27.el9_4) | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in both final and base image SBOMs | base image |

> **Discrepancy**: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually. (Same as 2.2.1 -- retag.)

#### Version 2.2.3 (build tag v0.4.11) -- NOT AFFECTED

openssl-libs version 3.0.7-28.el9_4 ships the fixed version. SBOM verification not required for unaffected versions.

#### Version 2.2.4 (build tag v0.4.12) -- NOT AFFECTED

openssl-libs version 3.0.7-28.el9_4 ships the fixed version. SBOM verification not required for unaffected versions.

### Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals **disagree**:

| Version | rpms.lock.yaml | SBOM comparison | Agreement? |
|---------|---------------|-----------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both SBOMs) | NO |
| 2.2.1 | explicit install (present in lock file) | base image (present in both SBOMs) | NO |
| 2.2.2 | explicit install (present in lock file) | base image (present in both SBOMs) | NO (retag of 2.2.1) |

This discrepancy means the package may be both explicitly installed via rpms.lock.yaml AND inherited from the base image. Possible explanations:

1. The rpms.lock.yaml explicitly pins a version of a package that also exists in the base image (overlay/override pattern).
2. The SBOM tooling does not distinguish between explicitly installed packages and base image packages when both are present.

**Recommendation**: The engineer should investigate whether the rpms.lock.yaml entry is intentionally overriding the base image version. If so, remediation should update the rpms.lock.yaml (explicit install path). If the lock file entry is vestigial, removing it and relying on the base image update may be the correct remediation.
