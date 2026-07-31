# Step 2 -- Version Impact Analysis

## 2.1 -- Load the supportability matrix

Loaded security-matrix.md for the 2.2.x stream (scoped by issue suffix `[rhtpa-2.2]`).

Stream: **2.2.x** (rhtpa-release.0.4.z)

### Supportability Matrix (2.2.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Ecosystem Mappings (2.2.x stream)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Extract dependency versions

Ecosystem: **RPM** (system package)
Library: **openssl-libs**
Fix threshold: **3.0.7-28.el9_4** (versions before this are affected)

Extracted openssl-libs versions from rpms.lock.yaml at each pinned commit:

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |

## 2.3.5 -- Dependency chain context

### Package classification

**rpms.lock.yaml classification (primary signal):**

openssl-libs is **present** in rpms.lock.yaml for the affected versions (2.2.0 through 2.2.2). Per the classification rules, presence in the lock file means **explicit install** -- the package is explicitly specified in the Konflux release repo's package list.

**SBOM verification (cosign available at `/usr/bin/cosign`):**

Since `which cosign` returns `/usr/bin/cosign`, SBOM comparison was performed for the affected versions.

For each affected version (2.2.0, 2.2.1, 2.2.2):

1. Downloaded the final container image SBOM:
   ```bash
   cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json
   ```

2. Extracted the base image reference from the Dockerfile's `FROM` line.

3. Downloaded the base image SBOM:
   ```bash
   cosign download sbom <base-image-reference> > /tmp/base-sbom.json
   ```

4. Compared openssl-libs presence in both SBOMs:
   - openssl-libs appears in the **final image SBOM**: YES
   - openssl-libs appears in the **base image SBOM**: YES
   - SBOM classification: **base image** (present in both SBOMs -- the package is inherited from the base image)

### Dependency chain output (rpms.lock.yaml and SBOM results side by side)

```
Dependency chain for openssl-libs (RPM):

Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification: DISAGREEMENT

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification: DISAGREEMENT

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

Version 2.2.2 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4) -- retag of 2.2.1:
  rpms.lock.yaml: PRESENT --> explicit install (same as 2.2.1)
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification: DISAGREEMENT

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

Primary classification: rpms.lock.yaml (explicit install) remains the primary signal.
The SBOM result supplements but does not override the lock file classification.
The engineer should investigate the discrepancy to determine the true package origin:
the package may be present in both rpms.lock.yaml as an explicit install AND inherited
from the base image, resulting in a version override at build time.
```

### Summary

The rpms.lock.yaml classification identifies openssl-libs as an **explicit install** for all affected versions (2.2.0 through 2.2.2). However, SBOM verification using `cosign download sbom` shows openssl-libs is present in **both** the final image SBOM and the base image SBOM, which indicates **base image** origin. This disagreement is flagged for manual investigation.

The rpms.lock.yaml classification remains the **primary signal** per the skill's classification rules. The SBOM comparison is a supplementary cross-check that does not override the lock file result. The discrepancy may indicate that the package is explicitly pinned in rpms.lock.yaml at a version that differs from (or matches) the base image's version, or that the lock file includes a rebuild of a base image package.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | **NO** | |
| 2.2.4 | 3.0.7-28.el9_4 | **NO** | |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

Dependency chain context (inline):
- rpms.lock.yaml: openssl-libs is an explicit install (present in rpms.lock.yaml)
- SBOM verification (cosign): openssl-libs appears in both final and base image SBOMs (base image classification)
- Discrepancy: rpms.lock.yaml says explicit install; SBOM says base image. Flagged for manual investigation.
- Primary signal: rpms.lock.yaml (explicit install). SBOM supplements but does not override.
