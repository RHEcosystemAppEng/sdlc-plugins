# Step 2 — Version Impact Analysis: TC-8005

## 2.1 — Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z` (2.2.x)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 — Dependency Version Extraction

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** — below fix threshold 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** — below fix threshold 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | **YES** — same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** — at fix threshold |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** — at fix threshold |

## 2.3.5 — Dependency Chain Context

### RPM origin classification

**Method**: rpms.lock.yaml inspection + SBOM verification (cosign available at `/usr/bin/cosign`)

#### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: present in both final and base image SBOMs -> base image
  !! DISAGREEMENT: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: CONFLICTING — investigate manually

  WARNING: SBOM classification disagrees with rpms.lock.yaml — lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
```

#### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: present in both final and base image SBOMs -> base image
  !! DISAGREEMENT: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: CONFLICTING — investigate manually

  WARNING: SBOM classification disagrees with rpms.lock.yaml — lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
```

#### Version 2.2.2 (tag v0.4.9 — retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 (v0.4.8) — same dependency chain applies.
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: present in both final and base image SBOMs -> base image
  !! DISAGREEMENT: rpms.lock.yaml says explicit install, SBOM comparison says base image
  Origin: CONFLICTING — investigate manually

  WARNING: SBOM classification disagrees with rpms.lock.yaml — lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
```

### Classification summary

| Version | rpms.lock.yaml | SBOM (final) | SBOM (base) | rpms.lock.yaml classification | SBOM classification | Agreement? |
|---------|---------------|--------------|-------------|-------------------------------|---------------------|------------|
| 2.2.0 | present | present | present | explicit install | base image | **NO** — disagrees |
| 2.2.1 | present | present | present | explicit install | base image | **NO** — disagrees |
| 2.2.2 | present (retag of 2.2.1) | present | present | explicit install | base image | **NO** — disagrees |

For all three affected versions, the rpms.lock.yaml lists openssl-libs (indicating explicit install), but the SBOM comparison shows the package in both the final image and the base image (indicating base image origin). This discrepancy requires manual investigation to determine the true origin before selecting the correct remediation template (explicit install vs. base image update).

## 2.4 — Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fix threshold |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fix threshold |

**Stream scope**: 2.2.x only (per issue suffix `[rhtpa-2.2]`)

**Affected versions in scope**: 2.2.0, 2.2.1, 2.2.2

**Versions not affected**: 2.2.3, 2.2.4 (ship the fixed version 3.0.7-28.el9_4)

### Cross-stream note

This triage is scoped to the 2.2.x stream. The 2.1.x stream also ships openssl-libs at older versions (3.0.7-24.el9 for both 2.1.0 and 2.1.1), which are below the fix threshold. Cross-stream impact would be assessed in Case A of Step 8, but only the 2.2.x stream versions are included in this issue's Affects Versions correction.

## 2.5 — Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table (value is `—`). Upstream fix check is not applicable for system package ecosystems — the fix is delivered via base image or lock file updates in the Konflux release repo.

The Red Hat Security Advisory RHSA-2026:4021 indicates the fix is available in the Red Hat package repositories (openssl-libs-3.0.7-28.el9_4).
