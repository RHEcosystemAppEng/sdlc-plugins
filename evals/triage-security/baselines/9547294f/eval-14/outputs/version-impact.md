# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from the 2.2.x stream's security-matrix.md. The issue is scoped to `[rhtpa-2.2]`, so only the 2.2.x stream versions are analyzed.

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Using rpms.lock.yaml data for the RPM ecosystem. The check command is `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

Extracted openssl-libs versions from rpms.lock.yaml at each pinned commit tag:

| Tag | openssl-libs version |
|-----|----------------------|
| `v0.4.5` | 3.0.7-25.el9_3 |
| `v0.4.8` | 3.0.7-27.el9_4 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 3.0.7-28.el9_4 |
| `v0.4.12` | 3.0.7-28.el9_4 |

## Version Impact Table

CVE-2026-40215 affects openssl-libs versions before 3.0.7-28.el9_4 (fixed in 3.0.7-28.el9_4).

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0 through 2.2.2 ship the vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4).

## 2.3.5 -- Dependency Chain Context

### Package Classification

Dependency chain for openssl-libs (RPM):

**rpms.lock.yaml classification**: openssl-libs is **present** in rpms.lock.yaml for versions 2.2.0 through 2.2.2 --> **explicit install**

**SBOM verification** (cosign available at /usr/bin/cosign):

For each affected version, cosign download sbom was used to compare the final container image SBOM against the base image SBOM:

- **Version 2.2.0** (tag v0.4.5):
  - `cosign download sbom <image-reference>@<image-digest>` --> final image SBOM contains openssl-libs-3.0.7-25.el9_3
  - `cosign download sbom <base-image-reference>` --> base image SBOM also contains openssl-libs-3.0.7-25.el9_3
  - SBOM result: present in **both** final and base image SBOMs --> **base image**

- **Version 2.2.1** (tag v0.4.8):
  - `cosign download sbom <image-reference>@<image-digest>` --> final image SBOM contains openssl-libs-3.0.7-27.el9_4
  - `cosign download sbom <base-image-reference>` --> base image SBOM also contains openssl-libs-3.0.7-27.el9_4
  - SBOM result: present in **both** final and base image SBOMs --> **base image**

- **Version 2.2.2** (tag v0.4.9, retag of v0.4.8):
  - Same as 2.2.1 (retag -- identical image)
  - SBOM result: present in **both** final and base image SBOMs --> **base image**

### Classification Comparison

| Version | rpms.lock.yaml | SBOM Verification | Agreement? |
|---------|---------------|-------------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both SBOMs) | **DISAGREE** |
| 2.2.1 | explicit install (present in lock file) | base image (present in both SBOMs) | **DISAGREE** |
| 2.2.2 | explicit install (present in lock file) | base image (present in both SBOMs) | **DISAGREE** |

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. The rpms.lock.yaml classification (explicit install) remains the primary signal, but this discrepancy should be investigated manually. The package may be both explicitly installed and present in the base image, or the lock file entry may be redundant.

**Primary classification (rpms.lock.yaml)**: explicit install
**SBOM cross-check**: base image (disagrees -- flagged for manual investigation)
**Origin**: explicit install per rpms.lock.yaml (primary signal)
**Remediation path**: Update the package spec in rpms.in.yaml / rpms.lock.yaml
