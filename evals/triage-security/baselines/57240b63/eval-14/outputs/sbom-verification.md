# Step 2.3.5 -- SBOM Verification Results: TC-8005

## Overview

This file documents the dependency chain classification for openssl-libs (RPM ecosystem) across affected versions in the 2.2.x stream, including the SBOM cross-verification results from cosign.

cosign availability: `/usr/bin/cosign` (confirmed via `which cosign`)

## Classification Method

Two independent signals are used to classify the package origin:

1. **rpms.lock.yaml** -- if the package appears in the lock file, it is classified as an **explicit install**; if absent, it is a **base image** package.
2. **SBOM comparison** -- the final container image SBOM is compared against the base image SBOM:
   - Present in final SBOM but NOT in base SBOM --> explicit install
   - Present in BOTH final and base SBOMs --> base image package

## SBOM Verification Results by Version

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3) -- AFFECTED

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** in lock file | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in **BOTH** final and base image SBOMs | base image |

> **DISAGREEMENT**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4) -- AFFECTED

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** in lock file | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in **BOTH** final and base image SBOMs | base image |

> **DISAGREEMENT**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

### Version 2.2.2 (tag v0.4.9, retag of v0.4.8) -- AFFECTED

Same as version 2.2.1 (retag -- identical source commits and image contents).

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** in lock file | explicit install |
| Final image SBOM | openssl-libs **present** | -- |
| Base image SBOM | openssl-libs **present** | base image |
| SBOM comparison | present in **BOTH** final and base image SBOMs | base image |

> **DISAGREEMENT**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

### Version 2.2.3 (tag v0.4.11, openssl-libs 3.0.7-28.el9_4) -- NOT AFFECTED

Not affected (ships fixed version). SBOM verification not required for unaffected versions.

### Version 2.2.4 (tag v0.4.12, openssl-libs 3.0.7-28.el9_4) -- NOT AFFECTED

Not affected (ships fixed version). SBOM verification not required for unaffected versions.

## Summary of Disagreements

| Version | rpms.lock.yaml | SBOM comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install | base image | DISAGREE |
| 2.2.1 | explicit install | base image | DISAGREE |
| 2.2.2 | explicit install (retag of 2.2.1) | base image (retag of 2.2.1) | DISAGREE |
| 2.2.3 | N/A (not affected) | N/A | -- |
| 2.2.4 | N/A (not affected) | N/A | -- |

## Interpretation

The disagreement across all three affected versions indicates that openssl-libs is **both** explicitly listed in rpms.lock.yaml (suggesting an intentional install) **and** present in the base image (inherited from the FROM image). This can occur when:

1. The rpms.lock.yaml explicitly pins a package that also exists in the base image, potentially to control the exact version installed.
2. The package was added to rpms.lock.yaml to override or ensure a specific version different from what the base image provides.
3. The lock file was generated from the full image contents (including base image packages) rather than only explicitly-added packages.

**This disagreement requires manual investigation** to determine the correct remediation path:

- If openssl-libs is intentionally pinned in rpms.lock.yaml to override the base image version, remediation should update the pin in rpms.lock.yaml (or rpms.in.yaml) to the fixed version (3.0.7-28.el9_4).
- If openssl-libs appears in rpms.lock.yaml only because the lock file captures all installed packages (including base image packages), then remediation should focus on updating the base image to one that includes the patched openssl-libs.

Both remediation paths may be needed -- update the base image AND update the lock file pin.

## Dependency Chain Output (per skill format)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: present in BOTH final and base image SBOMs --> base image
  DISAGREEMENT: rpms.lock.yaml classification (explicit install) does not match
    SBOM comparison (base image). Investigate manually.
  Origin: DISPUTED -- manual investigation required
  
  Possible remediation paths:
  1. Update openssl-libs pin in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
  2. Update base image to a version that includes patched openssl-libs
  3. Both (if the lock file pin is intentional AND the base image should be updated)
```
