# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | |
| 2.2.4 | 3.0.7-28.el9_4 | NO | |

All versions from the 2.2.x stream supportability matrix are included. Pinned commit tags from the matrix are used for each version (v0.4.5, v0.4.8, v0.4.9, v0.4.11, v0.4.12). Version 2.2.2 is a retag of 2.2.1, so the result is carried forward.

Data source: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each pinned tag.

## Dependency Chain Context (Step 2.3.5)

### Package origin classification

**rpms.lock.yaml classification**: openssl-libs IS present in rpms.lock.yaml for all 2.2.x versions → **explicit install**

The lock file presence is the primary classification signal per Step 2.3.5.

### SBOM verification (cosign available)

`which cosign` returns `/usr/bin/cosign` — cosign is available for SBOM comparison.

For the affected versions (2.2.0, 2.2.1, 2.2.2):

1. Downloaded final image SBOM via `cosign download sbom <image-reference>@<image-digest>`
2. Extracted base image reference from Dockerfile `FROM` line
3. Downloaded base image SBOM via `cosign download sbom <base-image-reference>`
4. Compared package presence:

| Version | rpms.lock.yaml | Final Image SBOM | Base Image SBOM | SBOM Classification |
|---------|---------------|-----------------|----------------|---------------------|
| 2.2.0 | present (explicit install) | present | present | base image |
| 2.2.1 | present (explicit install) | present | present | base image |
| 2.2.2 | — (retag of 2.2.1) | present | present | base image |

**Result**: openssl-libs appears in BOTH the final image SBOM and the base image SBOM, indicating the package originates from the base image. However, rpms.lock.yaml lists the package as an explicit install.

### Classification disagreement

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** — lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

The rpms.lock.yaml classification (explicit install) remains the **primary signal** — the SBOM result supplements but does not override it. The discrepancy is flagged for engineer investigation. Possible explanations:

- The package may be inherited from the base image AND re-declared in rpms.lock.yaml (explicit pin of a base image package)
- The rpms.lock.yaml may include base image packages for reproducibility tracking

**Recommendation**: The engineer should investigate whether openssl-libs in rpms.lock.yaml is an explicit install or a lock of a base-image-inherited package. This affects the remediation path:
- If truly explicit install → update the package spec in rpms.in.yaml / rpms.lock.yaml
- If base image package pinned in lock file → update the base image to a version with the patched openssl-libs

### Summary

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present → explicit install (primary signal)
  SBOM verification: present in both final and base image SBOMs → base image
  WARNING: Classification disagreement — rpms.lock.yaml says explicit install,
           SBOM comparison says base image. Investigate manually.
  Origin: UNRESOLVED — engineer must determine whether this is a base image
          package pinned in the lock file or a true explicit install
```
