# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fixed version threshold: **3.0.7-28.el9_4**

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | at fixed version |

## 2.3.5 -- Dependency Chain Context

### Dependency chain for openssl-libs (RPM):

**Version 2.2.0 (tag v0.4.5):**

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM: openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    -> Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml lists openssl-libs (explicit install)
    but SBOM shows it in both final and base images (base image origin)
```

**Version 2.2.1 (tag v0.4.8):**

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM: openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    -> Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml lists openssl-libs (explicit install)
    but SBOM shows it in both final and base images (base image origin)
```

**Version 2.2.2 (tag v0.4.9):**

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 (same source as v0.4.8) -- same results as 2.2.1
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM: openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    -> Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml lists openssl-libs (explicit install)
    but SBOM shows it in both final and base images (base image origin)
```

### SBOM Disagreement Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals disagree:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|---------------|-----------------|------------|
| 2.2.0 | explicit install (listed in lock file) | base image (in both final + base SBOMs) | NO |
| 2.2.1 | explicit install (listed in lock file) | base image (in both final + base SBOMs) | NO |
| 2.2.2 | explicit install (listed in lock file) | base image (in both final + base SBOMs) | NO |

This disagreement likely indicates that openssl-libs is both present in the base image AND explicitly pinned/reinstalled via rpms.lock.yaml (possibly to override the base image version). Manual investigation is required to determine the correct remediation path:
- If the explicit install in rpms.lock.yaml is the controlling source, remediation is to update the package spec in rpms.in.yaml/rpms.lock.yaml.
- If the base image version takes precedence, remediation is to update the base image reference.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fixed version |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### Cross-stream note

This issue is scoped to the 2.2.x stream. The 2.1.x stream (rhtpa-release.0.3.z) also contains openssl-libs:
- v0.3.8: 3.0.7-24.el9 (AFFECTED)
- v0.3.12: 3.0.7-24.el9 (AFFECTED)

Cross-stream impact exists but is tracked separately per Case A protocol.
