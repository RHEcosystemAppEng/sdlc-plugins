# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z` (2.2.x)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fixed version threshold: **3.0.7-28.el9_4**

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** (before 3.0.7-28.el9_4) |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** (before 3.0.7-28.el9_4) |
| 2.2.2 | `v0.4.9` | -- | **YES** (retag of 2.2.1, same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** (matches fixed version) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** (matches fixed version) |

## 2.3.5 -- Dependency Chain Context

### RPM Origin Classification

#### Version 2.2.0 (tag v0.4.5) -- openssl-libs 3.0.7-25.el9_3

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image origin (present in both final and base image SBOMs)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image origin (present in both final and base SBOMs)
    Investigate manually -- the package may be both inherited from the base
    image AND explicitly listed in rpms.lock.yaml (redundant pin), or the SBOM
    comparison may not distinguish reinstalled packages from inherited ones.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  Affected: YES (3.0.7-25.el9_3 is before fixed version 3.0.7-28.el9_4)
```

#### Version 2.2.1 (tag v0.4.8) -- openssl-libs 3.0.7-27.el9_4

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image origin (present in both final and base image SBOMs)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image origin (present in both final and base SBOMs)
    Investigate manually -- the package may be both inherited from the base
    image AND explicitly listed in rpms.lock.yaml (redundant pin), or the SBOM
    comparison may not distinguish reinstalled packages from inherited ones.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  Affected: YES (3.0.7-27.el9_4 is before fixed version 3.0.7-28.el9_4)
```

#### Version 2.2.2 (tag v0.4.9) -- retag of 2.2.1

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 -- same source commits as v0.4.8, carrying forward results.
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification (cosign at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image origin (present in both final and base image SBOMs)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml classification.
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image origin (present in both final and base SBOMs)
    Investigate manually -- the package may be both inherited from the base
    image AND explicitly listed in rpms.lock.yaml (redundant pin), or the SBOM
    comparison may not distinguish reinstalled packages from inherited ones.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  Affected: YES (same as 2.2.1)
```

#### Versions 2.2.3 and 2.2.4 -- NOT AFFECTED

Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) ship openssl-libs 3.0.7-28.el9_4, which matches the fixed version. These versions are not affected and no dependency chain or SBOM analysis is required.

### SBOM Discrepancy Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM verification and rpms.lock.yaml classification disagree:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|---------------|-----------------|------------|
| 2.2.0 | explicit install | base image origin | **DISAGREE** |
| 2.2.1 | explicit install | base image origin | **DISAGREE** |
| 2.2.2 | explicit install (retag of 2.2.1) | base image origin | **DISAGREE** |
| 2.2.3 | (not affected -- skipped) | -- | -- |
| 2.2.4 | (not affected -- skipped) | -- | -- |

**rpms.lock.yaml remains the primary signal** -- the lock file explicitly lists openssl-libs, so the package is classified as an explicit install for remediation purposes. The SBOM result supplements but does not override this classification.

The discrepancy likely indicates that `openssl-libs` is both present in the base image AND explicitly pinned in `rpms.lock.yaml` (a redundant pin that overrides the base image version). The engineer should investigate whether the lock file entry is intentional (version pinning for security or compatibility) or an unnecessary duplicate of the base image package.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

Stream scope: **2.2.x** (from issue suffix `[rhtpa-2.2]`)

| Version | openssl-libs | Affected? | Origin (primary: rpms.lock.yaml) | SBOM Verification | Notes |
|---------|-------------|-----------|----------------------------------|-------------------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | explicit install | base image origin (DISAGREES) | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | explicit install | base image origin (DISAGREES) | |
| 2.2.2 | -- | **YES** | explicit install | base image origin (DISAGREES) | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | **NO** | -- | -- | matches fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | **NO** | -- | -- | matches fixed version |

### Remediation Context

- **Ecosystem**: RPM (system package) -- 1 remediation task for the affected stream
- **Primary classification**: explicit install (rpms.lock.yaml lists openssl-libs)
- **Remediation path**: update the openssl-libs package spec in `rpms.lock.yaml` (or `rpms.in.yaml`) to >= 3.0.7-28.el9_4
- **Already fixed in**: versions 2.2.3+ (openssl-libs 3.0.7-28.el9_4 shipped since build 0.4.11)
- **SBOM discrepancy**: all affected versions show a disagreement between rpms.lock.yaml (explicit install) and SBOM comparison (base image origin). The engineer should verify whether the rpms.lock.yaml entry is an intentional version pin or an unnecessary duplicate of the base image package. This may affect the remediation approach -- if the package is truly base-image-only, a base image update may be sufficient rather than modifying rpms.lock.yaml.
