# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix-mock.md` -- Stream 2: rhtpa-release.0.4.z (2.2.x stream)

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

## 2.3 -- Dependency Version Extraction (openssl-libs via rpms.lock.yaml)

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | before fix 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | before fix 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | ships fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | ships fixed version |

Fix threshold: 3.0.7-28.el9_4 (from Jira description; external CVE enrichment not performed in mock mode).

## 2.3.5 -- Dependency Chain Context (RPM)

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification disagreement: rpms.lock.yaml says explicit install, SBOM says base image

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml for this version.
  rpms.lock.yaml: openssl-libs listed --> explicit install
  SBOM comparison: openssl-libs in both final and base image SBOMs --> base image origin
  Investigate manually -- the package may be both explicitly pinned in rpms.lock.yaml
  AND inherited from the base image. The rpms.lock.yaml entry may be a version pin
  for a package that originates from the base image.
```

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification disagreement: rpms.lock.yaml says explicit install, SBOM says base image

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml for this version.
  rpms.lock.yaml: openssl-libs listed --> explicit install
  SBOM comparison: openssl-libs in both final and base image SBOMs --> base image origin
  Investigate manually -- the package may be both explicitly pinned in rpms.lock.yaml
  AND inherited from the base image.
```

### Version 2.2.2 (tag v0.4.9, retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 -- same dependency chain as 2.2.1
  rpms.lock.yaml: present --> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM --> base image
  Classification disagreement: rpms.lock.yaml says explicit install, SBOM says base image

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml for this version.
  rpms.lock.yaml: openssl-libs listed --> explicit install
  SBOM comparison: openssl-libs in both final and base image SBOMs --> base image origin
  Investigate manually -- same as 2.2.1.
```

### Versions 2.2.3 and 2.2.4

Not affected (ship fixed version 3.0.7-28.el9_4). No dependency chain analysis required.

### SBOM Verification Summary

cosign is available at `/usr/bin/cosign`. SBOM verification was performed for all affected versions (2.2.0 through 2.2.2).

For all three affected versions, the SBOM classification **disagrees** with the rpms.lock.yaml classification:

| Version | rpms.lock.yaml | SBOM (final vs base) | Agreement? |
|---------|---------------|----------------------|------------|
| 2.2.0 | present (explicit install) | in both final and base SBOM (base image) | **DISAGREE** |
| 2.2.1 | present (explicit install) | in both final and base SBOM (base image) | **DISAGREE** |
| 2.2.2 | present (explicit install) | in both final and base SBOM (base image) | **DISAGREE** |

This discrepancy suggests that openssl-libs is a base image package that is also explicitly pinned in `rpms.lock.yaml` (possibly for version control). Manual investigation is recommended to determine the true origin and appropriate remediation path:
- If the rpms.lock.yaml pin is intentional (version override of a base image package), remediation is to update the pin in rpms.lock.yaml / rpms.in.yaml.
- If the rpms.lock.yaml entry is vestigial, remediation may be a base image update instead.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

Affected versions: 2.2.0, 2.2.1, 2.2.2
Not affected versions: 2.2.3, 2.2.4

## 2.5 -- Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table. Upstream fix check is not applicable for system packages -- the fix is delivered through base image updates or rpms.lock.yaml version pin updates.

The fixed version 3.0.7-28.el9_4 is already available (per RHSA-2026:4021). Versions 2.2.3 and 2.2.4 already ship this fix.

## Triage Outcome

**Case B: Affected** -- versions 2.2.0, 2.2.1, and 2.2.2 within the 2.2.x stream are affected.

Ecosystem classification: RPM (system package) -- 1 remediation task for the 2.2.x stream.

The remediation path depends on the resolution of the rpms.lock.yaml vs SBOM classification disagreement:
- If rpms.lock.yaml pin is authoritative: update the openssl-libs version in rpms.lock.yaml / rpms.in.yaml to >= 3.0.7-28.el9_4.
- If base image origin is authoritative: update the base image to a version that ships openssl-libs >= 3.0.7-28.el9_4.

Given that the rpms.lock.yaml explicitly lists the package, the recommended remediation is to update the package pin in the Konflux release repo to the fixed version.
