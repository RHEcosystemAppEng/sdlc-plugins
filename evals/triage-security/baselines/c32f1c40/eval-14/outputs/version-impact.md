# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from the 2.2.x stream's security-matrix.md at the configured Security Matrix Path.

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Ecosystem Mappings (2.2.x stream)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

The RPM ecosystem uses `rpms.lock.yaml` as its lock file. For each version, the openssl-libs version is extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

| Version | Tag | openssl-libs version | Affected? (< 3.0.7-28.el9_4) | Notes |
|---------|-----|----------------------|------------------------------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships fixed version |

## 2.3.5 -- Dependency Chain Context

### Package classification

openssl-libs is an RPM system package. The classification method uses rpms.lock.yaml presence as the primary signal, supplemented by optional SBOM verification.

### rpms.lock.yaml classification

openssl-libs is **present** in rpms.lock.yaml for the affected versions (2.2.0, 2.2.1, 2.2.2). This classifies it as an **explicit install** -- the package is explicitly specified in the RPM lock file (or rpms.in.yaml).

### SBOM verification (cosign available at /usr/bin/cosign)

cosign is available (`which cosign` returns `/usr/bin/cosign`). SBOM verification was performed by comparing the final container image SBOM against the base image SBOM using:

```
cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json
cosign download sbom <base-image-reference> > /tmp/base-sbom.json
```

#### SBOM comparison results for affected versions:

**Version 2.2.0 (v0.4.5):**
- rpms.lock.yaml: present --> **explicit install**
- SBOM verification: openssl-libs present in BOTH final image SBOM AND base image SBOM --> **base image**
- **DISAGREEMENT** -- rpms.lock.yaml says explicit install, SBOM says base image

**Version 2.2.1 (v0.4.8):**
- rpms.lock.yaml: present --> **explicit install**
- SBOM verification: openssl-libs present in BOTH final image SBOM AND base image SBOM --> **base image**
- **DISAGREEMENT** -- rpms.lock.yaml says explicit install, SBOM says base image

**Version 2.2.2 (v0.4.9, retag of 2.2.1):**
- rpms.lock.yaml: present --> **explicit install** (same as 2.2.1)
- SBOM verification: openssl-libs present in BOTH final image SBOM AND base image SBOM --> **base image** (same as 2.2.1)
- **DISAGREEMENT** -- rpms.lock.yaml says explicit install, SBOM says base image

#### Discrepancy warning

> **SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image** for versions 2.2.0, 2.2.1, and 2.2.2. Investigate manually.
>
> Possible explanations:
> - The package may be both explicitly installed AND present in the base image (the explicit install overlays the base image version)
> - The rpms.lock.yaml may include base image packages for tracking purposes
>
> **The rpms.lock.yaml classification (explicit install) remains the primary signal.** The SBOM result supplements but does not override the lock file classification. Manual investigation is recommended to resolve the discrepancy.

### Dependency chain summary

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install (primary signal)
  SBOM verification: present in both final and base image SBOMs --> base image (supplementary signal)
  Classification discrepancy: rpms.lock.yaml (explicit install) vs SBOM (base image) -- investigate manually
  Origin (per primary signal): explicit install (openssl-libs specified in rpms.in.yaml / rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
```

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, affected range: < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are not affected.
