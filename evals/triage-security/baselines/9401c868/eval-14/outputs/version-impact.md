# Step 2 -- Version Impact Analysis: TC-8005

CVE-2026-40215 -- openssl-libs buffer over-read in X.509 certificate verification

- **Vulnerable library**: openssl-libs
- **Affected range**: versions before 3.0.7-28.el9_4
- **Fixed version**: 3.0.7-28.el9_4
- **Ecosystem**: RPM (system package)
- **Stream scope**: 2.2.x only (from issue suffix [rhtpa-2.2])

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: rhtpa-release.0.4.z security-matrix.md

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Matrix Last-Updated: 2026-06-28T10:00:00Z (102 days ago -- stale, exceeds 14-day threshold)

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Investigation method: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | **YES** | retag of 2.2.1 (same as v0.4.8: 3.0.7-27.el9_4) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are not affected.

## 2.3.5 -- Dependency Chain Context

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  rpms.lock.yaml classification: explicit install (primary signal)
  SBOM classification: base image (supplementary signal)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
  rpms.lock.yaml says explicit install, but SBOM comparison says base image.
  The rpms.lock.yaml classification remains authoritative. The SBOM result
  supplements but does not override the lock file evidence. Investigate
  manually -- the package may be both explicitly pinned in the lock file
  AND inherited from the base image, or the lock file entry may be redundant.

  Origin: explicit install (per rpms.lock.yaml, primary signal)
  SBOM note: base image also ships openssl-libs -- discrepancy noted for review
```

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  rpms.lock.yaml classification: explicit install (primary signal)
  SBOM classification: base image (supplementary signal)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
  rpms.lock.yaml says explicit install, but SBOM comparison says base image.
  The rpms.lock.yaml classification remains authoritative. The SBOM result
  supplements but does not override the lock file evidence. Investigate
  manually -- the package may be both explicitly pinned in the lock file
  AND inherited from the base image, or the lock file entry may be redundant.

  Origin: explicit install (per rpms.lock.yaml, primary signal)
  SBOM note: base image also ships openssl-libs -- discrepancy noted for review
```

### Version 2.2.2 (tag v0.4.9, retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 (v0.4.8) -- same dependency chain as 2.2.1
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  rpms.lock.yaml classification: explicit install (primary signal)
  SBOM classification: base image (supplementary signal)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
  rpms.lock.yaml says explicit install, but SBOM comparison says base image.
  The rpms.lock.yaml classification remains authoritative. The SBOM result
  supplements but does not override the lock file evidence. Investigate
  manually -- the package may be both explicitly pinned in the lock file
  AND inherited from the base image, or the lock file entry may be redundant.

  Origin: explicit install (per rpms.lock.yaml, primary signal)
  SBOM note: base image also ships openssl-libs -- discrepancy noted for review
```

### SBOM Disagreement Summary

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml lists openssl-libs (indicating explicit install), but SBOM comparison shows the package present in both the final image and the base image (indicating base image origin). The rpms.lock.yaml classification is retained as the primary signal per the skill protocol -- SBOM verification supplements but does not override the lock file classification.

The disagreement suggests the package may be both explicitly pinned in the lock file and inherited from the base image. Remediation should follow the explicit install path (updating the package spec in rpms.in.yaml / rpms.lock.yaml), since the lock file explicitly declares the package. The engineer should verify whether the lock file entry is intentional or redundant.

## 2.4 -- Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):
Stream scope: 2.2.x only

| Version | openssl-libs      | Affected? | Notes                                                   |
|---------|-------------------|-----------|----------------------------------------------------------|
| 2.2.0   | 3.0.7-25.el9_3    | YES       | rpms.lock.yaml: explicit install; SBOM: base image       |
| 2.2.1   | 3.0.7-27.el9_4    | YES       | rpms.lock.yaml: explicit install; SBOM: base image       |
| 2.2.2   | --                | YES       | retag of 2.2.1; same SBOM disagreement                  |
| 2.2.3   | 3.0.7-28.el9_4    | NO        | = fixed version                                         |
| 2.2.4   | 3.0.7-28.el9_4    | NO        | = fixed version                                         |
```

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

## 2.5 -- Cross-Stream Impact Check

Since the issue is scoped to the 2.2.x stream (suffix [rhtpa-2.2]), the 2.1.x stream is outside scope. However, for Case A (cross-stream impact) awareness:

| Stream | openssl-libs versions in stream | Any affected? |
|--------|---------------------------------|---------------|
| 2.1.x | 3.0.7-24.el9 (all versions) | YES (< 3.0.7-28.el9_4) |
| 2.2.x | 3.0.7-25.el9_3 to 3.0.7-28.el9_4 | YES (2.2.0-2.2.2) |

The 2.1.x stream is also affected (all versions ship openssl-libs older than the fix threshold). This would trigger Case A cross-stream impact notification. The 2.1.x stream ships openssl-libs 3.0.7-24.el9 across all its versions (v0.3.8 and v0.3.12), which is below the fix threshold of 3.0.7-28.el9_4.
