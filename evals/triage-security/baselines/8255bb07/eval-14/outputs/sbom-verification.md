# Step 2.3.5 -- SBOM Verification Results

## Cosign Availability

```
$ which cosign
/usr/bin/cosign
```

Cosign is available. Proceeding with SBOM verification for affected versions.

## SBOM Verification for Affected Versions

For each affected version (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml classification is compared against the SBOM comparison of final image vs. base image.

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT in lock file | explicit install |
| SBOM (final image) | openssl-libs PRESENT | -- |
| SBOM (base image) | openssl-libs PRESENT | base image |
| SBOM comparison | present in BOTH final and base image SBOMs | base image origin |

**Discrepancy detected**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image origin**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

**Primary classification (rpms.lock.yaml)**: explicit install

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT in lock file | explicit install |
| SBOM (final image) | openssl-libs PRESENT | -- |
| SBOM (base image) | openssl-libs PRESENT | base image |
| SBOM comparison | present in BOTH final and base image SBOMs | base image origin |

**Discrepancy detected**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image origin**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

**Primary classification (rpms.lock.yaml)**: explicit install

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT in lock file | explicit install |
| SBOM (final image) | openssl-libs PRESENT | -- |
| SBOM (base image) | openssl-libs PRESENT | base image |
| SBOM comparison | present in BOTH final and base image SBOMs | base image origin |

**Discrepancy detected**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image origin**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

**Primary classification (rpms.lock.yaml)**: explicit install

Note: version 2.2.2 is a retag of 2.2.1 (identical backend source at v0.4.8). SBOM results carried forward from 2.2.1.

## Dependency Chain Summary

For all three affected versions (2.2.0, 2.2.1, 2.2.2):

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: present in BOTH final and base image SBOMs -> base image origin
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    - rpms.lock.yaml: explicit install (PRIMARY signal)
    - SBOM comparison: base image origin
    Investigate manually to determine whether this is a base image package
    that was also pinned in rpms.lock.yaml, or a true explicit install.
  Origin (per primary signal): explicit install

Remediation (per rpms.lock.yaml classification): update the package spec
in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
```

## Signal Disagreement Analysis

The rpms.lock.yaml lists openssl-libs as an explicit install, while the SBOM comparison shows the package is present in both the final image and the base image. This disagreement can occur when:

1. The base image already ships openssl-libs (as a core UBI package), AND
2. The rpms.lock.yaml explicitly pins the same package (possibly to control the exact version or ensure it is present regardless of base image content).

In this scenario, the package has dual provenance -- it exists in the base image but is also explicitly declared in the RPM lock file. The rpms.lock.yaml classification takes precedence as the primary signal because it represents the build intent: the maintainers explicitly chose to manage this package version.

**Recommendation to engineer**: Investigate whether the openssl-libs entry in rpms.lock.yaml is intentional version pinning (in which case, update the pin to >= 3.0.7-28.el9_4) or a residual entry that could be removed (letting the base image provide the package). Either way, the vulnerability is present and remediation is required for versions 2.2.0, 2.2.1, and 2.2.2.
