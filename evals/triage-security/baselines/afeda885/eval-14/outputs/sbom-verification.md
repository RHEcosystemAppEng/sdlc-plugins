# Step 2.3.5 -- SBOM Verification Results: TC-8005

## Dependency Chain Context for openssl-libs (RPM)

Ecosystem: RPM (system package)
Package: openssl-libs
cosign availability: /usr/bin/cosign (available)

## SBOM Verification by Version

For each affected version (2.2.0 through 2.2.2), both rpms.lock.yaml and SBOM
signals were checked side by side.

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT | explicit install |
| Final image SBOM | openssl-libs PRESENT | -- |
| Base image SBOM | openssl-libs PRESENT | base image origin |
| SBOM classification | In both final and base image SBOMs | base image |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin. Investigate manually.

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT | explicit install |
| Final image SBOM | openssl-libs PRESENT | -- |
| Base image SBOM | openssl-libs PRESENT | base image origin |
| SBOM classification | In both final and base image SBOMs | base image |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin. Investigate manually.

### Version 2.2.2 (tag v0.4.9, retag of v0.4.8 -- same as 2.2.1)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs PRESENT | explicit install |
| Final image SBOM | openssl-libs PRESENT | -- |
| Base image SBOM | openssl-libs PRESENT | base image origin |
| SBOM classification | In both final and base image SBOMs | base image |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin. Investigate manually.

## Summary Table

| Version | openssl-libs version | rpms.lock.yaml | SBOM (final) | SBOM (base) | rpms.lock.yaml classification | SBOM classification | Agreement? |
|---------|---------------------|----------------|-------------|-------------|------------------------------|---------------------|------------|
| 2.2.0 | 3.0.7-25.el9_3 | PRESENT | PRESENT | PRESENT | explicit install | base image | NO |
| 2.2.1 | 3.0.7-27.el9_4 | PRESENT | PRESENT | PRESENT | explicit install | base image | NO |
| 2.2.2 | 3.0.7-27.el9_4 | PRESENT | PRESENT | PRESENT | explicit install | base image | NO |

## Interpretation

The rpms.lock.yaml lists openssl-libs for all three affected versions (2.2.0,
2.2.1, 2.2.2), classifying it as an **explicit install**. However, SBOM
comparison shows the package is present in **both** the final image SBOM and
the base image SBOM for all three versions, which indicates **base image origin**.

This disagreement means one of the following:
1. openssl-libs is both inherited from the base image AND explicitly pinned in
   rpms.lock.yaml (the lock file may be re-declaring a base image package to pin
   a specific version).
2. The rpms.lock.yaml entry may be a lockfile artifact that mirrors base image
   contents rather than representing a true explicit install.

**Recommendation**: Investigate manually to determine the true origin. If
openssl-libs is effectively a base image package that is also listed in the
lock file, the remediation path may be either:
- Update the base image to a version shipping openssl-libs >= 3.0.7-28.el9_4, OR
- Update the explicit pin in rpms.lock.yaml / rpms.in.yaml to >= 3.0.7-28.el9_4

The engineer should verify which approach is appropriate for the build pipeline.
