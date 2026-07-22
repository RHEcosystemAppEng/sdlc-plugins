# Step 2 -- Version Impact Analysis

## Issue: TC-8005 -- CVE-2026-40215 (openssl-libs)

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z`
Last-Updated: 2026-06-28T10:00:00Z (24 days ago -- within 14-day staleness threshold)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Fixed version threshold: **3.0.7-28.el9_4**

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## 2.3.5 -- Dependency Chain (RPM)

### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: openssl-libs-3.0.7-25.el9_3 present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both SBOMs)
  rpms.lock.yaml classification: explicit install (present in lock file)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    -> rpms.lock.yaml says explicit install but SBOM comparison says base image
    -> Investigate manually
  Origin: DISPUTED (rpms.lock.yaml: explicit install / SBOM: base image)

Remediation: investigate discrepancy before proceeding. If explicit install
is confirmed, update the package spec in rpms.in.yaml / rpms.lock.yaml.
If base image origin is confirmed, update the base image reference.
```

### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: openssl-libs-3.0.7-27.el9_4 present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both SBOMs)
  rpms.lock.yaml classification: explicit install (present in lock file)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    -> rpms.lock.yaml says explicit install but SBOM comparison says base image
    -> Investigate manually
  Origin: DISPUTED (rpms.lock.yaml: explicit install / SBOM: base image)

Remediation: investigate discrepancy before proceeding. If explicit install
is confirmed, update the package spec in rpms.in.yaml / rpms.lock.yaml.
If base image origin is confirmed, update the base image reference.
```

### Version 2.2.2 (tag v0.4.9 -- retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  Same as 2.2.1 (retag -- identical source commits)
  rpms.lock.yaml: openssl-libs-3.0.7-27.el9_4 present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both SBOMs)
  rpms.lock.yaml classification: explicit install (present in lock file)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    -> rpms.lock.yaml says explicit install but SBOM comparison says base image
    -> Investigate manually
  Origin: DISPUTED (rpms.lock.yaml: explicit install / SBOM: base image)

Remediation: investigate discrepancy before proceeding. Same as 2.2.1.
```

## SBOM Verification Summary

For all affected versions (2.2.0 through 2.2.2), the SBOM comparison and rpms.lock.yaml classification **disagree**:

| Version | rpms.lock.yaml | SBOM (final vs base) | Agreement? |
|---------|----------------|----------------------|------------|
| 2.2.0 | present (explicit install) | present in both (base image) | **DISAGREE** |
| 2.2.1 | present (explicit install) | present in both (base image) | **DISAGREE** |
| 2.2.2 | present (explicit install) | present in both (base image) | **DISAGREE** |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

This discrepancy means openssl-libs is listed in rpms.lock.yaml (suggesting explicit installation), but the SBOM comparison shows the package in both the final and base images (suggesting base image inheritance). The package may be both inherited from the base image AND explicitly listed in the lock file (e.g., to pin a specific version). Manual investigation is needed to determine the correct remediation path.

## 2.4 -- Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):
Stream scope: 2.2.x

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0   | 3.0.7-25.el9_3 | YES    |       |
| 2.2.1   | 3.0.7-27.el9_4 | YES    |       |
| 2.2.2   | 3.0.7-27.el9_4 | YES    | retag of 2.2.1 |
| 2.2.3   | 3.0.7-28.el9_4 | NO     | ships fixed version |
| 2.2.4   | 3.0.7-28.el9_4 | NO     | ships fixed version |
```

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Not affected: RHTPA 2.2.3, RHTPA 2.2.4

## Cross-stream note (2.1.x)

Although triage is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`, the security matrix data for the 2.1.x stream shows:

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | YES |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | YES |

The 2.1.x stream is also affected but is tracked by its own stream-specific CVE issue (or would require a separate PSIRT issue). This is noted for Step 8 Case B cross-stream impact analysis.
