# Step 2 -- Version Impact Analysis: TC-8005

## Stream Scope

This issue is scoped to the **2.2.x** stream (from the `[rhtpa-2.2]` suffix).

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: rhtpa-release.0.4.z security-matrix.md (Last-Updated: 2026-06-28T10:00:00Z -- 29 days ago, stale)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Package: openssl-libs
Fixed version: 3.0.7-28.el9_4
Lock file: rpms.lock.yaml

### rpms.lock.yaml results

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES (< 3.0.7-28.el9_4) |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES (< 3.0.7-28.el9_4) |
| 2.2.2 | v0.4.9 | -- | YES (retag of 2.2.1, same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO (= fixed version) |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO (= fixed version) |

## 2.3.5 -- Dependency Chain Context

### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  Classification conflict:
    rpms.lock.yaml: explicit install
    SBOM comparison: base image

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: CONFLICTING (rpms.lock.yaml says explicit install; SBOM says base image)
```

### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  Classification conflict:
    rpms.lock.yaml: explicit install
    SBOM comparison: base image

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: CONFLICTING (rpms.lock.yaml says explicit install; SBOM says base image)
```

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs -> base image
  Classification conflict:
    rpms.lock.yaml: explicit install
    SBOM comparison: base image

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: CONFLICTING (rpms.lock.yaml says explicit install; SBOM says base image)
  Note: retag of 2.2.1 -- identical source commits
```

### Versions 2.2.3 and 2.2.4

Not affected -- openssl-libs version 3.0.7-28.el9_4 matches the fixed version. No dependency chain analysis required.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).

### SBOM Verification Summary (inline)

For all affected versions (2.2.0, 2.2.1, 2.2.2), SBOM verification was performed using cosign at /usr/bin/cosign. In all cases:

- **rpms.lock.yaml**: openssl-libs is listed (explicit install classification)
- **SBOM comparison**: openssl-libs appears in BOTH the final image SBOM and the base image SBOM (base image classification)
- **Result**: CLASSIFICATION DISAGREES -- rpms.lock.yaml says explicit install, SBOM comparison says base image. Manual investigation is required to determine the correct origin.

This discrepancy may indicate that the package is both inherited from the base image AND explicitly listed in rpms.lock.yaml (e.g., to pin a specific version). The remediation path depends on the resolution of this conflict:
- If explicit install: update the package spec in rpms.in.yaml / rpms.lock.yaml
- If base image: update the base image tag to a version with patched openssl-libs

## 2.5 -- Upstream Fix Check

The RPM ecosystem in the 2.2.x stream has no Upstream Branch configured (the Upstream Branch column is empty for the RPM row). Therefore, no upstream fix check is applicable for RPM system packages.

The fix is already present in versions 2.2.3+ (openssl-libs 3.0.7-28.el9_4), confirming that the release pipeline has already picked up the fix for newer versions.

## Cross-Stream Impact (for Step 3 / Case A consideration)

This issue is scoped to the 2.2.x stream. The 2.1.x stream also has openssl-libs entries:

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES (< 3.0.7-28.el9_4) |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES (< 3.0.7-28.el9_4) |

The 2.1.x stream is also affected. This would trigger Case A (cross-stream impact) in Step 8: a cross-stream impact comment should be posted, and preemptive remediation tasks should be considered for the 2.1.x stream if no companion CVE Jira exists for that stream.
