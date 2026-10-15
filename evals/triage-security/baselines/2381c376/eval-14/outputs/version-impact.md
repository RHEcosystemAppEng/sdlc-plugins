# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from Stream 2: rhtpa-release.0.4.z (2.2.x stream).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Source |
|---------|-----|---------------------------------------|--------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | `git show v0.4.5:rpms.lock.yaml` |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | `git show v0.4.8:rpms.lock.yaml` |
| 2.2.2 | `v0.4.9` | -- | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | `git show v0.4.11:rpms.lock.yaml` |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | `git show v0.4.12:rpms.lock.yaml` |

Fix threshold: **3.0.7-28.el9_4** (from Jira description; external CVE enrichment not performed in this eval).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

## 2.3.5 -- Dependency Chain Context (with SBOM Verification)

### Package origin classification

**cosign availability**: `/usr/bin/cosign` -- available.

For each affected version, the RPM package origin was classified using both `rpms.lock.yaml` and SBOM comparison:

#### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  !! SBOM classification DISAGREES with rpms.lock.yaml:
     rpms.lock.yaml says: explicit install (openssl-libs listed in lock file)
     SBOM comparison says: base image (present in both final and base image SBOMs)
  Origin: DISPUTED -- rpms.lock.yaml indicates explicit install, but SBOM
          comparison indicates base image inheritance. Investigate manually.
```

#### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  !! SBOM classification DISAGREES with rpms.lock.yaml:
     rpms.lock.yaml says: explicit install (openssl-libs listed in lock file)
     SBOM comparison says: base image (present in both final and base image SBOMs)
  Origin: DISPUTED -- rpms.lock.yaml indicates explicit install, but SBOM
          comparison indicates base image inheritance. Investigate manually.
```

#### Version 2.2.2 (retag of 2.2.1 -- tag v0.4.9)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: same as 2.2.1 (retag of v0.4.8)
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  !! SBOM classification DISAGREES with rpms.lock.yaml:
     rpms.lock.yaml says: explicit install (openssl-libs listed in lock file)
     SBOM comparison says: base image (present in both final and base image SBOMs)
  Origin: DISPUTED -- same classification conflict as 2.2.1 (retag).
          Investigate manually.
```

### Discrepancy summary

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml and SBOM comparison results disagree:

| Version | rpms.lock.yaml | SBOM (final image) | SBOM (base image) | rpms.lock.yaml classification | SBOM classification | Agreement? |
|---------|---------------|--------------------|--------------------|------------------------------|---------------------|------------|
| 2.2.0 | present | present | present | explicit install | base image | NO |
| 2.2.1 | present | present | present | explicit install | base image | NO |
| 2.2.2 | (retag of 2.2.1) | present | present | explicit install | base image | NO |

> WARNING: SBOM classification disagrees with rpms.lock.yaml for all affected versions.
> rpms.lock.yaml lists openssl-libs (indicating explicit install), but SBOM comparison
> shows the package in both the final image and base image SBOMs (indicating base image origin).
> This may indicate that openssl-libs is explicitly pinned in rpms.lock.yaml but is ALSO
> provided by the base image. Manual investigation is required to determine the correct
> remediation path before proceeding.

### Impact on remediation path

The disagreement affects the remediation approach:

- **If explicit install** (rpms.lock.yaml classification): Remediation is to update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
- **If base image** (SBOM classification): Remediation is to update the base image to a version that includes patched openssl-libs.

Because the classifications disagree, the engineer must investigate the actual package provenance before selecting the remediation approach. Both signals should be presented in any remediation task created.

## Proposed Jira Actions (not executed)

Based on the version impact analysis, the following Jira mutations would be proposed:

1. **Affects Versions Correction (Step 3)**: Current `RHTPA 2.0.0` is incorrect. Proposed correction to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (scoped to the 2.2.x stream per issue suffix `[rhtpa-2.2]`). Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version.

2. **Case B -- Remediation (Step 8)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the scoped stream. Since this is an RPM/system package ecosystem, **1 remediation task** would be created for the 2.2.x stream. However, the rpms.lock.yaml vs SBOM discrepancy must be resolved first to determine the correct remediation template (explicit install vs base image origin).

3. **Cross-stream impact (Case A)**: The issue is scoped to 2.2.x. The 2.1.x stream also contains affected openssl-libs versions (3.0.7-24.el9 at v0.3.8 and v0.3.12, both before 3.0.7-28.el9_4). A cross-stream impact comment would be posted, and preemptive remediation tasks would be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.
