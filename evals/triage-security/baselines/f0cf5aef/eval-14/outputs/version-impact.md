# Step 2 -- Version Impact Analysis: TC-8005

CVE-2026-40215 -- openssl-libs buffer over-read in X.509 certificate verification

- Vulnerable library: openssl-libs (RPM)
- Affected range: versions before 3.0.7-28.el9_4
- Fixed version: 3.0.7-28.el9_4
- Stream scope: 2.2.x only (issue suffix `[rhtpa-2.2]`)

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for rhtpa-release.0.4.z

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings (2.2.x stream):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version | vs fix (3.0.7-28.el9_4) | Affected? |
|---------|-----|----------------------|-------------------------|-----------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | below fix | YES |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | below fix | YES |
| 2.2.2 | `v0.4.9` | -- | retag of 2.2.1 (v0.4.8) | YES |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | equals fix | NO |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | equals fix | NO |

## 2.3.5 -- Dependency Chain Context

### SBOM Verification

cosign availability: `/usr/bin/cosign` (available)

SBOM comparison was performed for affected versions (2.2.0 through 2.2.2) by downloading
the final image SBOM and base image SBOM via cosign.

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3) -- AFFECTED

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary signal)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to
openssl-libs >= 3.0.7-28.el9_4.
```

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4) -- AFFECTED

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary signal)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to
openssl-libs >= 3.0.7-28.el9_4.
```

### Version 2.2.2 (tag v0.4.9, retag of v0.4.8) -- AFFECTED

```
Dependency chain for openssl-libs (RPM):
  Same as version 2.2.1 (retag of v0.4.8 -- identical image)
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary signal)

Remediation: same as 2.2.1 -- update the package spec in rpms.in.yaml / rpms.lock.yaml.
```

### Versions 2.2.3 and 2.2.4 -- NOT AFFECTED

These versions ship openssl-libs 3.0.7-28.el9_4, which is at or above the fix
version. No dependency chain analysis required.

### SBOM Disagreement Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM classification and the
rpms.lock.yaml classification disagree:

| Version | rpms.lock.yaml | SBOM comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (in both final and base SBOMs) | DISAGREE |
| 2.2.1 | explicit install (present in lock file) | base image (in both final and base SBOMs) | DISAGREE |
| 2.2.2 | explicit install (same as 2.2.1) | base image (same as 2.2.1) | DISAGREE |

rpms.lock.yaml remains the primary signal. The disagreement suggests that
openssl-libs may be both explicitly installed via rpms.lock.yaml AND present in the
base image. Manual investigation is recommended to confirm the origin and determine
the correct remediation path (lock file update vs. base image update vs. both).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fix version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fix version |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

## 2.5 -- Upstream Fix Check

RPM ecosystem has no Upstream Branch configured in the 2.2.x Ecosystem Mappings
table (Upstream Branch column is empty for RPM). Upstream fix check is not applicable
for RPM system packages -- remediation is handled via rpms.lock.yaml updates in the
Konflux release repo.

## Cross-Stream Impact (Case A preliminary)

This issue is scoped to the **2.2.x** stream. The 2.1.x stream also contains
openssl-libs (versions 3.0.7-24.el9 at v0.3.8 and v0.3.12), which are below the
fix threshold and would also be affected. Cross-stream impact should be reported
per Case A in Step 8.

## Triage Outcome (preliminary)

- **Ecosystem**: RPM (system package)
- **Tasks per stream**: 1 (Konflux release repo fix)
- **Affected versions in scope**: 2.2.0, 2.2.1, 2.2.2
- **Remediation**: update openssl-libs in rpms.lock.yaml to >= 3.0.7-28.el9_4
- **Note**: SBOM verification flagged a classification disagreement for all
  affected versions -- rpms.lock.yaml says explicit install but SBOM says base
  image. Engineer should investigate whether both the lock file and base image
  need updating.
