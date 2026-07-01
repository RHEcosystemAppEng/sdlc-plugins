# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

The issue is scoped to stream `[rhtpa-2.2]`, so only the 2.2.x stream supportability matrix is used. The matrix is loaded from the local security-matrix.md for stream `rhtpa-release.0.4.z`.

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

For the RPM ecosystem, the lock file is `rpms.lock.yaml`. The check command is `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each pinned commit tag.

Extracted openssl-libs versions from rpms.lock.yaml at each pinned tag:

| Tag | openssl-libs version | Source |
|-----|----------------------|--------|
| `v0.4.5` | 3.0.7-25.el9_3 | rpms.lock.yaml |
| `v0.4.8` | 3.0.7-27.el9_4 | rpms.lock.yaml |
| `v0.4.9` | _(retag of v0.4.8)_ | retag -- same as v0.4.8 |
| `v0.4.11` | 3.0.7-28.el9_4 | rpms.lock.yaml |
| `v0.4.12` | 3.0.7-28.el9_4 | rpms.lock.yaml |

## 2.4 -- Version Impact Table

CVE-2026-40215 affects openssl-libs versions before 3.0.7-28.el9_4. The fix version is 3.0.7-28.el9_4. Comparison uses RPM version ordering.

**Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):**

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable openssl-libs package. Versions 2.2.3 and 2.2.4 ship the patched version and are not affected.

## 2.3.5 -- Dependency Chain Context

### Package Classification

**openssl-libs** is present in `rpms.lock.yaml` for the affected versions (2.2.0 through 2.2.2). The rpms.lock.yaml presence is the primary classification signal.

**rpms.lock.yaml classification**: openssl-libs is listed in rpms.lock.yaml for each version tag checked. This indicates it is an **explicit install** -- the package is explicitly specified in the RPM lock file (or rpms.in.yaml), not merely inherited from the base image.

### SBOM Verification

> SBOM verification skipped -- cosign not available. External tool invocations are prohibited in this eval context. Using rpms.lock.yaml classification only.

### Dependency Chain Summary

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available (external tools prohibited)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package version in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The rpms.lock.yaml classification is the primary signal. The SBOM verification step was skipped because cosign is not available in this environment. The rpms.lock.yaml data alone is sufficient to determine the remediation path.

### Version History

- **2.2.0** (v0.4.5): openssl-libs 3.0.7-25.el9_3 -- affected
- **2.2.1** (v0.4.8): openssl-libs 3.0.7-27.el9_4 -- affected (updated but still below fix)
- **2.2.2** (v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- **2.2.3** (v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT affected (fix version)
- **2.2.4** (v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT affected (fix version)

The fix was picked up in version 2.2.3 (build 0.4.11, dated 2026-03-23).
