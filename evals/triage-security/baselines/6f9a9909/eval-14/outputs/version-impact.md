# Step 2 -- Version Impact Analysis: CVE-2026-40215

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Matrix last updated: 2026-06-28 (8 days ago -- within 14-day freshness threshold).

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: **3.0.7-28.el9_4** (from Jira description)

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version and are NOT affected.

## 2.3.5 -- Dependency Chain Context

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  rpms.lock.yaml classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- rpms.lock.yaml lists openssl-libs (explicit install)
          but SBOM comparison shows it in both final and base image (base image origin).

Remediation: investigate the discrepancy. If openssl-libs is truly an explicit
install (per rpms.lock.yaml), update the package spec in rpms.in.yaml / rpms.lock.yaml.
If it is a base image package redundantly listed in rpms.lock.yaml, consider updating
the base image instead.
```

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  rpms.lock.yaml classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- rpms.lock.yaml lists openssl-libs (explicit install)
          but SBOM comparison shows it in both final and base image (base image origin).

Remediation: investigate the discrepancy. If openssl-libs is truly an explicit
install (per rpms.lock.yaml), update the package spec in rpms.in.yaml / rpms.lock.yaml.
If it is a base image package redundantly listed in rpms.lock.yaml, consider updating
the base image instead.
```

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 -- same as version 2.2.1 above.
  rpms.lock.yaml: present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  rpms.lock.yaml classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- same discrepancy as 2.2.1 (retag).
```

### SBOM Verification Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM verification using cosign
(`/usr/bin/cosign`) shows a disagreement between the two classification signals:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both final and base SBOMs) | **DISAGREE** |
| 2.2.1 | explicit install (present in lock file) | base image (present in both final and base SBOMs) | **DISAGREE** |
| 2.2.2 | explicit install (retag of 2.2.1) | base image (retag of 2.2.1) | **DISAGREE** |

This discrepancy suggests that openssl-libs may be both inherited from the base image
AND explicitly listed in rpms.lock.yaml (redundant explicit install). The engineer
should investigate whether the rpms.lock.yaml entry is intentional (to pin a specific
version) or accidental (a leftover from a previous configuration).

## 2.4 -- Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0   | 3.0.7-25.el9_3 | YES    |       |
| 2.2.1   | 3.0.7-27.el9_4 | YES    |       |
| 2.2.2   | --             | YES    | retag of 2.2.1 |
| 2.2.3   | 3.0.7-28.el9_4 | NO     | fixed version |
| 2.2.4   | 3.0.7-28.el9_4 | NO     | fixed version |
```

## Cross-Stream Impact (for Case A evaluation)

Since this issue is scoped to 2.2.x, the 2.1.x stream was also checked for impact:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |

The 2.1.x stream is also affected. This triggers **Case A** (cross-stream impact).
A cross-stream impact comment should be posted, and preemptive remediation tasks
should be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.

## Triage Outcome

- **Affected versions (in-scope, 2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (in-scope, 2.2.x)**: 2.2.3, 2.2.4
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 also affected
- **Ecosystem**: RPM (system package) -- 1 remediation task per stream
- **SBOM discrepancy**: rpms.lock.yaml and SBOM classification disagree for all affected versions; manual investigation required
- **Remediation path**: Case B (create remediation task for 2.2.x) + Case A (cross-stream notice for 2.1.x)
