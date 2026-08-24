# Step 2 -- Version Impact Analysis

## CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4)

### 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream **2.2.x** (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### 2.3 -- Dependency Version Extraction

Source: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version | vs. fix threshold (3.0.7-28.el9_4) | Affected? |
|---------|-----|----------------------|------------------------------------|-----------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | below | YES |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | below | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | below | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | equals fixed version | NO |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | equals fixed version | NO |

### 2.4 -- Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fixed version |
```

Affected versions: 2.2.0, 2.2.1, 2.2.2
Not affected versions: 2.2.3, 2.2.4

### 2.3.5 -- Dependency Chain (RPM, with SBOM Verification)

For each affected version (2.2.0, 2.2.1, 2.2.2), the dependency chain was traced
to classify the package origin. cosign is available at /usr/bin/cosign and was used
for SBOM cross-verification.

#### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install, SBOM says base image

Remediation: investigate discrepancy before determining fix path.
  - If explicit install (per rpms.lock.yaml): update package spec in rpms.in.yaml / rpms.lock.yaml
  - If base image (per SBOM): update base image tag to a version with patched openssl-libs
```

#### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install, SBOM says base image

Remediation: investigate discrepancy before determining fix path.
  - If explicit install (per rpms.lock.yaml): update package spec in rpms.in.yaml / rpms.lock.yaml
  - If base image (per SBOM): update base image tag to a version with patched openssl-libs
```

#### Version 2.2.2 (retag of v0.4.8 / 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  Same as 2.2.1 (retag -- identical source commits)
  rpms.lock.yaml: present -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install, SBOM says base image
```

### SBOM Classification Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml and SBOM
classifications disagree:

| Version | rpms.lock.yaml | SBOM (final vs base) | Agreement? |
|---------|----------------|----------------------|------------|
| 2.2.0 | present (explicit install) | in both (base image) | DISAGREE |
| 2.2.1 | present (explicit install) | in both (base image) | DISAGREE |
| 2.2.2 | (retag of 2.2.1) | (retag of 2.2.1) | DISAGREE |

This discrepancy indicates that openssl-libs may be both explicitly installed in
rpms.lock.yaml AND inherited from the base image. The package could be listed in
rpms.lock.yaml to pin a specific version of a package that is also present in
the base image. Manual investigation is required to determine the correct
remediation path.

### Cross-Stream Impact (for Case A consideration)

The 2.1.x stream is also affected (openssl-libs versions 3.0.7-24.el9 at both
v0.3.8 and v0.3.12 are below the fix threshold). This is outside the current
issue's scope ([rhtpa-2.2]) and would be flagged in Step 8 Case A for
cross-stream impact handling.

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |
