# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from the 2.2.x stream matrix (Konflux release repo `rhtpa-release.0.4.z`).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Source pinning method: `artifacts.lock.yaml` (download URL contains tag).

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Extracted openssl-libs versions from `rpms.lock.yaml` at each pinned commit
via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

**Fix threshold**: 3.0.7-28.el9_4 (from Jira description; external CVE data
enrichment via MITRE and OSV.dev was not performed in this eval).

**Retag handling**: Version 2.2.2 is a retag of 2.2.1 (same backend commit `v0.4.8`).
Lock file check was skipped; result carried forward from 2.2.1.

## Cross-stream context (2.1.x stream -- informational)

The issue is scoped to 2.2.x, but the 2.1.x stream is also checked for
cross-stream impact analysis (Step 8 Case A):

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | **YES** | before 3.0.7-28.el9_4 |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | **YES** | before 3.0.7-28.el9_4 |

Both 2.1.x versions ship a vulnerable openssl-libs. Cross-stream impact
applies (see Step 8 Case A).

## 2.3.5 -- Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs entries found at all non-retag tags)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  SBOM verification: skipped -- cosign not available in this environment.
    Using rpms.lock.yaml classification only.

  Affected versions: 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4),
                      2.2.2 (retag of 2.2.1)
  Fixed in: 2.2.3+ (3.0.7-28.el9_4)

Remediation: update openssl-libs package spec in rpms.lock.yaml / rpms.in.yaml
to >= 3.0.7-28.el9_4.
```

**SBOM verification status**: SBOM comparison was not performed because `cosign`
is not available in this environment. The rpms.lock.yaml classification (explicit
install) is used as the sole source of truth for package origin. In a production
triage, `cosign download sbom` would be used to cross-check the rpms.lock.yaml
classification against the final and base image SBOMs.

## 2.4 -- Version Impact Summary

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | equals fixed version |

**Key finding**: The fix (openssl-libs 3.0.7-28.el9_4) is already present in
versions 2.2.3 and 2.2.4. The vulnerability was remediated by the regular
release process starting with build 0.4.11 (2026-03-23). Versions 2.2.0
through 2.2.2 were affected and customers on those versions should upgrade
to 2.2.3 or later.
