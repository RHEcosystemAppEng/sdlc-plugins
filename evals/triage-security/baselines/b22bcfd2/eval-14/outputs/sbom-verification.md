# Step 2.3.5 -- SBOM Verification Results

## Overview

This document presents the SBOM verification results for CVE-2026-40215 (openssl-libs) alongside the rpms.lock.yaml classification for the affected versions in the 2.2.x stream. Cosign is available at `/usr/bin/cosign`, so SBOM comparison was performed.

## cosign Availability Check

```
$ which cosign
/usr/bin/cosign
```

cosign is available. Proceeding with SBOM verification.

## SBOM Comparison Procedure

For each affected version (2.2.0 through 2.2.2), the following steps were performed:

1. Downloaded the final container image SBOM using `cosign download sbom <image-reference>@<image-digest>`
2. Extracted the base image reference from the Dockerfile's `FROM` line
3. Downloaded the base image SBOM using `cosign download sbom <base-image-reference>`
4. Checked whether openssl-libs appears in both SBOMs

## Results -- rpms.lock.yaml and SBOM Signals Side by Side

| Version | Pinned Tag | rpms.lock.yaml Classification | SBOM: In Final Image? | SBOM: In Base Image? | SBOM Classification | Agreement? |
|---------|------------|-------------------------------|----------------------|---------------------|---------------------|------------|
| 2.2.0 | `v0.4.5` | **Explicit install** (present in rpms.lock.yaml) | Yes | Yes | **Base image** (in both SBOMs) | **DISAGREE** |
| 2.2.1 | `v0.4.8` | **Explicit install** (present in rpms.lock.yaml) | Yes | Yes | **Base image** (in both SBOMs) | **DISAGREE** |
| 2.2.2 | `v0.4.9` | **Explicit install** (present in rpms.lock.yaml, retag of 2.2.1) | Yes | Yes | **Base image** (in both SBOMs, retag of 2.2.1) | **DISAGREE** |

### Versions 2.2.3 and 2.2.4 (not affected)

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4, which is the fixed version. SBOM verification was not performed for non-affected versions as it is not relevant to remediation path determination.

## Disagreement Analysis

For all affected versions (2.2.0 through 2.2.2), the two classification signals **disagree**:

| Signal | Classification | Reasoning |
|--------|---------------|-----------|
| **rpms.lock.yaml** (primary) | Explicit install | openssl-libs is listed in rpms.lock.yaml, indicating it was intentionally specified as a package to install |
| **SBOM comparison** (supplementary) | Base image | openssl-libs appears in BOTH the final container image SBOM and the base image SBOM, indicating the package is inherited from the base image |

### Warning Issued

> **WARNING -- SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

This discrepancy could arise from several scenarios:
- The package is present in the base image AND also explicitly pinned in rpms.lock.yaml (dual source)
- The rpms.lock.yaml entry may be a lockfile artifact that mirrors what the base image provides (redundant pin)
- The base image was rebuilt to include a version that matches the rpms.lock.yaml specification

### Primary Signal Decision

Per the skill's design, the **rpms.lock.yaml classification remains the primary signal**. The SBOM result supplements but does not override the lock file classification. The discrepancy is flagged to the engineer for manual investigation.

## Impact on Remediation Path

Because the primary signal (rpms.lock.yaml) classifies openssl-libs as an **explicit install**, the remediation path is:

- Update the package version specification in rpms.in.yaml / rpms.lock.yaml to require >= 3.0.7-28.el9_4
- Regenerate the lock file if applicable
- The engineer should also investigate the SBOM disagreement to determine whether both the rpms.lock.yaml entry and the base image reference need to be updated

## Summary

- **cosign available**: Yes (`/usr/bin/cosign`)
- **SBOM comparison performed**: Yes, for affected versions 2.2.0-2.2.2
- **rpms.lock.yaml classification**: Explicit install (openssl-libs present in lock file)
- **SBOM classification**: Base image (openssl-libs in both final and base image SBOMs)
- **Agreement**: No -- signals disagree for all affected versions
- **Action**: Discrepancy flagged to engineer for manual investigation. rpms.lock.yaml classification used as primary signal for remediation path determination.
