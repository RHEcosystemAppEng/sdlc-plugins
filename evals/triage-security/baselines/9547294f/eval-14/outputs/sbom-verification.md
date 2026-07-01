# Step 2.3.5 -- SBOM Verification Results

## cosign Availability

```
$ which cosign
/usr/bin/cosign
```

cosign is available. Proceeding with SBOM verification to cross-check the rpms.lock.yaml classification.

## SBOM Comparison Methodology

For each affected version (2.2.0 through 2.2.2), the following procedure was performed:

1. Download the final container image SBOM using `cosign download sbom <image-reference>@<image-digest>`
2. Extract the base image reference from the Dockerfile's `FROM` line
3. Download the base image SBOM using `cosign download sbom <base-image-reference>`
4. Compare openssl-libs presence in both SBOMs

## Results by Version

### Version 2.2.0 (tag v0.4.5)

| Signal | Classification | Evidence |
|--------|---------------|----------|
| rpms.lock.yaml | **explicit install** | openssl-libs is listed in rpms.lock.yaml at version 3.0.7-25.el9_3 |
| SBOM verification | **base image** | openssl-libs-3.0.7-25.el9_3 appears in BOTH the final image SBOM and the base image SBOM |

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

### Version 2.2.1 (tag v0.4.8)

| Signal | Classification | Evidence |
|--------|---------------|----------|
| rpms.lock.yaml | **explicit install** | openssl-libs is listed in rpms.lock.yaml at version 3.0.7-27.el9_4 |
| SBOM verification | **base image** | openssl-libs-3.0.7-27.el9_4 appears in BOTH the final image SBOM and the base image SBOM |

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

### Version 2.2.2 (tag v0.4.9, retag of v0.4.8)

| Signal | Classification | Evidence |
|--------|---------------|----------|
| rpms.lock.yaml | **explicit install** | Same as 2.2.1 (retag -- identical source commits and lock file) |
| SBOM verification | **base image** | openssl-libs appears in BOTH the final image SBOM and the base image SBOM (same as 2.2.1, retag) |

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

## Summary Comparison Table

| Version | rpms.lock.yaml Classification | SBOM Verification Result | Agreement? | Action |
|---------|-------------------------------|--------------------------|------------|--------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both final and base image SBOMs) | **DISAGREE** | Flag for manual investigation |
| 2.2.1 | explicit install (present in lock file) | base image (present in both final and base image SBOMs) | **DISAGREE** | Flag for manual investigation |
| 2.2.2 | explicit install (retag of 2.2.1) | base image (retag of 2.2.1) | **DISAGREE** | Flag for manual investigation |

## Classification Decision

**rpms.lock.yaml remains the primary signal.** The rpms.lock.yaml classification of **explicit install** is used as the authoritative classification for remediation planning. The SBOM verification result of **base image** is a supplementary signal that disagrees with the primary classification.

This discrepancy indicates that openssl-libs may be:
- Explicitly installed via rpms.in.yaml but also inherited from the base image (redundant install)
- A package that is present in the base image but was pinned in the lock file for version control purposes

The engineer should investigate manually to determine whether the rpms.lock.yaml entry is intentional (explicit version pinning) or an artifact that should be cleaned up.

**Effective classification for remediation**: explicit install (per rpms.lock.yaml, primary signal)

## Versions Not Affected (2.2.3 and 2.2.4)

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4, which is the fixed version. SBOM verification was not performed for these versions as they are not affected by the CVE.
