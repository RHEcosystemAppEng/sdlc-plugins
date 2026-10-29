# Step 2 -- Version Impact Analysis

## Issue: TC-8005 -- CVE-2026-40215 (openssl-libs)

**Stream scope**: 2.2.x (from issue suffix [rhtpa-2.2])
**Fix threshold**: 3.0.7-28.el9_4 (from Jira description)
**Ecosystem**: RPM (system package)
**Lock file**: rpms.lock.yaml

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from: rhtpa-release.0.4.z security-matrix.md

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

Source: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version | vs. fix threshold (3.0.7-28.el9_4) |
|---------|-----|----------------------|------------------------------------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | BELOW fix threshold -- AFFECTED |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | BELOW fix threshold -- AFFECTED |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | same as 2.2.1 -- AFFECTED |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | EQUALS fix threshold -- NOT AFFECTED |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | EQUALS fix threshold -- NOT AFFECTED |

## 2.3.5 -- Dependency Chain Context

### RPM Origin Classification

**Package**: openssl-libs
**Ecosystem**: RPM (system package)
**Classification method**: rpms.lock.yaml presence + SBOM cross-verification

#### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs --> base image
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (package present in both final and base image SBOMs)
    --> Investigate manually. The package may be both inherited from the base image
        AND explicitly listed in rpms.lock.yaml (redundant explicit install).
  Origin: CONFLICTING -- requires manual investigation
```

#### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs --> base image
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (package present in both final and base image SBOMs)
    --> Investigate manually. The package may be both inherited from the base image
        AND explicitly listed in rpms.lock.yaml (redundant explicit install).
  Origin: CONFLICTING -- requires manual investigation
```

#### Version 2.2.2 (retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 -- same classification as 2.2.1
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification: same as 2.2.1 -- DISAGREES with rpms.lock.yaml
  Origin: CONFLICTING -- requires manual investigation (same as 2.2.1)
```

#### Versions 2.2.3 and 2.2.4 (NOT AFFECTED)

These versions ship openssl-libs 3.0.7-28.el9_4 which equals the fix threshold.
Dependency chain tracing is not required for unaffected versions.

### SBOM Disagreement Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM verification produced a
classification that disagrees with the rpms.lock.yaml classification:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install (present) | base image (in both SBOMs) | DISAGREE |
| 2.2.1 | explicit install (present) | base image (in both SBOMs) | DISAGREE |
| 2.2.2 | (retag of 2.2.1) | (retag of 2.2.1) | DISAGREE |

This discrepancy suggests that openssl-libs may be both inherited from the base image
AND redundantly listed as an explicit install in rpms.lock.yaml. Manual investigation
is required to determine the true remediation path:

- If the package is truly a base image dependency that is redundantly pinned in
  rpms.lock.yaml, remediation may involve both updating the base image AND updating
  the lock file pin.
- If the lock file pin overrides the base image version, remediation focuses on
  updating rpms.lock.yaml (or rpms.in.yaml).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, affected: versions before 3.0.7-28.el9_4):

| Version | openssl-libs version | Affected? | Notes |
|---------|----------------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fix version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fix version |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).

## 2.5 -- Upstream Fix Check

The RPM ecosystem in the 2.2.x stream does not have an Upstream Branch configured in
the Ecosystem Mappings table (the Upstream Branch column shows "--" for RPM). Upstream
fix checking is not applicable for system packages -- the fix is delivered through the
RPM distribution channel (Red Hat errata RHSA-2026:4021).

The fix IS available: the fixed version 3.0.7-28.el9_4 is already shipped in versions
2.2.3 and 2.2.4, confirming the RPM update has been published and consumed in later
releases.

## Cross-Stream Observations

Although triage is scoped to the 2.2.x stream, the mock data shows that the 2.1.x
stream also ships openssl-libs at vulnerable versions:

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |

This would trigger Case A (cross-stream impact) in Step 8 if the 2.1.x stream does
not have its own CVE Jira for this vulnerability.

## Proposed Jira Mutations (NOT EXECUTED)

The following actions would be proposed in subsequent triage steps:

### Step 3 -- Affects Versions Correction (PROPOSAL)

The current Affects Versions field shows "RHTPA 2.0.0" which does not correspond to
any version in the 2.2.x stream supportability matrix. Based on the version impact
analysis, the corrected Affects Versions should include the affected 2.2.x versions
(RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2) using dynamically discovered Jira version
IDs.

### Step 8 -- Remediation (PROPOSAL)

**Ecosystem**: RPM (system package) -- 1 remediation task per affected stream.

Since the fix is already available in later releases (2.2.3+), the remediation task
would focus on the Konflux release repo update for affected versions, noting that
no new builds of 2.2.0, 2.2.1, or 2.2.2 are expected unless a z-stream respin is
planned.

**Task type**: Konflux release repo fix (single task for the 2.2.x stream)

**SBOM disagreement note**: The remediation task description should flag the
rpms.lock.yaml vs. SBOM classification disagreement so the implementing engineer
can investigate the true package origin before determining the remediation approach
(lock file update vs. base image update vs. both).
