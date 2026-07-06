# Step 2.3.5 -- SBOM Verification: TC-8005

## Dependency Chain for openssl-libs (RPM)

cosign is available at `/usr/bin/cosign`. SBOM verification was performed for all affected versions.

### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  !! DISCREPANCY: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: DISPUTED -- see discrepancy note below

Remediation: update the package spec in rpms.lock.yaml (primary signal),
but investigate base image origin flagged by SBOM.
```

### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  !! DISCREPANCY: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: DISPUTED -- see discrepancy note below

Remediation: update the package spec in rpms.lock.yaml (primary signal),
but investigate base image origin flagged by SBOM.
```

### Version 2.2.2 (tag v0.4.9, retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image (same as 2.2.1)
  !! DISCREPANCY: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: DISPUTED -- see discrepancy note below

Remediation: update the package spec in rpms.lock.yaml (primary signal),
but investigate base image origin flagged by SBOM.
```

### Versions 2.2.3 and 2.2.4 (not affected)

These versions ship openssl-libs 3.0.7-28.el9_4, which matches the fixed version. SBOM verification was not performed for non-affected versions.

## Classification Signal Comparison

| Version | rpms.lock.yaml Signal | rpms.lock.yaml Classification | SBOM Signal | SBOM Classification | Agreement? |
|---------|----------------------|-------------------------------|-------------|---------------------|------------|
| 2.2.0 | openssl-libs present (3.0.7-25.el9_3) | explicit install | present in both final and base image SBOMs | base image | NO |
| 2.2.1 | openssl-libs present (3.0.7-27.el9_4) | explicit install | present in both final and base image SBOMs | base image | NO |
| 2.2.2 | openssl-libs present (3.0.7-27.el9_4) | explicit install (retag of 2.2.1) | present in both final and base image SBOMs (retag of 2.2.1) | base image | NO |

## Discrepancy Analysis

For all affected versions (2.2.0 through 2.2.2), the two classification signals disagree:

- **rpms.lock.yaml** (PRIMARY signal): openssl-libs IS listed in the lock file, classifying it as an **explicit install**. This means the package is intentionally pinned and managed through rpms.lock.yaml / rpms.in.yaml.
- **SBOM comparison** (supplementary signal): openssl-libs appears in BOTH the final image SBOM and the base image SBOM, classifying it as a **base image** package inherited from the `FROM` image.

> **Warning**: SBOM classification disagrees with rpms.lock.yaml for versions 2.2.0, 2.2.1, and 2.2.2. The lock file says **explicit install** but the SBOM comparison says **base image**. This could indicate that the package is both inherited from the base image AND explicitly pinned in the lock file (e.g., to override the base image version). Investigate manually to determine the correct remediation path.

**rpms.lock.yaml remains the primary signal** -- SBOM supplements but does not override the lock file classification. Remediation should target the rpms.lock.yaml / rpms.in.yaml package spec as the primary action, while the engineer investigates whether the base image also needs updating or if the explicit pin is intentionally overriding the base image version.
