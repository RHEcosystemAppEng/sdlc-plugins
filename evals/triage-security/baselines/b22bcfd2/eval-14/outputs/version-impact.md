# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

The issue is scoped to the **2.2.x** stream (`[rhtpa-2.2]`). The supportability matrix for stream `rhtpa-release.0.4.z` contains the following versions:

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Since the ecosystem is **RPM**, the lock file is `rpms.lock.yaml`. For each version in the 2.2.x stream, the openssl-libs version is extracted from rpms.lock.yaml at the pinned commit tag:

| Version | Pinned Tag | Command | openssl-libs version |
|---------|------------|---------|----------------------|
| 2.2.0 | `v0.4.5` | `git show v0.4.5:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-25.el9_3 |
| 2.2.1 | `v0.4.8` | `git show v0.4.8:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-27.el9_4 |
| 2.2.2 | `v0.4.9` | retag of 2.2.1 -- skipped, carried forward | 3.0.7-27.el9_4 |
| 2.2.3 | `v0.4.11` | `git show v0.4.11:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 |
| 2.2.4 | `v0.4.12` | `git show v0.4.12:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 |

## 2.4 -- Version Impact Table

CVE-2026-40215 affects openssl-libs versions before 3.0.7-28.el9_4. Fixed version: 3.0.7-28.el9_4.

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0 through 2.2.2 ship the vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 ship the patched version.

## 2.3.5 -- Dependency Chain Context

The dependency chain analysis for openssl-libs follows the RPM / container-level investigation path.

### Package Origin Classification

**rpms.lock.yaml classification (primary signal):**
openssl-libs IS present in rpms.lock.yaml for versions 2.2.0 through 2.2.2. This classifies it as an **explicit install** -- the package is specified in the RPM lock file (rpms.in.yaml or equivalent).

### SBOM Verification

**cosign availability:** cosign IS available (`which cosign` returns `/usr/bin/cosign`).

SBOM comparison was performed for the affected versions (2.2.0 through 2.2.2) using `cosign download sbom`:

| Version | rpms.lock.yaml | Final Image SBOM | Base Image SBOM | SBOM Classification |
|---------|----------------|------------------|-----------------|---------------------|
| 2.2.0 | present (explicit install) | present | present | base image |
| 2.2.1 | present (explicit install) | present | present | base image |
| 2.2.2 | present (explicit install) | present | present | base image (retag of 2.2.1) |

**SBOM classification result:** openssl-libs appears in BOTH the final container image SBOM and the base image SBOM for versions 2.2.0 through 2.2.2. This indicates a **base image** origin per SBOM analysis.

### Disagreement Warning

> **WARNING -- SBOM classification disagrees with rpms.lock.yaml:**
> rpms.lock.yaml says **explicit install** (openssl-libs is present in rpms.lock.yaml),
> but SBOM comparison says **base image** (openssl-libs appears in both the final image SBOM
> and the base image SBOM). Investigate manually.

The rpms.lock.yaml classification remains the **primary signal** -- the SBOM result supplements but does not override it. The discrepancy is flagged for the engineer to investigate whether openssl-libs is intentionally pinned in rpms.lock.yaml despite also being present in the base image.

### Dependency Chain Summary

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install (PRIMARY)
  SBOM verification: present in BOTH final and base image SBOMs --> base image
  WARNING: SBOM classification (base image) disagrees with rpms.lock.yaml classification
  (explicit install). Investigate manually.
  Origin (per primary signal): explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml.
Note: SBOM suggests this package also comes from the base image. The engineer should
verify whether the rpms.lock.yaml entry is intentional or redundant before proceeding.
```
