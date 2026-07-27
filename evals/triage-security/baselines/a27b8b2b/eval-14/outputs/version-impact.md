# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix-mock.md. Matrix Last-Updated timestamp (2026-06-28T10:00:00Z) is within the 14-day threshold -- staleness check passed silently.

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings for RPM: Lock File = `rpms.lock.yaml`, Check Command = `git show <tag>:rpms.lock.yaml`

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Using rpms.lock.yaml data for each pinned commit tag:

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed) |

**Summary:** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## 2.3.5 -- Dependency Chain Context (RPM -- openssl-libs)

### Package Origin Classification

openssl-libs is present in rpms.lock.yaml for the affected versions (2.2.0 through 2.2.2). The lock file presence is the primary classification signal.

- **rpms.lock.yaml classification:** present in lock file --> **explicit install**

### SBOM Verification (cosign available at /usr/bin/cosign)

`cosign` is available (`which cosign` returns `/usr/bin/cosign`). SBOM comparison was performed for the affected versions by downloading the final container image SBOM and the base image SBOM using `cosign download sbom`.

**Procedure applied per affected version:**
1. Downloaded final image SBOM: `cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json`
2. Extracted base image reference from Dockerfile `FROM` line
3. Downloaded base image SBOM: `cosign download sbom <base-image-reference> > /tmp/base-sbom.json`
4. Compared openssl-libs presence in both SBOMs

### Combined Classification Results (rpms.lock.yaml + SBOM side by side)

| Version | rpms.lock.yaml | SBOM (final image) | SBOM (base image) | rpms.lock.yaml Classification | SBOM Classification | Agreement? |
|---------|----------------|---------------------|--------------------|-------------------------------|----------------------|------------|
| 2.2.0 | present | present | present | **explicit install** | **base image** | **DISAGREE** |
| 2.2.1 | present | present | present | **explicit install** | **base image** | **DISAGREE** |
| 2.2.2 | _(retag of 2.2.1)_ | _(same as 2.2.1)_ | _(same as 2.2.1)_ | **explicit install** | **base image** | **DISAGREE** |
| 2.2.3 | present (fixed) | -- | -- | (not affected -- skipped) | (not affected -- skipped) | -- |
| 2.2.4 | present (fixed) | -- | -- | (not affected -- skipped) | (not affected -- skipped) | -- |

### Discrepancy Warning

> **WARNING: SBOM classification disagrees with rpms.lock.yaml for versions 2.2.0, 2.2.1, and 2.2.2.**
>
> rpms.lock.yaml says **explicit install** (openssl-libs is listed in the lock file), but SBOM comparison says **base image** (openssl-libs appears in BOTH the final image SBOM and the base image SBOM, indicating the package is inherited from the base image).
>
> The rpms.lock.yaml classification remains the **primary signal** -- it is not overridden by the SBOM result. However, this disagreement indicates the package may be both explicitly installed AND present in the base image (possibly a layered reinstall over a base image package). Manual investigation is recommended to determine the true remediation path.

### Dependency Chain Summary

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install (primary signal)
  SBOM verification: present in BOTH final and base image SBOMs --> base image
  Classification disagreement: rpms.lock.yaml (explicit install) vs SBOM (base image)
  Origin (primary): explicit install per rpms.lock.yaml
  Note: SBOM cross-validation DISAGREES -- investigate manually

Remediation (based on primary rpms.lock.yaml classification):
  Update openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
  Note: SBOM evidence suggests the package may also be inherited from the base image.
  Verify whether updating the lock file alone is sufficient, or if the base image
  reference also needs updating.
```

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4), scoped to 2.2.x stream:

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | fixed version |
