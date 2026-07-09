# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream only, scoped by [rhtpa-2.2])

From the 2.2.x stream security-matrix.md:

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Since the ecosystem is RPM, the lock file is `rpms.lock.yaml`. Extraction uses:
```
git show <tag>:rpms.lock.yaml | grep 'openssl-libs'
```

Extracted openssl-libs versions from rpms.lock.yaml at each pinned commit tag:

| Version | Tag | openssl-libs version (from rpms.lock.yaml) |
|---------|-----|-------------------------------------------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ -- same as 2.2.1: 3.0.7-27.el9_4 |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 |

## Version Impact Comparison

Fix threshold: 3.0.7-28.el9_4 (versions before this are affected).

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

## Step 2.3.5 -- Dependency Chain Context

### Package Origin Classification

**Investigation method**: rpms.lock.yaml (RPM lock file is configured for this stream)

**rpms.lock.yaml classification**: openssl-libs IS present in rpms.lock.yaml at all inspected tags. The lock file presence is the primary classification signal -- presence in rpms.lock.yaml indicates an **explicit install** (the package is explicitly specified in the rpms.in.yaml or equivalent package manifest, not merely inherited from the base image).

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign is not available / external tools are prohibited in eval mode.
    Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.in.yaml / rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to require openssl-libs >= 3.0.7-28.el9_4.
```

**SBOM verification status**: SBOM verification was skipped because external tools (cosign) are not available in this eval context. The rpms.lock.yaml classification is used as the sole signal. Per Step 2.3.5, the lock file presence is the primary classification signal -- SBOM verification supplements but does not replace it.
