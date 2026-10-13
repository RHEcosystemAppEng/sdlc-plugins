# Step 2 -- Version Impact Analysis: TC-8005

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. Two streams configured:

- **2.1.x** stream (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **2.2.x** stream (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

Issue is scoped to **2.2.x** stream per `[rhtpa-2.2]` suffix, but all supported versions are checked per triage rules.

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Package: openssl-libs.
Fixed version: 3.0.7-28.el9_4.

### RPM lock file results (all streams)

| Version | Stream | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|--------|-----|---------------------------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 2.1.x | `v0.3.12` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.2.0 | 2.2.x | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 2.2.x | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 2.2.x | `v0.4.8` | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 3.0.7-28.el9_4 | NO | at fixed version |

## 2.3.5 -- Dependency Chain Context

### RPM Origin Classification and SBOM Verification

cosign availability: `/usr/bin/cosign` (available)

#### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install; SBOM says base image

Remediation: investigate the disagreement between rpms.lock.yaml and SBOM
classification before determining remediation path. If explicit install,
update the package spec in rpms.in.yaml / rpms.lock.yaml. If base image,
update the base image reference to a version with patched openssl-libs.
```

#### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install; SBOM says base image

Remediation: investigate the disagreement between rpms.lock.yaml and SBOM
classification before determining remediation path. If explicit install,
update the package spec in rpms.in.yaml / rpms.lock.yaml. If base image,
update the base image reference to a version with patched openssl-libs.
```

#### Version 2.2.2 (tag v0.4.8, retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml says explicit install; SBOM says base image
  Note: retag of 2.2.1 -- same source commits and SBOM results

Remediation: same as 2.2.1 (retag -- identical source and build artifacts).
```

#### Versions 2.2.3 and 2.2.4 (NOT affected)

Not affected -- openssl-libs is at the fixed version 3.0.7-28.el9_4. No dependency chain analysis needed.

#### Versions 2.1.0 and 2.1.1 (2.1.x stream -- outside scoped stream)

Affected versions in the 2.1.x stream (openssl-libs 3.0.7-24.el9 < 3.0.7-28.el9_4). These versions are outside the issue's scoped stream (2.2.x) and would be tracked by a companion CVE Jira for the 2.1.x stream or via preemptive remediation (Step 8, Case A).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Stream | openssl-libs | Affected? | Notes |
|---------|--------|--------------|-----------|-------|
| 2.1.0 | 2.1.x | 3.0.7-24.el9 | YES | outside scoped stream |
| 2.1.1 | 2.1.x | 3.0.7-24.el9 | YES | outside scoped stream |
| 2.2.0 | 2.2.x | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 2.2.x | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 2.2.x | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 2.2.x | 3.0.7-28.el9_4 | NO | at fixed version |

### SBOM Verification Summary (scoped stream 2.2.x, affected versions only)

| Version | rpms.lock.yaml | SBOM (final vs base) | Classification | Agreement? |
|---------|----------------|----------------------|----------------|------------|
| 2.2.0 | present -> explicit install | present in both -> base image | CONFLICTING | NO |
| 2.2.1 | present -> explicit install | present in both -> base image | CONFLICTING | NO |
| 2.2.2 | present -> explicit install (retag of 2.2.1) | present in both -> base image | CONFLICTING | NO |

All three affected versions in the scoped stream show a **disagreement** between rpms.lock.yaml classification (explicit install) and SBOM comparison classification (base image). The rpms.lock.yaml lists openssl-libs explicitly, but the SBOM shows the package is present in both the final container image and the base image, indicating it originates from the base image.

This discrepancy requires manual investigation to determine the correct remediation path:
- If the package is truly an explicit install (rpms.lock.yaml is authoritative), remediation is: update the package spec in rpms.in.yaml / rpms.lock.yaml.
- If the package is truly a base image dependency (SBOM is authoritative), remediation is: update the base image tag/digest to a version with patched openssl-libs.

## 2.5 -- Upstream Fix Check

RPM ecosystem has no upstream branch configured (Upstream Branch column is "--" in Ecosystem Mappings). The upstream fix status is determined by the base image vendor's errata pipeline. The Red Hat Security Advisory RHSA-2026:4021 indicates a fix is available from the base image vendor.

## Cross-Stream Impact Summary

The issue is scoped to 2.2.x, but 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9, which is below the fix threshold). This cross-stream impact would be reported via Step 8 Case A (cross-stream impact comment) and preemptive remediation tasks for 2.1.x if no sibling CVE Jira exists for that stream.
