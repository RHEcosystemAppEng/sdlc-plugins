# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z (2.2.x stream)
Last-Updated: 2026-06-28T10:00:00Z (25 days ago -- exceeds 14-day staleness threshold)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings for 2.2.x:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Lock file: `rpms.lock.yaml`
Package: openssl-libs
Fixed version: 3.0.7-28.el9_4

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## 2.3.5 -- Dependency Chain Context

### openssl-libs (RPM) -- versions 2.2.0, 2.2.1, 2.2.2

**Classification signals (side by side):**

| Version | rpms.lock.yaml | SBOM (final image) | SBOM (base image) | Classification |
|---------|----------------|---------------------|--------------------|----------------|
| 2.2.0 (v0.4.5) | present -- explicit install | present | present | **DISAGREE** |
| 2.2.1 (v0.4.8) | present -- explicit install | present | present | **DISAGREE** |
| 2.2.2 (v0.4.9) | present -- explicit install | present | present | **DISAGREE** (same as 2.2.1, retag) |

**rpms.lock.yaml classification:** openssl-libs is listed in rpms.lock.yaml for all three affected versions, indicating **explicit install**.

**SBOM verification (cosign available at /usr/bin/cosign):**
For each affected version, the final image SBOM and base image SBOM were compared:
- Final image SBOM: openssl-libs **present**
- Base image SBOM: openssl-libs **present**
- SBOM conclusion: present in both SBOMs -- **base image** origin

**Disagreement detected:**

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

The rpms.lock.yaml lists openssl-libs (suggesting it was explicitly installed), but the SBOM comparison shows the package is present in both the final and base image SBOMs (suggesting it is inherited from the base image). This disagreement requires manual investigation to determine:
1. Whether openssl-libs in rpms.lock.yaml is an intentional explicit install that overrides the base image version, or
2. Whether the rpms.lock.yaml entry is a lock of the base-image-provided package (some lock file generators capture all installed packages, not just explicitly added ones).

**Dependency chain output:**

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: present in both final and base image SBOMs --> base image (DISAGREES with lock file)

  WARNING: SBOM classification disagrees with rpms.lock.yaml --
    rpms.lock.yaml says explicit install, but SBOM comparison says base image.
    Investigate manually to determine the true origin.

  Versions affected: 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), 2.2.2 (3.0.7-27.el9_4, retag of 2.2.1)
  Fixed version: 3.0.7-28.el9_4
  First fixed in: 2.2.3 (v0.4.11)

  Remediation (if explicit install):
    Update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.

  Remediation (if base image):
    Update base image tag/digest to a version that includes patched openssl-libs.
    Check base image errata or container catalog for available updates.
```

## 2.4 -- Version Impact Table (presented to engineer)

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 3.0.7-25.el9_3 | YES    |       |
| 2.2.1   | 3.0.7-27.el9_4 | YES    |       |
| 2.2.2   | 3.0.7-27.el9_4 | YES    | retag of 2.2.1 |
| 2.2.3   | 3.0.7-28.el9_4 | NO     | equals fixed version |
| 2.2.4   | 3.0.7-28.el9_4 | NO     | equals fixed version |
```

## Cross-Stream Impact (informational)

Since this issue is scoped to the 2.2.x stream, the 2.1.x stream was also checked for informational purposes:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

The 2.1.x stream is also affected. This will be reported in Step 8 (Case B -- cross-stream impact) if no sibling CVE Jira exists for stream 2.1.x.

## 2.5 -- Upstream Fix Status

RPM ecosystem has no upstream branch configured (Upstream Branch column is empty for the RPM row in Ecosystem Mappings). The fix for openssl-libs is provided by the base OS vendor via errata RHSA-2026:4021. No upstream source repo fix check is applicable for system packages.
